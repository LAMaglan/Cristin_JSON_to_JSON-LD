import requests

# Parse through projects and publications from Cristin API (v2) and transform
# to JSON-LD. Made as generic as possible, to better adapt if Cristin changes
# schema of their data.


# project schema:
# https://api.cristin.no/v2/doc/json-schemas/projects_GET_POST_response.json

# publication schema:
# https://api.cristin.no/v2/doc/json-schemas/results_GET_response.json


def input_as_list(input) -> list:
    """convert to list of dicts if not already
     (might happen if just one "instance") """

    if isinstance(input, list):
        return input
    else:
        single_file = input
        single_file_as_list = []
        single_file_as_list.append(single_file)
        return single_file_as_list


def edit_title_format(string):
    """Removes potential underscores and titlecase each word"""

    return "".join(x.capitalize() or "_" for x in string.split("_"))


def get_cristin_data(data_id=302186, type="project") -> list:
    """Get data from Cristin API. Currently set up to extract data
    from a specific project or publication. Can be modified (i.e. extract
    more than one publication/project, other types, etc.)"""

    if type == "project":
        request = "projects"
    elif type == "publication":
        request = "results"

    URL_request = f"https://api.cristin.no/v2/{request}/{data_id}"

    cristin_data = requests.get(URL_request)
    cristin_data = cristin_data.json()

    return cristin_data


def link_cristin_projects(
    input_dict: dict,
    custom_project_URL="http://cristin/project_id/",
    project_type: str = "Project",
    title_type: str = "Title",
) -> dict:
    """ within "projects" list of an publication, for each dictionary, check if an
    publication has a  cristin_project_id, and if so, create a link to that project with an @id"""

    if "projects" in input_dict:
        for project in input_dict["projects"]:
            if "cristin_project_id" in project:
                # empty each project input_dict and add id to link with cristin project
                project_id = project["cristin_project_id"]
                project.clear()
                project["@id"] = custom_project_URL + project_id
            else:
                project["@type"] = project_type
                if "title" in project:
                    project["title"]["@type"] = title_type


def link_cristin_publications(
    input_dict: dict,
    replace_string="https://api.cristin.no/v2/results/",
    custom_publication_URL="http://cristin/publication_id/",
) -> dict:
    """ check if an project has a "results" array with publications (strings),
    and if so, create a link to that publication with an @id"""

    if "results" in input_dict:

        for publication in range(len(input_dict["results"])):

            # step 1: switch cristin string with custom string
            input_dict["results"][publication] = input_dict["results"][publication].replace(
                replace_string, custom_publication_URL
            )

            # step 2: make each element into a dict with @id
            tmp = input_dict["results"][publication]
            input_dict["results"][publication] = {}
            input_dict["results"][publication]["@id"] = tmp


def add_type(input_dict: dict, key: str, type_name: str) -> dict:
    """ add @type to a dictionary object, or to each dictionary
    contained within a list"""

    if key in input_dict:
        if isinstance(input_dict[key], list) or isinstance(input_dict[key], dict):
            if not isinstance(input_dict[key], list):
                input_dict[key]["@type"] = type_name
            else:
                for multi_instance in input_dict[key]:
                    if isinstance(multi_instance, dict):
                        multi_instance["@type"] = type_name


def add_type_nesting_dict(input_obj, parent_key, verbose=False):
    """ add a @type to every nested dictionary, with
    recursion to continue through nested dictionaries, or
    call the list variant of this function"""

    for nested_key, _ in input_obj[parent_key].items():
        if verbose:
            nested_key_type = type(input_obj[parent_key][nested_key])
            print(f"the data type of {nested_key} is {nested_key_type}")
        add_type(
            input_dict=input_obj[parent_key],
            key=nested_key,
            type_name=edit_title_format(nested_key),
        )

        # recursion
        if isinstance(input_obj[parent_key][nested_key], dict):
            add_type_nesting_dict(input_obj[parent_key], parent_key=nested_key)
        elif isinstance(input_obj[parent_key][nested_key], list):
            add_type_nesting_list(input_obj[parent_key], parent_key=nested_key)


def add_type_nesting_list(input_obj, parent_key, verbose=False):
    """ add a @type to every dictionary element of a list, with
    recursion, or call the diciontar variant of this function"""

    for idx, element in enumerate(input_obj[parent_key]):
        if verbose:
            data_type = type(element)
            print(f"the data type of {element} is {data_type}")
        if isinstance(element, dict) or isinstance(element, list):
            for nested_key in element.keys():
                if isinstance(element, dict) or isinstance(element, list):
                    add_type(
                        input_dict=element, key=nested_key, type_name=edit_title_format(
                            nested_key),
                    )

                # recursion
                if isinstance(input_obj[parent_key][idx][nested_key], dict):
                    add_type_nesting_dict(
                        input_obj[parent_key][idx], parent_key=nested_key)

                elif isinstance(input_obj[parent_key][idx][nested_key], list):
                    add_type_nesting_list(
                        input_obj[parent_key][idx], parent_key=nested_key)


def add_type_nesting(input_obj, parent_key):
    """ call one of two recursive functions depending
    on whether the object is a dictionary or a list"""

    if isinstance(input_obj[parent_key], dict):
        add_type_nesting_dict(input_obj, parent_key)
    elif isinstance(input_obj[parent_key], list):
        add_type_nesting_list(input_obj, parent_key)


def add_all_types(single_instance, verbose=False):
    """ go through a single instance from Cristin, and
    add types to every contained dictionaries"""

    for key, _ in single_instance.items():
        if verbose:
            print(f"the key {key} is in project_orig")

        add_type(
            input_dict=single_instance, key=key, type_name=edit_title_format(
                key),
        )

        add_type_nesting(input_obj=single_instance, parent_key=key)


def cristin_to_JSON_LD(
    cristin_inputs,
    type="project",
    context_name="http://cristin/result/project/",
    custom_URL="http://cristin/project_id/",
    custom_link_URL="http://cristin/publication_id/",
    verbose=False,
) -> list:
    """
    convert cristin inputs from
    JSON to JSON-lD
    """

    cristin_inputs = input_as_list(cristin_inputs)

    # empty list for processed input data
    inputs_JSON = []

    context = {"@vocab": context_name}

    if type == "project":
        id_string = "cristin_project_id"
    elif type == "publication":
        id_string = "cristin_result_id"

    for index, input_orig in enumerate(cristin_inputs):

        # Initialize empty input_dict
        # as of python 3.6, input_dictionaries are insertion ordered
        input = {}

        if verbose:
            print(f"processing input {index} of {len(cristin_inputs)}")

        # Add new keys in order
        input["@context"] = context
        input["@id"] = custom_URL + input_orig[id_string]
        input["@type"] = type.title()

        add_all_types(input_orig)

        if type == "project":
            link_cristin_publications(
                input_dict=input_orig, custom_publication_URL=custom_link_URL)
        elif type == "publication":
            link_cristin_projects(
                input_dict=input_orig,
                custom_project_URL=custom_link_URL,
                project_type="Project",
                title_type="Title",
            )

        # merge to (ordered) input_dict
        input = {**input, **input_orig}

        # append processed result to JSON list
        inputs_JSON.append(input)

    print("input payloads are ready")

    return inputs_JSON


if __name__ == "__main__":

    # Example project_ids
    project_ids = [302186, 450627, 501114, 520677, 574074, 574076]

    cristin_selected_projects = []

    for project_id in project_ids:
        print(f"getting data for project: {project_id}")
        cristin_selected_projects.append(
            get_cristin_data(data_id=project_id, type="project"))

    all_projects = cristin_to_JSON_LD(
        cristin_selected_projects,
        type="project",
        context_name="http://cristin/result/project/",
        custom_URL="http://cristin/project_id/",
        custom_link_URL="http://cristin/publication_id/",
    )

    # Example publication_ids
    publication_ids = [1055733, 1046529, 1046521]

    cristin_selected_publications = []

    for publication_id in publication_ids:
        print(f"getting data for publication: {publication_id}")
        cristin_selected_publications.append(
            get_cristin_data(data_id=publication_id, type="publication")
        )

    all_publications = cristin_to_JSON_LD(
        cristin_selected_publications,
        type="publication",
        context_name="http://cristin/result/publication/",
        custom_URL="http://cristin/publication_id/",
        custom_link_URL="http://cristin/project_id/",
    )

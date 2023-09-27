# General

Parse through projects and publications from Cristin API (v2) and transform
to JSON-LD. See API documentation [here](https://api.cristin.no/v2/doc/index.html) Made as generic as possible, to better adapt if Cristin changes
schema of their data.

Mainly set up to parse publications and projects data, and to link together via
the `@id` key/identifier. If other data is to be extracted, (e.g. about institutions), 
the function  `get_cristin_data()` must be modified. 

`get_cristin_data()` is set up to extract data from specific publications/projects, but can be modified (see API documentation), e.g. to take all data (remove `data_id` paramater), or from specified
institutions.

See example use in section under

```python
if __name__ == "__main__":
```

Tested on python v3.7.10



## Examples

Raw output (JSON) as dict from list element of`get_cristin_data()`. Parsed data
(JSON-LD) as dict from list element of `cristin_to_JSON_LD()`. Printed as JSON via
```python
import json
print(json.dumps(<element of either above functions>, indent=4, sort_keys=False))
```

### Project

raw project data

```json
{
    "cristin_project_id": "302186",
    "publishable": true,
    "published": true,
    "title": {
        "no": "In vivo dynamics of plant responses to tropospheric ozone"
    },
    "main_language": "no",
    "start_date": "2007-11-01T00:00:00.000Z",
    "end_date": "2011-10-31T00:00:00.000Z",
    "status": "CONCLUDED",
    "created": {
        "date": "2010-01-18T09:05:14.000Z"
    },
    "last_modified": {
        "date": "2010-02-15T10:37:16.000Z"
    },
    "coordinating_institution": {
        "institution": {
            "cristin_institution_id": "185",
            "institution_name": {
                "en": "University of Oslo"
            },
            "url": "https://api.cristin.no/v2/institutions/185"
        },
        "unit": {
            "cristin_unit_id": "185.15.21.0",
            "unit_name": {
                "en": "Department of Biosciences"
            }
        }
    },
    "languages": [
        {
            "code": "no",
            "name": {
                "en": "Norwegian"
            }
        }
    ],
    "participants": [
        {
            "cristin_person_id": "23938",
            "first_name": "Aud Else Berglen",
            "surname": "Eriksen",
            "url": "https://api.cristin.no/v2/persons/23938",
            "roles": [
                {
                    "role_code": "PRO_MANAGER",
                    "institution": {
                        "cristin_institution_id": "185",
                        "institution_name": {
                            "en": "University of Oslo"
                        }
                    },
                    "unit": {
                        "cristin_unit_id": "185.15.21.40",
                        "unit_name": {
                            "en": "Program for Toxicology and Ecological Physiology"
                        }
                    }
                }
            ]
        }
    ],
    "participants_url": "https://api.cristin.no/v2/projects/302186/participants",
    "academic_summary": {
        "no": "Ikke-destruktive visualiseringsteknikker s\u00e5 som termografi, multispektral reflektans bildetaking, fluorescens og magnetisk resonans avbildning har i de senere \u00e5r i \u00f8kende grad blitt tatt i bruk innen plantefysiologiske studier. Den h\u00f8ye tids- og romlig oppl\u00f8sningen til metodene gj\u00f8r det mulig \u00e5 kartlegge raske og lokaliserte in vivo endringer i plantenes fysiologiske tilstand f\u00f8r synlige endringer kan detekteres. I f\u00f8lgende prosjekt vil vi benytte flere ikke-destruktive m\u00e5lemetoder og visualiseringsteknikker for \u00e5 kartlegge og forst\u00e5 in vivo skader for\u00e5rsaket av en av de viktigste fytotoksiske luftforurensinger - bakken\u00e6rt ozon. Prosjektet er interdisiplin\u00e6rt hvor b\u00e5de eksperimentelle og teoretiske metoder fra biologi, fysikk, dynamikk av komplekse systemer, m\u00f8nsterdannende prosesser og informatikk vil bli brukt. Utvikling av analyse- og modelleringsverkt\u00f8y vil ogs\u00e5 v\u00e6re sentralt. Ozon er en reaktiv, giftig gass som kan f\u00f8re til slimhinneskader i mennesker samt alvorlige skader p\u00e5 vegetasjon. Bakken\u00e6rt ozon dannes i troposf\u00e6ren gjennom kjemiske reaksjoner hvor blant annet utslipp fra biltransport og industri inng\u00e5r. Reaksjonene krever solstr\u00e5ling og ozonproduksjonen er dermed st\u00f8rst i sommerhalv\u00e5ret. Dette sammenfaller med vekstsesongen og kan dermed f\u00f8re til store tap i avlinger og redusert biomasseproduksjonen i skog og mark. I l\u00f8pet av de siste 100 \u00e5r, har bakgrunnsniv\u00e5et til bakken\u00e6rt ozon \u00f8kt fra ca. 10 ppb til 30-40 ppb. Ozonepisoder med niv\u00e5er over 100 ppb blir stadig vanligere ogs\u00e5 i Skandinavia. Bakken\u00e6rt ozon blir dermed sett p\u00e5 som en av de viktigste fytotoksiske luftforurensinger."
    },
    "creator": {
        "cristin_person_id": "5641",
        "first_name": "Agnethe",
        "surname": "Sidselrud",
        "roles": [
            {
                "unit": {
                    "cristin_unit_id": "185.0.0.0"
                }
            }
        ]
    }
}

```

project in JSON-LD

```json
{
    "@context": {
        "@vocab": "http://cristin/result/project/"
    },
    "@id": "http://cristin/project_id/302186",
    "@type": "Project",
    "cristin_project_id": "302186",
    "publishable": true,
    "published": true,
    "title": {
        "no": "In vivo dynamics of plant responses to tropospheric ozone",
        "@type": "Title"
    },
    "main_language": "no",
    "start_date": "2007-11-01T00:00:00.000Z",
    "end_date": "2011-10-31T00:00:00.000Z",
    "status": "CONCLUDED",
    "created": {
        "date": "2010-01-18T09:05:14.000Z",
        "@type": "Created"
    },
    "last_modified": {
        "date": "2010-02-15T10:37:16.000Z",
        "@type": "LastModified"
    },
    "coordinating_institution": {
        "institution": {
            "cristin_institution_id": "185",
            "institution_name": {
                "en": "University of Oslo",
                "@type": "InstitutionName"
            },
            "url": "https://api.cristin.no/v2/institutions/185",
            "@type": "Institution"
        },
        "unit": {
            "cristin_unit_id": "185.15.21.0",
            "unit_name": {
                "en": "Department of Biosciences",
                "@type": "UnitName"
            },
            "@type": "Unit"
        },
        "@type": "CoordinatingInstitution"
    },
    "languages": [
        {
            "code": "no",
            "name": {
                "en": "Norwegian",
                "@type": "Name"
            },
            "@type": "Languages"
        }
    ],
    "participants": [
        {
            "cristin_person_id": "23938",
            "first_name": "Aud Else Berglen",
            "surname": "Eriksen",
            "url": "https://api.cristin.no/v2/persons/23938",
            "roles": [
                {
                    "role_code": "PRO_MANAGER",
                    "institution": {
                        "cristin_institution_id": "185",
                        "institution_name": {
                            "en": "University of Oslo",
                            "@type": "InstitutionName"
                        },
                        "@type": "Institution"
                    },
                    "unit": {
                        "cristin_unit_id": "185.15.21.40",
                        "unit_name": {
                            "en": "Program for Toxicology and Ecological Physiology",
                            "@type": "UnitName"
                        },
                        "@type": "Unit"
                    },
                    "@type": "Roles"
                }
            ],
            "@type": "Participants"
        }
    ],
    "participants_url": "https://api.cristin.no/v2/projects/302186/participants",
    "academic_summary": {
        "no": "Ikke-destruktive visualiseringsteknikker s\u00e5 som termografi, multispektral reflektans bildetaking, fluorescens og magnetisk resonans avbildning har i de senere \u00e5r i \u00f8kende grad blitt tatt i bruk innen plantefysiologiske studier. Den h\u00f8ye tids- og romlig oppl\u00f8sningen til metodene gj\u00f8r det mulig \u00e5 kartlegge raske og lokaliserte in vivo endringer i plantenes fysiologiske tilstand f\u00f8r synlige endringer kan detekteres. I f\u00f8lgende prosjekt vil vi benytte flere ikke-destruktive m\u00e5lemetoder og visualiseringsteknikker for \u00e5 kartlegge og forst\u00e5 in vivo skader for\u00e5rsaket av en av de viktigste fytotoksiske luftforurensinger - bakken\u00e6rt ozon. Prosjektet er interdisiplin\u00e6rt hvor b\u00e5de eksperimentelle og teoretiske metoder fra biologi, fysikk, dynamikk av komplekse systemer, m\u00f8nsterdannende prosesser og informatikk vil bli brukt. Utvikling av analyse- og modelleringsverkt\u00f8y vil ogs\u00e5 v\u00e6re sentralt. Ozon er en reaktiv, giftig gass som kan f\u00f8re til slimhinneskader i mennesker samt alvorlige skader p\u00e5 vegetasjon. Bakken\u00e6rt ozon dannes i troposf\u00e6ren gjennom kjemiske reaksjoner hvor blant annet utslipp fra biltransport og industri inng\u00e5r. Reaksjonene krever solstr\u00e5ling og ozonproduksjonen er dermed st\u00f8rst i sommerhalv\u00e5ret. Dette sammenfaller med vekstsesongen og kan dermed f\u00f8re til store tap i avlinger og redusert biomasseproduksjonen i skog og mark. I l\u00f8pet av de siste 100 \u00e5r, har bakgrunnsniv\u00e5et til bakken\u00e6rt ozon \u00f8kt fra ca. 10 ppb til 30-40 ppb. Ozonepisoder med niv\u00e5er over 100 ppb blir stadig vanligere ogs\u00e5 i Skandinavia. Bakken\u00e6rt ozon blir dermed sett p\u00e5 som en av de viktigste fytotoksiske luftforurensinger.",
        "@type": "AcademicSummary"
    },
    "creator": {
        "cristin_person_id": "5641",
        "first_name": "Agnethe",
        "surname": "Sidselrud",
        "roles": [
            {
                "unit": {
                    "cristin_unit_id": "185.0.0.0",
                    "@type": "Unit"
                },
                "@type": "Roles"
            }
        ],
        "@type": "Creator"
    }
}
```

### Publication

raw publication data


```json
{
    "category": {
        "code": "ARTICLE",
        "name": {
            "en": "Academic article"
        }
    },
    "channel": {
        "title": "Science in Context"
    },
    "contributors": {
        "url": "https://api.cristin.no/v2/results/1055733/contributors",
        "count": 2,
        "preview": [
            {
                "first_name": "Kristin",
                "surname": "Asdal"
            },
            {
                "first_name": "Christoph",
                "surname": "Gradmann"
            }
        ]
    },
    "cristin_result_id": "1055733",
    "created": {
        "date": "2013-10-07T14:55:22.000Z"
    },
    "funding_sources": [
        {
            "funding_source_code": "NFR",
            "project_code": "195648",
            "funding_source_name": {
                "en": "Research Council of Norway (RCN)"
            }
        }
    ],
    "last_modified": {
        "date": "2014-08-13T13:08:09.000Z"
    },
    "links": [
        {
            "url_type": "DOI",
            "url": "https://doi.org/10.1017/S0269889714000039"
        }
    ],
    "open_access": "none",
    "original_language": "en",
    "projects": [
        {
            "cristin_project_id": "450627",
            "title": {
                "nb": "Transformasjoner/Innovasjoner: \u00c5 gripe endring, \u00e5 lese tekster, \u00e5 skrive inn natur"
            },
            "url": "https://api.cristin.no/v2/projects/450627"
        }
    ],
    "title": {
        "en": "Science, technology, medicine - and the state: The science-state nexus in Scandinavia 1850-1980"
    },
    "year_published": "2014",
    "year_reported": "2014",
    "url": "https://api.cristin.no/v2/results/1055733",
    "journal": {
        "cristin_journal_id": "8493",
        "name": "Science in Context",
        "publisher": {
            "cristin_publisher_id": "123",
            "name": "Cambridge University Press",
            "url": "http://www.cambridge.org",
            "nvi_level": "2"
        },
        "international_standard_numbers": [
            {
                "type": "printed",
                "value": "0269-8897"
            },
            {
                "type": "electronic",
                "value": "1474-0664"
            }
        ],
        "nvi_level": "2"
    },
    "volume": "27",
    "issue": "3",
    "pages": {
        "from": "177",
        "to": "186"
    }
}
```

publication in JSON-LD

```json
{
    "@context": {
        "@vocab": "http://cristin/result/publication/"
    },
    "@id": "http://cristin/publication_id/1055733",
    "@type": "Publication",
    "category": {
        "code": "ARTICLE",
        "name": {
            "en": "Academic article",
            "@type": "Name"
        },
        "@type": "Category"
    },
    "channel": {
        "title": "Science in Context",
        "@type": "Channel"
    },
    "contributors": {
        "url": "https://api.cristin.no/v2/results/1055733/contributors",
        "count": 2,
        "preview": [
            {
                "first_name": "Kristin",
                "surname": "Asdal",
                "@type": "Preview"
            },
            {
                "first_name": "Christoph",
                "surname": "Gradmann",
                "@type": "Preview"
            }
        ],
        "@type": "Contributors"
    },
    "cristin_result_id": "1055733",
    "created": {
        "date": "2013-10-07T14:55:22.000Z",
        "@type": "Created"
    },
    "funding_sources": [
        {
            "funding_source_code": "NFR",
            "project_code": "195648",
            "funding_source_name": {
                "en": "Research Council of Norway (RCN)",
                "@type": "FundingSourceName"
            },
            "@type": "FundingSources"
        }
    ],
    "last_modified": {
        "date": "2014-08-13T13:08:09.000Z",
        "@type": "LastModified"
    },
    "links": [
        {
            "url_type": "DOI",
            "url": "https://doi.org/10.1017/S0269889714000039",
            "@type": "Links"
        }
    ],
    "open_access": "none",
    "original_language": "en",
    "projects": [
        {
            "@id": "http://cristin/project_id/450627"
        }
    ],
    "title": {
        "en": "Science, technology, medicine - and the state: The science-state nexus in Scandinavia 1850-1980",
        "@type": "Title"
    },
    "year_published": "2014",
    "year_reported": "2014",
    "url": "https://api.cristin.no/v2/results/1055733",
    "journal": {
        "cristin_journal_id": "8493",
        "name": "Science in Context",
        "publisher": {
            "cristin_publisher_id": "123",
            "name": "Cambridge University Press",
            "url": "http://www.cambridge.org",
            "nvi_level": "2",
            "@type": "Publisher"
        },
        "international_standard_numbers": [
            {
                "type": "printed",
                "value": "0269-8897",
                "@type": "InternationalStandardNumbers"
            },
            {
                "type": "electronic",
                "value": "1474-0664",
                "@type": "InternationalStandardNumbers"
            }
        ],
        "nvi_level": "2",
        "@type": "Journal"
    },
    "volume": "27",
    "issue": "3",
    "pages": {
        "from": "177",
        "to": "186",
        "@type": "Pages"
    }
}
```

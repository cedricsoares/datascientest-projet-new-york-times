RESULTS_BY_PAGE = 20
MAX_API_CALLS = 500
MAX_BOOKS_MOVIES_CALLS = 220

INDEX_SETTINGS = {
    "number_of_shards": 2,
    "number_of_replicas": 2
}

NEWS_MAPPING = {
        'properties': {
            'abstract': {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
            'byline':  {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
            'created_date': {'type': 'date'},
            'des_facet': {'type': 'keyword'},
            'first_published_date': {'type': 'date'},
            'geo_facet': {'type': 'keyword'},
            'item_type': {'type': 'keyword'},
            'kicker':  {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
            'material_type_facet': {'type': 'keyword'},
            'multimedia': {
                'type': 'nested',
                'properties': {
                    'caption':  {
                                    'type': 'text',
                                    'analyzer': 'english',
                                    'fields': {
                                        'keyword': {
                                                        "type": "keyword"
                                                    }
                                        }
                                },
                    'copyright':  {
                                    'type': 'text',
                                    'analyzer': 'english',
                                    'fields': {
                                        'keyword': {
                                                        "type": "keyword"
                                                    }
                                        }
                                },
                    'format': {'type': 'keyword'},
                    'height': {'type': 'integer'},
                    'subtype': {'type': 'keyword'},
                    'type': {'type': 'keyword'},
                    'url':  {
                                'type': 'text',
                                'analyzer': 'english',
                                'fields': {
                                    'keyword': {
                                                    "type": "keyword"
                                                }
                                    }
                            },
                    'width': {'type': 'integer'}
                }
            },
            'org_facet': {'type': 'keyword'},
            'per_facet': {'type': 'keyword'},
            'published_date': {'type': 'date'},
            'section': {'type': 'keyword'},
            'slug_name': {'type': 'keyword'},
            'source': {
                        'type': 'text',
                        'analyzer': 'english',
                        'fields': {
                            'keyword': {
                                            "type": "keyword"
                                        }
                            }
                        },
            'subheadline': {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
            'subsection': {'type': 'keyword'},
            'thumbnail_standard': {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
            'title': {
                        'type': 'text',
                        'analyzer': 'english',
                        'fields': {
                            'keyword': {
                                            "type": "keyword"
                                        }
                            }
                    },
            'updated_date': {'type': 'date'},
            'uri': {'type': 'keyword'},
            'url': {
                    'type': 'text',
                    'analyzer': 'english',
                    'fields': {
                        'keyword': {
                                        "type": "keyword"
                                    }
                        }
                    },
        }
    }

BOOKS_MAPPING = {
    'properties': {
        'title': {
                    'type': 'text',
                    'analyzer': 'english',
                    'fields': {
                        'keyword': {
                                        "type": "keyword"
                                    }
                        }
                },
        'description': {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
        'contributor': {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
        'author': {
                    'type': 'text',
                    'analyzer': 'english',
                    'fields': {
                        'keyword': {
                                        "type": "keyword"
                                    }
                        }
                    },
        'contributor_note': {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
        'price': {'type': 'float'},
        'age_group': {'type': 'keyword'},
        'publisher': {
                        'type': 'text',
                        'analyzer': 'english',
                        'fields': {
                            'keyword': {
                                            "type": "keyword"
                                        }
                            }
                        },
        'isbns': {
            'type': 'nested',
            'properties': {
                'isbn10': {'type': 'keyword'},
                'isbn13': {'type': 'keyword'},
            }
        },
        'ranks_history': {
            'type': 'nested',
            'properties': {
                'primary_isbn10': {'type': 'keyword'},
                'primary_isbn13': {'type': 'keyword'},
                'rank': {'type': 'integer'},
                'list_name': {
                                'type': 'text',
                                'analyzer': 'english',
                                'fields': {
                                    'keyword': {
                                                    "type": "keyword"
                                                }
                                    }
                            },
                'display_name': {
                                    'type': 'text',
                                    'analyzer': 'english',
                                    'fields': {
                                        'keyword': {
                                                        "type": "keyword"
                                                    }
                                        }
                                },
                'published_date': {'type': 'date'},
                'bestsellers_date': {'type': 'date'},
                'weeks_on_list': {'type': 'integer'},
                'ranks_last_week': {'type': 'integer', 'null_value': None},
                'asterisk': {'type': 'integer'},
                'dagger': {'type': 'integer'},
            }
        },
        'reviews': {
            'type': 'nested',
            'properties': {
                'book_review_link': {'type': 'keyword'},
                'first_chapter_link': {'type': 'keyword'},
                'sunday_review_link': {'type': 'keyword'},
                'article_chapter_link': {'type': 'keyword'},
                }
            },
        }
}

MOVIES_MAPPING = {
    "properties": {
        "byline":  {
                        'type': 'text',
                        'analyzer': 'english',
                        'fields': {
                            'keyword': {
                                            "type": "keyword"
                                        }
                            }
                    },
        "critics_pick": {"type": "integer"},
        "date_updated": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
        "display_title": {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
        "headline":  {
                        'type': 'text',
                        'analyzer': 'english',
                        'fields': {
                            'keyword': {
                                            "type": "keyword"
                                        }
                            }
                    },
        "link": {
            "properties": {
                "suggested_link_text": {
                                            'type': 'text',
                                            'analyzer': 'english',
                                            'fields': {
                                                'keyword': {
                                                                "type": "keyword"
                                                            }
                                                }
                                        },
                "type": {"type": "keyword"},
                "url": {"type": "text"}
            }
        },
        "mpaa_rating": {"type": "keyword"},
        "multimedia": {
            "properties": {
                "height": {"type": "integer"},
                "src":  {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
                "type": {"type": "keyword"},
                "width": {"type": "integer"}
            }
        },
        "opening_date": {"type": "date", "format": "yyyy-MM-dd"},
        "publication_date": {"type": "date", "format": "yyyy-MM-dd"},
        "summary_short":  {
                            'type': 'text',
                            'analyzer': 'english',
                            'fields': {
                                'keyword': {
                                                "type": "keyword"
                                            }
                                }
                        },
    }
}

NEWS_CONFIGURATION = {
    'mapping': NEWS_MAPPING,
    'settings': INDEX_SETTINGS,
}

BOOKS_CONFIGURATION = {
    'mapping': BOOKS_MAPPING,
    'settings': INDEX_SETTINGS,
}

MOVIES_CONFIGURATION = {
    'mapping': MOVIES_MAPPING,
    'settings': INDEX_SETTINGS,
}

CONFIGURATIONS = {
    'news': NEWS_CONFIGURATION,
    'books': BOOKS_CONFIGURATION,
    'movies': MOVIES_CONFIGURATION
}

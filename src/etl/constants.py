INDEXES_SETTINGS = {
    "number_of_shards": 2,
    "number_of_replicas": 2
}

INDEXEXES_NAMES = ['newswire', 'books', 'movies']

NEWSWIRE_MAPPING = {
        'properties': {
            'abstract': {'type': 'text', 'analyzer': 'english'},
            'byline': {'type': 'text', 'analyzer': 'english'},
            'created_date': {'type': 'date'},
            'des_facet': {'type': 'keyword'},
            'first_published_date': {'type': 'date'},
            'geo_facet': {'type': 'keyword'},
            'item_type': {'type': 'keyword'},
            'kicker': {'type': 'text'},
            'material_type_facet': {'type': 'keyword'},
            'multimedia': {
                'type': 'nested',
                'properties': {
                    'caption': {'type': 'text', 'analyzer': 'english'},
                    'copyright': {'type': 'text', 'analyzer': 'english'},
                    'format': {'type': 'keyword'},
                    'height': {'type': 'integer'},
                    'subtype': {'type': 'keyword'},
                    'type': {'type': 'keyword'},
                    'url': {'type': 'text', 'analyzer': 'english'},
                    'width': {'type': 'integer'}
                }
            },
            'org_facet': {'type': 'keyword'},
            'per_facet': {'type': 'keyword'},
            'published_date': {'type': 'date'},
            'section': {'type': 'keyword'},
            'slug_name': {'type': 'keyword'},
            'source': {'type': 'text', 'analyzer': 'english'},
            'subheadline': {'type': 'text', 'analyzer': 'english'},
            'subsection': {'type': 'keyword'},
            'thumbnail_standard': {'type': 'text', 'analyzer': 'english'},
            'title': {'type': 'text'},
            'updated_date': {'type': 'date'},
            'uri': {'type': 'keyword'},
            'url': {'type': 'text', 'analyzer': 'english'}
        }
    }

BOOKS_MAPPING = {
    'properties': {
        'title': {'type': 'text', 'analyzer': 'english'},
        'description': {'type': 'text', 'analyzer': 'english'},
        'contributor': {'type': 'text', 'analyzer': 'english'},
        'author': {'type': 'text', 'analyzer': 'english'},
        'contributor_note': {'type': 'text', 'analyzer': 'english'},
        'price': {'type': 'float'},
        'age_group': {'type': 'keyword'},
        'publisher': {'type': 'text', 'analyzer': 'english'},
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
                'list_name': {'type': 'text', 'analyzer': 'english'},
                'display_name': {'type': 'text', 'analyzer': 'english'},
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
        "byline":  {'type': 'text', 'analyzer': 'english'},
        "critics_pick": {"type": "integer"},
        "date_updated": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
        "display_title": {'type': 'text', 'analyzer': 'english'},
        "headline":  {'type': 'text', 'analyzer': 'english'},
        "link": {
            "properties": {
                "suggested_link_text":  {'type': 'text', 'analyzer': 'english'},
                "type": {"type": "keyword"},
                "url": {"type": "text"}
            }
        },
        "mpaa_rating": {"type": "keyword"},
        "multimedia": {
            "properties": {
                "height": {"type": "integer"},
                "src":  {'type': 'text', 'analyzer': 'english'},
                "type": {"type": "keyword"},
                "width": {"type": "integer"}
            }
        },
        "opening_date": {"type": "date", "format": "yyyy-MM-dd"},
        "publication_date": {"type": "date", "format": "yyyy-MM-dd"},
        "summary_short": {"type": "text"}
    }
}

movies_settings = {
    "number_of_shards": 2,
    "number_of_replicas": 2
}

OFFSET_VALUE = 0
OFFSET_FACTOR = 20
END_POINT_HITS = 35311
API_CALL_DAILY_INDEX = 0

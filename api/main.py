import json
from datetime import date, timedelta
from typing import Annotated, Optional

from elasticsearch import AsyncElasticsearch
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel

api = FastAPI(
    title='Elasticsearch database API',
    description='Expose Elastic search indices',
    version='0.0.1',
    openapi_tags=[
        {
            'name': 'news',
            'description': 'Related to news functions'
        },
        {
            'name': 'books',
            'description': 'Related to books functions'
        },
        {
            'name': 'movies',
            'description': 'Related to movies functions'
        }
    ]
)

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {
    "dashboard": {
        "username": "dashboard",
        "name": "NYT contents dashboard",
        "hashed_password": pwd_context.hash("dst_NYT_dashboard")
    }
}

es = AsyncElasticsearch(hosts="http://@localhost:9200")


class elasticResponse(BaseModel):
    """Retieved response from Elastiucsearch database

    Attributes:
        data (str): Json string of useful retieved response from Elastiscsearch
            database
    """

    data: str


def get_current_user(
                        credentials: HTTPBasicCredentials = Depends(security)
                    ) -> str:
    """"Check authentication
    """
    username = credentials.username
    if not (users.get(username)) or not (pwd_context.verify(
     credentials.password, users[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_time_scale(time_scale: str) -> tuple[Optional[date], Optional[date]]:
    """Return datetimes to use in queries filters

    Args:
        time_scale (str): Time scale used to define datetimes

    Returns:
        tuple(date, date): Dates corresponding of start and end of a time scale
    """

    if time_scale == "yesterday":
        today = date.today()
        start_date = today - timedelta(days=1)
        end_date = today
        return start_date, end_date

    elif time_scale == "week_ago":
        today = date.today()
        start_date = today - timedelta(days=7)
        end_date = today
        return start_date, end_date

    elif time_scale == "month_ago":
        today = date.today()
        start_date = today - timedelta(days=30)
        end_date = today
        return start_date, end_date

    else:
        return None, None


@api.get('/news/top-journalists', tags=['news'])
async def get_top_journalists(
                              section: Annotated[str, Query()],
                              time_scale: Annotated[str, Query()],
                              username: str = Depends(get_current_user)
                             ) -> elasticResponse:
    """Returns top 10 journalist for a section / period filter
        It returns 10 journalists who have published most articles
    \f
    Args:
        section (str): Name of the section used in filter clause
        time_scale (str): Time scale used in the filter clause
            values can be : "yesterday", "week_ago" or "month_ago"
        username: Used username for authentication

    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """

    start_date, end_date = get_time_scale(time_scale=time_scale)

    query_body = {
        "query":
            {
                "bool":
                    {
                        "filter":
                            [
                                {
                                    "term":
                                    {
                                        "section": section
                                    }
                                },
                                {
                                    "range":
                                        {
                                            "first_published_date":
                                                {
                                                    "gte": start_date,
                                                    "lte": end_date
                                                }
                                        }
                                }
                            ]
                        }
            },
            "size": 0,
            "aggs": {
                "articles_per_author":
                    {
                        "terms":
                            {
                                "field": "byline.keyword",
                                "size": 10
                            }
                    }
                }
    }

    start_date, end_date = get_time_scale(time_scale=time_scale)

    result = await es.search(index="news", body=query_body)
    result = json.dumps(result["aggregations"]["articles_per_author"]["buckets"])

    return elasticResponse(data=result)


@api.get('/news/top-persons', tags=['news'])
async def get_top_persons(
                          section: Annotated[str, Query()],
                          time_scale: Annotated[str, Query()],
                          username: str = Depends(get_current_user)
                          ) -> elasticResponse:
    """Returns top 5 persons for a section / period filter
        It returns 5 most represented persons on per_facet facet
    \f
    Args:
        section (str): Name of the section used in filter clause
        time_scale (str): Time scale used in the filter clause
            values can be : "yesterday", "week_ago" or "month_ago"
        username: Used username for authentication

    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """
    start_date, end_date = get_time_scale(time_scale=time_scale)

    query_body = {
        "query": {
            "bool":
                {
                    "filter":
                        [
                            {
                                "term":
                                {
                                    "section": section
                                }
                            },
                            {
                                "range":
                                    {
                                        "first_published_date":
                                            {
                                                "gte": start_date,
                                                "lte": end_date
                                            }
                                    }
                            }
                        ]
                }
            },
        "size": 0,
        "aggs":
            {
                "persons":
                    {
                        "terms":
                            {
                                "field": "per_facet",
                                "size": 5
                            }
                    }
            }
    }

    result = await es.search(index="news", body=query_body)
    result = json.dumps(result["aggregations"]["persons"]["buckets"])

    return elasticResponse(data=result)


@api.get('/news/articles-count', tags=['news'])
async def get_articles_count(
                             section: Annotated[str, Query()],
                             step: Annotated[str, Query()],
                             username: str = Depends(get_current_user)
                            ) -> elasticResponse:
    """Returns artciles count for a section / time scale step parameter
        step parameter can be "day", "month", "quarter", "year"
        \f

    Args:
        section (str): Name of the section used in filter clause
        step (str): Step used in calendar_interval aggregation clause
            values can be "day", "month", "quarter", "year"
        username: Used username for authentication

    Returns:
       elasticResponse : Object that embebeds elasticsearch response
    """

    query_body = {
        "query":
            {
                "bool":
                    {
                        "filter":
                            [
                                {
                                    "term":
                                    {
                                        "section": section
                                    }
                                }
                            ]
                    }
            },
        "size": 0,
        "aggs":
            {
                "articles_over_time":
                    {
                        "date_histogram":
                            {
                                "field": "first_published_date",
                                "calendar_interval": step
                            }
                    }
            }
    }

    result = await es.search(index="news", body=query_body)
    result = json.dumps(result["aggregations"]["articles_over_time"]["buckets"])

    return elasticResponse(data=result)


@api.get('/news/sections-proportions', tags=['news'])
async def get_sections_proportions(
                                    time_scale: Annotated[str, Query()],
                                    username: str = Depends(get_current_user)
                                  ) -> elasticResponse:
    """Returns Published articles proportions by sections for a given time scale
    \f

    Args:
        time_scale (str): Time scale used in the filter clause
            values can be : "yesterday", "week_ago" or "month_ago"
        username: Used username for authentication

    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """

    start_date, end_date = get_time_scale(time_scale=time_scale)

    query_body = {
        "query": {
            "bool":
                {
                    "filter":
                        [
                            {
                                "range":
                                    {
                                        "first_published_date":
                                            {
                                                "gte": start_date,
                                                "lte": end_date
                                            }
                                    }
                            }
                        ]
                }
        },
        "size": 0,
        "aggs":
            {
                "articles_per_section":
                    {
                        "terms":
                            {
                                "field": "section",
                                "size": 10
                            }
                    }
            }
    }

    result = await es.search(index="news", body=query_body)
    result = json.dumps(result["aggregations"]["articles_per_section"]["buckets"])

    return elasticResponse(data=result)


@api.get('/news/top-topics', tags=['news'])
async def get_top_topics(
                         section: Annotated[str, Query()],
                         time_scale: Annotated[str, Query()],
                         username: str = Depends(get_current_user)
                        ) -> elasticResponse:
    """Returns top 5 topics for a section / period filter
        It returns 5 most represented  on des_facet facet
    \f

    Args:
        section (str): Name of the section used in filter clause
        time_scale (str): Time scale used in the filter clause
            values can be : "yesterday", "week_ago" or "month_ago"
        username: Used username for authentication

    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """

    start_date, end_date = get_time_scale(time_scale=time_scale)

    query_body = {
        "query":
            {
                "bool":
                    {
                        "filter":
                            [
                                {
                                    "term":
                                    {
                                        "section": section
                                    }
                                },
                                {
                                    "range":
                                        {
                                            "first_published_date":
                                                {
                                                    "gte": start_date,
                                                    "lte": end_date
                                                }
                                        }
                                }
                            ]
                    }
            },
        "size": 0,
        "aggs":
            {
                "description_facet":
                    {
                        "terms":
                            {
                                "field": "des_facet",
                                "size": 5
                            }
                    }
            }
    }

    result = await es.search(index="news", body=query_body)
    result = json.dumps(result["aggregations"]["description_facet"]["buckets"])

    return elasticResponse(data=result)


@api.get('/books/top-writers', tags=['books'])
async def get_top_writers(
                          size: Annotated[int, Query()] = 15,
                          username: str = Depends(get_current_user)
                         ) -> elasticResponse:
    """Returns top writers in terms of books that are in best sellers lists
    \f

    Args:
        size (int): Number of top writers to retrieve
        username: Used username for authentication

    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """
    query_body = {
        "size": 0,
        "aggs":
            {
                "per_author":
                {
                    "terms":
                    {
                        "field": "author.keyword",
                        "size": size
                    }
                }
            }
        }

    result = await es.search(index="books", body=query_body)
    result = json.dumps(result["aggregations"]["per_author"]["buckets"])

    return elasticResponse(data=result)


@api.get('/books/count-by-lists', tags=['books'])
async def get_count_by_lists(
                             size: Annotated[int, Query()] = 59,
                             username: str = Depends(get_current_user)
                             ) -> elasticResponse:
    """Returns number of books by lists
    \f

    Args:
        size (int): Number of lists with mowt books to return
            default value il 59 (number of lists provided by New York Times)
        username: Used username for authentication
    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """
    query_body = {
        "size": 0,
        "aggs":
            {
                "ranks_history":
                    {
                        "nested":
                            {
                                "path": "ranks_history"
                            },
                        "aggs":
                            {
                                "per_list":
                                {
                                    "terms":
                                    {
                                        "field": "ranks_history.list_name.keyword",
                                        "size": size
                                    }
                                }
                            }
                    }
            }
        }

    result = await es.search(index="books", body=query_body)
    result = json.dumps(result["aggregations"]["ranks_history"]["per_list"]["buckets"])

    return elasticResponse(data=result)


@api.get('/books/top-writers-by-lists', tags=['books'])
async def get_top_writers_by_list(
                                  list: Annotated[str, Query()],
                                  size: Annotated[int, Query()] = 10,
                                  username: str = Depends(get_current_user)
                                 ) -> elasticResponse:
    """Returns top writers for a selected lists
    \f

    Args:
        list (str): Name of the list to retrieve top writers
        size (int): Number of top writers to retrieve
        username: Used username for authentication

    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """

    query_body = {
        "query":
            {
                "bool":
                {
                    "filter":
                        [
                            {
                                "nested":
                                    {
                                        "path": "ranks_history",
                                        "query":
                                            [
                                                {
                                                    "match":
                                                        {
                                                            "ranks_history.list_name": list
                                                        }
                                                }
                                            ]
                                    }
                            }
                        ]
                }
            },
        "size": 0,
        "aggs":
            {
                "authors_per_list":
                {
                    "terms":
                    {
                        "field": "author.keyword",
                        "size": f"{size}"
                    }
                }
            }
        }

    result = await es.search(index="books", body=query_body)
    result = json.dumps(result["aggregations"]["authors_per_list"]["buckets"])

    return elasticResponse(data=result)


@api.get('/books/top-publishers', tags=['books'])
async def get_top_publishers(
                              size: Annotated[int, Query()] = 15,
                              username: str = Depends(get_current_user)
                            ) -> elasticResponse:

    """Returns top publisher
        regarding how many of there books are in Best sellers lists
        \f

    Args:
        size (int): Number of top writers to retrieve
        username: Used username for authentication


    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """

    query_body = {
                    "size": 0,
                    "aggs":
                    {
                        "per_publisher":
                        {
                            "terms":
                                {
                                    "field": "publisher.keyword",
                                    "size": size
                                }
                        }
                    }
                }

    result = await es.search(index="books", body=query_body)
    result = json.dumps(result["aggregations"]["per_publisher"]["buckets"])

    return elasticResponse(data=result)


@api.get('/movies/count-per-year', tags=['movies'])
async def get_count_per_year(
                             username: str = Depends(get_current_user)
                            ) -> elasticResponse:
    """Returns number of movies reviens per year
    \f

    Returns:
        elasticResponse : Object that embebeds elasticsearch response
        username: Used username for authentication
    """

    query_body = {
        "size": 0,
        "aggs":
            {
                "reviews_by_year":
                    {
                        "date_histogram":
                            {
                                "field": "publication_date",
                                "calendar_interval": "year",
                                "format": "yyyy"
                            }
                        }
            }
        }
    result = await es.search(index="movies", body=query_body)
    result = json.dumps(result["aggregations"]["reviews_by_year"]["buckets"])

    return elasticResponse(data=result)


@api.get('/movies/top-reviwers', tags=["movies"])
async def get_top_reviewers(
                             year: Annotated[int, Query()],
                             username: str = Depends(get_current_user)
                            ) -> elasticResponse:
    """Returns top reviewers per year
        Means reviewers with most reviewes in database
    \f

    Args:
        year: Selected year to filter data
        username: Used username for authentication

    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """

    query_body = {
        "size": 0,
        "query":
            {
                "bool":
                    {
                        "filter":
                            [
                                {
                                    "range":
                                        {
                                            "publication_date":
                                                {
                                                    "gte": f"{year}-01-01",
                                                    "lte": f"{year}-12-31"
                                                }
                                        }
                                }
                            ]
                    }
            },
        "aggs":
            {
                "top_journalists":
                    {
                        "terms":
                            {
                                "field": "byline.keyword", "size": 5
                            }
                    }
            }
    }

    result = await es.search(index="movies", body=query_body)
    result = json.dumps(result["aggregations"]["top_journalists"]["buckets"])

    return elasticResponse(data=result)


@api.get('/movies/top-mpaa-rating', tags=["movies"])
async def get_top_mpaa_ratings(
                                username: str = Depends(get_current_user)
                              ) -> elasticResponse:
    """Returns top 5 MPAA rating categories all time
    \f

    Args:
        username: Used username for authentication

    Returns:
        elasticResponse : Object that embebeds elasticsearch response
    """

    query_body = {
        "size": 0,
        "query":
            {
                "bool":
                    {
                        "must_not":
                            [
                                {
                                    "terms":
                                        {
                                            "mpaa_rating":
                                                [
                                                    "",
                                                    "Unrated",
                                                    "Not Rated"
                                                ]
                                        }
                                }
                            ]
                    }
            },
        "aggs":
            {
                "films_by_mpaa_rating":
                    {
                        "terms":
                            {
                                "field": "mpaa_rating",
                                "size": 5
                            }
                    }
            }
    }
    result = await es.search(index="movies", body=query_body)
    result = json.dumps(result["aggregations"]["films_by_mpaa_rating"]["buckets"])

    return elasticResponse(data=result)

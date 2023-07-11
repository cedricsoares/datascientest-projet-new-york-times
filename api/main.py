from pydantic import BaseModel
from fastapi import FastAPI
from elasticsearch import AsyncElasticsearch
from datetime import date, timedelta
from typing import Optional
import json
import asyncio


api = FastAPI()
es = AsyncElasticsearch(hosts="http://@localhost:9200")


class elasticResponse(BaseModel):
    data: str


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


@api.get('/news/top-journalists')
async def get_top_journalists(section: str, time_scale: str) -> elasticResponse:
    """Returns top 10 journalist for a section / period filter
        It returns 10 journalists who have published most articles

    Args:
        section (str): Name of the section used in filter clause
        time_scale (str): Time scale used in the filter clause
            values can be : "yesterday", "week_ago" or "month_ago"
    Returns:
        Item : Object that embebeds elasticsearch response 
    """

    start_date, end_date = get_time_scale(time_scale=time_scale)

    query_body = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "term":
                        {
                            "section": f"{section}"
                        }
                    },
                    {
                        "range":
                            {
                                "first_published_date":
                                    {
                                        "gte": f"{start_date}",
                                        "lte": f"{end_date}"
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


@api.get('/news/top-persons')
async def get_top_persons(section: str, time_scale: str) -> elasticResponse:
    """Returns top 5 persons for a section / period filter
        It returns 5 most represented persons on per_facet facet
    
    Args:
        section (str): Name of the section used in filter clause
        time_scale (str): Time scale used in the filter clause
            values can be : "yesterday", "week_ago" or "month_ago"
    Returns:
        Item : Object that embebeds elasticsearch response
    """
    start_date, end_date = get_time_scale(time_scale=time_scale)

    query_body = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "term":
                        {
                            "section": f"{section}"
                        }
                    },
                    {
                        "range":
                            {
                                "first_published_date":
                                    {
                                        "gte": f"{start_date}",
                                        "lte": f"{end_date}"
                                    }
                            }
                    }
                ]
            }
        },
        "size": 0,
        "aggs": {
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


@api.get('/news/articles-count')
async def get_articles_count(section: str, step: str) -> elasticResponse:
    """Returns artciles count for a section / time scale step parameter
        step parameter can be "day", "month", "quarter", "year"

    Args:
        section (str): Name of the section used in filter clause
        step (str): Step used in calendar_interval aggregation clause
            values can be "day", "month", "quarter", "year"
    Returns:
        Item : Object that embebeds elasticsearch response
    """

    query_body = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "term":
                        {
                            "section": f"{section}"
                        }
                    }
                ]
            }
        },
        "size": 0,
        "aggs": {
            "articles_over_time":
                {
                    "date_histogram":
                        {
                            "field": "first_published_date",
                            "calendar_interval": f"{step}"
                        }
                }
            }
    }

    result = await es.search(index="news", body=query_body)
    result = json.dumps(result["aggregations"]["articles_over_time"]["buckets"])   

    return elasticResponse(data=result)


@api.get('/news/sections-proportions')
async def get_sections_proportions(time_scale: str) -> elasticResponse:
    """Returns Published articles proportions by sections for a given time scale

    Args:
        time_scale (str): Time scale used in the filter clause
            values can be : "yesterday", "week_ago" or "month_ago"
    Returns:
        Item : Object that embebeds elasticsearch response
    """

    start_date, end_date = get_time_scale(time_scale=time_scale)

    query_body = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "range":
                            {
                                "first_published_date":
                                    {
                                        "gte": f"{start_date}",
                                        "lte": f"{end_date}"
                                    }
                            }
                    }
                ]
            }
        },
        "size": 0,
        "aggs": {
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


@api.get('/news/top-topics')
async def get_top_topics(section: str, time_scale: str)  -> elasticResponse:
    """Returns top 5 topics for a section / period filter
        It returns 5 most represented  on des_facet facet

    Args:
        section (str): Name of the section used in filter clause
        time_scale (str): Time scale used in the filter clause
            values can be : "yesterday", "week_ago" or "month_ago"
    Returns:
        Item : Object that embebeds elasticsearch response
    """

    start_date, end_date = get_time_scale(time_scale=time_scale)

    query_body = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "term":
                        {
                            "section": f"{section}"
                        }
                    },
                    {
                        "range":
                            {
                                "first_published_date":
                                    {
                                        "gte": f"{start_date}",
                                        "lte": f"{end_date}"
                                    }
                            }
                    }
                ]
            }
        },
        "size": 0,
        "aggs": {
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


@api.get('/books/top-writers')
async def get_top_writers(size: int) -> elasticResponse:
    """Returns top writers in terms of books that are in best sellers lists
    
    Args:
        size (int): Number of top writers to retrieve
    Returns:
        Item : Object that embebeds elasticsearch response
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
                        "size": f"{size}"
                    }
                }
            }
        }

    result = await es.search(index="books", body=query_body)
    result = json.dumps(result["aggregations"]["per_author"]["buckets"])

    return elasticResponse(data=result)


@api.get('/books/count-by-lists')
async def get_count_by_lists(size: int=59) -> elasticResponse:
    """Returns number of books by lists

    Args:
        size (int): Number of lists with mowt books to return
            default value il 59 (number of lists provided by New York Times)
    Returns:
        Item : Object that embebeds elasticsearch response
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
                                        "size": f"{size}"
                                    }
                                }
                            }
                    }
            }
        }

    result = await es.search(index="books", body=query_body)
    result = json.dumps(result["aggregations"]["ranks_history"]["per_list"]["buckets"])

    return elasticResponse(data=result)


@api.get('/books/top-writers-by-lists')
async def get_top_writers_by_list(list: str, size: int) -> elasticResponse:
    """Returns top writers for a selected lists 
    
    Args:
        list (str): Name of the list to retrieve top writers
        size (int): NUmber of top writers to retrieve
    Returns:
        Item : Object that embebeds elasticsearch response
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
                                                            "ranks_history.list_name": f"{list}"
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

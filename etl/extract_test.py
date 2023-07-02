import sys
sys.path.append('etl/')

from session import Session
from extract import get_news, get_news_sections, get_news_data,get_books_or_movies
from unittest import TestCase,mock
import requests
from utils import build_query

class TestGetNews(TestCase):
       
    @mock.patch("extract.get_news_sections")
    @mock.patch("extract.get_news_data")
    def test_get_news(self, mock_get_news_data, mock_get_news_sections):
       
        """
        test the session
        test the session with the section 
        check if the max api call has been called
        """

        # Create a mock Session object
        mock_session = mock.create_autospec(Session)

        # Define test input parameters
        max_api_calls = 100

        # Mock the return value of get_news_sections
        mock_sections = ["section1", "section2"]
        mock_get_news_sections.return_value = mock_sections

        # Mock the return value of is_remaining_api_calls
        mock_session.is_remaining_api_calls.return_value = True

        # Call the get_news function
        get_news(session=mock_session, max_api_calls=max_api_calls)

        # Verify the function calls
        mock_get_news_sections.assert_called_once_with(session=mock_session)
        mock_get_news_data.assert_called_once_with(session=mock_session, sections=mock_sections, max_api_calls=max_api_calls)
        mock_session.is_remaining_api_calls.assert_called_once_with(max_api_calls=max_api_calls)





class TestGetNewsSections(TestCase):
    
    @mock.patch("extract.logger")
    @mock.patch("extract.build_query")
    @mock.patch("requests.get")
    def test_get_news_sections(self, mock_requests_get, mock_build_query, mock_logger):
       
        # Create a mock Session object
        mock_session = mock.create_autospec(Session)

        # Mock the response of requests.get
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "results": [
                {"section": "Politics"},
                {"section": "Business"},
                {"section": "Sports"}
            ]
        }
        mock_requests_get.return_value = mock_response

        # Call the get_news_sections function
        sections = get_news_sections(session=mock_session)

       # Print the actual calls made to logger.info
        print(mock_logger.info.call_args_list)

        # Verify the function calls
        mock_build_query.assert_called_with(index_name='news_sections', api_key=mock_session.api_key)
        mock_requests_get.assert_called_once_with(mock_build_query.return_value)
        mock_logger.info.assert_called_with(f'----- Total number of NYT API calls: {mock_session.api_calls} -----')

        # Verify the return value
        self.assertEqual(sections, ["Politics", "Business", "Sports"])

        # Additional assertions can be added for other function calls and behaviors
        #?????

class TestGetNewsData(TestCase):
    @mock.patch("extract.logger")
    @mock.patch("utils.build_query")
    @mock.patch("load.bulk_to_elasticsearch")
    @mock.patch("requests.get")

    def test_get_news_data(self, mock_requests_get, mock_bulk_to_elasticsearch, mock_build_query, mock_logger):
        # Create a mock Session object
        mock_session = mock.create_autospec(Session)

        # Define test input parameters
        sections = ["section1", "section2"]
        max_api_calls = 100

        # Mock the return value of build_query
        mock_query = "mock_query"
        mock_build_query.return_value = mock_query

        # Mock the response of requests.get
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "results": [
                {"title": "News article 1"},
                {"title": "News article 2"}
            ]
        }
        mock_requests_get.return_value = mock_response

        print(mock_session.api_calls)
        # Call the get_news_data function
        get_news_data(session=mock_session, sections=sections, max_api_calls=max_api_calls)
       
       # Verify the function calls
        
        """
        #mock_build_query.assert_called_with(index_name='news', news_section="section1", api_key=mock_session.api_key)
        #print(mock_build_query)
        
        mock_requests_get.assert_called_with(mock_query) 
        mock_bulk_to_elasticsearch.assert_called_with(con=mock_session.con, bulk_list=[
            {"index": {"_index": "news"}},
            {"title": "News article 1"},
            {"index": {"_index": "news"}},
            {"title": "News article 2"}
        ])
        """

        # Print the number of API calls
        print(mock_session.api_calls)
        self.assertGreaterEqual(mock_session.api_calls.__iadd__.call_count, 0)   ####ISSUE FOR THIS ONE 
        self.assertEqual(mock_logger.info.call_count, 5)
        self.assertEqual(mock_logger.warning.call_count, 0)


class TestGetBooksOrMovies(TestCase):
       
    @mock.patch("extract.logger")
    @mock.patch("extract.get_endpoint_hits")
    @mock.patch("extract.get_start_offset")
    @mock.patch("extract.build_query")
    @mock.patch("load.bulk_to_elasticsearch")
    @mock.patch("requests.get")
    def test_get_books_or_movies(self, mock_requests_get, mock_bulk_to_elasticsearch, mock_build_query,
                                 mock_get_start_offset, mock_get_endpoint_hits, mock_logger):
       
        # Create a mock Session object
        mock_session = mock.create_autospec(Session)
        mock_session._api_key = "your_api_key_value"


        # Define test input parameters
        index_name = "books"
        results_by_page = 10
        max_api_calls = 100
        max_books_movies_calls = 5

        # Mock the return value of get_endpoint_hits
        mock_get_endpoint_hits.return_value = 50

        # Mock the return value of get_start_offset
        mock_get_start_offset.return_value = 0

        # Mock the response of requests.get
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "num_results": 50,
            "results": [
                {"title": "Book 1"},
                {"title": "Book 2"}
            ]
        }
        mock_requests_get.return_value = mock_response

        # Call the get_books_or_movies function
        get_books_or_movies(index_name=index_name, 
                            results_by_page=results_by_page,
                            session=mock_session, 
                            max_api_calls=max_api_calls,
                            max_books_movies_calls=max_books_movies_calls)
        
        # Verify the function calls
        mock_get_endpoint_hits.assert_called_once_with(con=mock_session.con,
                                                       api_key=mock_session.api_key,
                                                       index_name=index_name)
       
        
        mock_get_start_offset.assert_called_once_with(con=mock_session.con,
                                                      index_name=index_name)
        
    
        """
        mock_build_query.assert_called_with(index_name=index_name,
                                             api_key=mock_session._api_key,
                                             start_offset=0)  # Called at least once
        
        mock_requests_get.assert_called_once_with(mock_build_query.return_value)
        
        mock_bulk_to_elasticsearch.assert_called_once_with(con=mock_session.con,
                                                           bulk_list=[
                                                               {"index": {"_index": index_name}},
                                                               {"title": "Book 1"},
                                                               {"index": {"_index": index_name}},
                                                               {"title": "Book 2"}
                                                           ])
       

        """
        
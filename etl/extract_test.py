import sys
sys.path.append('etl/')

from session import Session
from extract import get_news, get_news_sections, get_news_data
from unittest import TestCase,mock


class TestGetNews(TestCase):
       
       @mock.patch("extract.get_news_sections")
       @mock.patch("extract.get_news_data")
       def test_get_news(self, mock_get_news_data, mock_get_news_sections):
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
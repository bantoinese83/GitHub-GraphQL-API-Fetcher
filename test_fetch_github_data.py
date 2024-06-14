import unittest
from unittest.mock import patch, Mock
import os

from requests import RequestException

from fetch_github_data import execute_github_graphql_query, handle_github_graphql_response


class TestGithubDataFetcher(unittest.TestCase):
    @patch('requests.post')
    def test_execute_github_graphql_query(self, mock_post):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        url = 'https://api.github.com/graphql'
        headers = {
            'Authorization': f"Bearer {os.getenv('GITHUB_TOKEN')}",
            'Content-Type': 'application/json',
        }
        query = '{ viewer { login } }'

        response = execute_github_graphql_query(url, headers, query)

        self.assertEqual(response, mock_response)

    @patch('fetch_github_data.PrettyTable')
    @patch('fetch_github_data.logger')
    def test_handle_github_graphql_response(self, mock_logger, mock_table):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'viewer': {
                    'login': 'test',
                    'repositories': {
                        'nodes': []
                    }
                }
            }
        }

        handle_github_graphql_response(mock_response)

        mock_logger.info.assert_called()
        mock_table.assert_called()

    @patch('fetch_github_data.logger')
    def test_handle_github_graphql_response_error(self, mock_logger):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'

        handle_github_graphql_response(mock_response)

        mock_logger.error.assert_called()

    @patch('requests.post')
    def test_execute_github_graphql_query_error(self, mock_post):
        mock_response = Mock()
        mock_post.return_value = mock_response
        mock_response.raise_for_status.side_effect = RequestException('An error occurred')

        url = 'https://api.github.com/graphql'
        headers = {
            'Authorization': f"Bearer {os.getenv('GITHUB_TOKEN')}",
            'Content-Type': 'application/json',
        }
        query = '{ viewer { login } }'

        response = execute_github_graphql_query(url, headers, query)

        self.assertIsNone(response)

    @patch('fetch_github_data.logger')
    def test_handle_github_graphql_response_non_200_status(self, mock_logger):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'

        handle_github_graphql_response(mock_response)

        mock_logger.error.assert_called()

    @patch('requests.post')
    def test_execute_github_graphql_query_request_exception(self, mock_post):
        mock_post.side_effect = RequestException('An error occurred')

        url = 'https://api.github.com/graphql'
        headers = {
            'Authorization': f"Bearer {os.getenv('GITHUB_TOKEN')}",
            'Content-Type': 'application/json',
        }
        query = '{ viewer { login } }'

        response = execute_github_graphql_query(url, headers, query)

        self.assertIsNone(response)

    @patch('fetch_github_data.logger')
    def test_handle_github_graphql_response_request_exception(self, mock_logger):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'

        handle_github_graphql_response(mock_response)

        mock_logger.error.assert_called()


if __name__ == '__main__':
    unittest.main()

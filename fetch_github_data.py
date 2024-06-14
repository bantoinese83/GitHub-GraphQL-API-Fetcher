import os

import requests
from dotenv import load_dotenv
from loguru import logger
from prettytable import PrettyTable
from requests.exceptions import RequestException

# Load environment variables from a .env file
load_dotenv()

# Define the GraphQL endpoint URL
GRAPHQL_URL = 'https://api.github.com/graphql'

# Your GitHub Personal Access Token
auth_headers = {
    'Authorization': f"Bearer {os.getenv('GITHUB_TOKEN')}",
    'Content-Type': 'application/json',
}

# GraphQL query string
graphql_query = '''
{
  viewer {
    login
    repositories(first: 20, orderBy: {field: CREATED_AT, direction: DESC}) {
      nodes {
        name
        createdAt
        description
        stargazerCount
        forkCount
        watchers {
          totalCount
        }
        issues {
          totalCount
        }
        pullRequests {
          totalCount
        }
      }
    }
  }
}
'''


def execute_github_graphql_query(url, headers, query):
    """
    execute a GitHub GraphQL query and return the response.

    Args:
        url (str): The GraphQL endpoint URL.
        headers (dict): The headers to include in the request.
        query (str): The GraphQL query to execute.

    Returns:
        response (requests.Response): The response from the server.
    """
    try:
        response = requests.post(url, headers=headers, json={'query': query})
        response.raise_for_status()
    except RequestException as e:
        logger.error(f"Request failed due to an error. {e}")
        return None  # Return None when an exception is raised
    return response


def handle_github_graphql_response(response):
    """
    Handle the response from a GitHub GraphQL query.

    Args:
        response (requests.Response): The response from the server.

    Returns:
        None
    """
    if response is not None:
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Create a PrettyTable instance
            table = PrettyTable()

            # Define the table columns
            table.field_names = ["Name", "Created At", "Description", "Stars", "Forks", "Watchers", "Issues",
                                 "Pull Requests"]

            # Add rows to the table
            for node in data['data']['viewer']['repositories']['nodes']:
                table.add_row([
                    node['name'],
                    node['createdAt'],
                    node['description'],
                    node['stargazerCount'],
                    node['forkCount'],
                    node['watchers']['totalCount'],
                    node['issues']['totalCount'],
                    node['pullRequests']['totalCount']
                ])

            # Print the table
            logger.info("\n" + str(table))
        else:
            logger.error(f"Request failed with status code {response.status_code}")
            logger.error(response.text)


github_response = execute_github_graphql_query(GRAPHQL_URL, auth_headers, graphql_query)
handle_github_graphql_response(github_response)

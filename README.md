# GitHub GraphQL API Fetcher

This project is a Python application that fetches data from the GitHub GraphQL API. It retrieves information about a user's repositories, including the name, creation date, description, star count, fork count, watcher count, issue count, and pull request count.

## Installation

Before running the application, you need to install the required Python packages. You can do this by running the following command:

```bash
pip install -r requirements.txt
```

## Usage

To run the application, you need to create a .env file in the root directory of the project and set the `GITHUB_TOKEN
` You can create a personal access token by following the instructions [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

After setting the `GITHUB_TOKEN` environment variable, you can run the application by executing the following command:

```bash
python fetch_github_data.py
```

## Tests
This project includes a suite of unit tests. You can run the tests with the following command:

```bash
coverage run -m unittest test_fetch_github_data.py
```

You can view the test coverage report by running the following command:
```bash
coverage html
```

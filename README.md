Clone this repo to work on pytest hands-on. Associated blog post: https://krupahebbar.substack.com/p/pytest-with-python-from-beginner-to-expert-aeb1152c2981

The project contains a simple FastAPI app and a few helper methods, along with test cases for all of them.

### Install dependencies

Create a virtualenv and install from requirements.txt
```commandline
python3 -m venv pytest_examples_venv
source pytest_examples_venv/bin/activate
pip install -r requirements.txt
```
(or use anaconda or any package manager of your choice with the given requirements.txt)

### Run the test suite

To run the test suite in verbose mode, run the following command from project root:
```commandline
python -m pytest -vv .
```
_Note: Running pytest as a python module handles some import-related issues that could come up_ 

### Check test coverage

To check test coverage, run the following command from project root:
```commandline
coverage run -m pytest .
coverage report  # to display coverage summary
```

To create htmlcov/ folder with navigable html files to see details of coverage within each file, run
```commandline
coverage html
```
and then open htmlcov/index.html in your browser.

### Run the application locally
Note: to run the actual fastapi server, you will need to have redis-server running on your system, and you can run this command from the repository root: 
```commandline
python -m app.server
```

The API docs page will then be visible at http://localhost:19999/docs

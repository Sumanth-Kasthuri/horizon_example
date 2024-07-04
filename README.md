# horizon_restaurants

I recommend using PyCharm for this project. It is free for students and has a lot of useful features. You can download it [here](https://www.jetbrains.com/pycharm/).

1. Use Python 3.11
2. Setup a virtual environment
```
python -m venv venv
```
3. Activate the virtual environment
```
source venv/bin/activate (macOS)
venv\Scripts\activate (Windows)
```
4. Install the pip requirements
```
pip install -r requirements.txt
```

If you get stuck with any of these steps, message me.

## Branch Strategy

When you are writing your code, please create a new branch and push your code to that branch. When you are done, create a pull request to merge your branch to the main branch. Please do not merge your branch to the main branch directly. I will then review the pull request and suggest changes or approve it for merging into main.

Branch naming convention: `<your name>/<feature>`

If you aren't familiar with git, please read this [tutorial](https://www.atlassian.com/git/tutorials/what-is-git) first.

## Migrating the Database

When you make changes to the database models, you need to migrate the database. To do this, run the following commands:
```
alembic revision -m "<message>"
alembic upgrade head
```

## Writing Code

When you are writing functions, please insert comments to show who wrote the code. For example:
```
def my_function():
    """
    Author: <your name>
    Student ID: <your student ID>
    """
    # Code goes here
```

If your entire file is written by you, you can add the comment at the top of the file. For example:
```
"""
Author: <your name>
Student ID: <your student ID>
"""
```

## Adding New Packages

If you need to add a new package to the project, please add it to the requirements.txt file. To do this, run the following command:
```
pipreqs --savepath=requirements.in && pip-compile
```

## Running the Project

To run the project, run main.py in the root directory. To do this, run the following command:
```
python main.py
```

## Testing

To run the tests, run the following command:
```
python -m unittest discover tests
```
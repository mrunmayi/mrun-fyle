# Fyle Backend Challenge

## Who is this for?

This challenge is meant for candidates who wish to be part of Fyle's engineering team specializing in backend.

## Why work at Fyle?

Fyle is a fast-growing Expense Management SaaS product. We are ~40 strong engineering team at the moment. 

We are an extremely transparent organization. Check out our [careers page](https://careers.fylehq.com) that will give you a glimpse of what it is like to work at Fyle. Also, check out our Glassdoor reviews [here](https://www.glassdoor.co.in/Reviews/Fyle-Reviews-E1723235.htm). You can read stories from our teammates [here](https://stories.fylehq.com).

## Challenge outline

This challenge involves writing a backend service for a classroom. The challenge is described in detail [here](./Application.md).

## What happens next?

You will hear back within 48 hours from us via email. 

## Installation

1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### Install requirements

```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```

### Reset DB
```
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/
```

### Start Server
```
bash run.sh
```

### Run Tests
```
pytest -vvv -s tests/

# for test coverage report
# pytest --cov
# open htmlcov/index.html
```

### To Run the test in Docker when cant run on local
```
1. fork the main repo.
2. install docker-desktop.
3. Create loging if not present.
4. setup Dev environments in docker desktop to point to your forked repo.
5. This will create a docker with the Debian GNU image with your github code in the root folder.
6. This give options to open docker code into your local editor. Open in IDE and update the code, run the test until ready.
7. push to forked github repository or building a docker image with the changes in the docker.
8. Share it with the team
```
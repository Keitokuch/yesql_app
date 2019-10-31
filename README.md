# yesql_app
Web Journal Recommender. FA19 CS411 project of group YeSQL

## Deployment instructions

First make sure that you have python3 and pip3 installed.

Next, install virtualenv if you haven't
```
$ pip3 install virtualenv
```

In project folder, run
```
$ virtualenv -p python3 venv
```
to initialize python virtual environment.

Activate virtual environment with:
```
$ source ./venv/bin/activate
```

Install required modules in venv
```
(venv)$ pip install -r requirements.txt
```
App is ready to run:
```
(venv)$ python app.py
```
Visit `http://127.0.0.1:5000` to view it locally.

## Unit testing

Run:
```sh
(venv)$ python -m unittest test.mysql
```

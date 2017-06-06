# Osper Technical Test

## Introduction

Web Service to provide compliance check of loaded money.

The following instruction have only been executed on Mac OS X.

## Requisites

The following software is needed to install and execute this application:

* [git][git] to access the code from github
* Python 2.6 to execute the application
* [virtualenv][virtualenv] to create an isolated development sandbox.
* [curl][curl] to run API calls from CLI

## Setting Up
### Getting the code

[git] has been used as the source control for this project and the canonical repository is held by the github service. To access this project correctly:

````sh
git clone git@github.com:mat-green/osper.git
cd osper
````

### Create A Python Virtual Environment
We deploy this application into it's own virtual environment therefore you will
need to do the same. Install & Activate the virtualenv (this assumes you are in
the root of the application folder using a cli):
```
easy_install virtualenv
mkdir ~/.virtualenvs
cd ~/.virtualenvs
virtualenv osper
source ~/.virtualenvs/osper/bin/activate
```

### Install Python Packages
This assumes you are in the osper folder:
````sh
pip install -r requirements.txt
pip install -r requirements-for-tests.txt
````

### Application Configuration
Copy the contents of `example.env` into a new file named `.env` and fill in your Braintree API credentials. Credentials can be found by navigating to Account > My User > View Authorizations in the Braintree Control Panel. Full instructions can be [found on our support site](https://articles.braintreepayments.com/control-panel/important-gateway-credentials#api-credentials).

### Start server
```sh
python osper.py
```

Check it executes by opening http://127.0.0.1:5000/token within a browser.

## Running tests

Unit tests do not make API calls to Braintree and do not require Braintree credentials. You can run this project's unit tests by calling `python test_app.py` on the command line.



[curl]: https://curl.haxx.se/
[git]: http://git-scm.com/
[virtualenv]: http://pypi.python.org/pypi/virtualenv

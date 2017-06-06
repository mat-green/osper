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

````
git clone git@github.com:mat-green/osper.git
cd osper
````

### Create A Python Virtual Environment
We deploy this application into it's own virtual environment therefore you will
need to do the same. Install & Activate the virtualenv (this assumes you are in
the root of the application folder using a cli):

        easy_install virtualenv
        mkdir ~/.virtualenvs
        cd ~/.virtualenvs
        virtualenv osper
        source ~/.virtualenvs/osper/bin/activate

### Install Python Packages
This assumes you are in the osper folder:
````
pip install -r requirements.txt
pip install -r requirements-for-tests.txt
````


[curl]: https://curl.haxx.se/
[git]: http://git-scm.com/
[virtualenv]: http://pypi.python.org/pypi/virtualenv

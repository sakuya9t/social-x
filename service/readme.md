# Social-X Backend

## Requirement

In the Dev environment, python 3.6.8 is installed.

To check python version, run:

``python3 --version``

If using Ubuntu 18.04, then the default python version is 3.6.8

If using Ubuntu 16.04, update the python version following: http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/

To install required libraries, run:

``pipenv run python3 -m pip install -r requirements.txt``

or

``pipenv run pip3 install -r requirements.txt``


## Troubleshoot

### python3 version in pipenv is not 3.6.8

Make sure the system python version is 3.6.8, then run:

``pipenv --rm``

``pipenv install``

to re-create the pipenv.

### pycurl install failed

If install pycurl failed, run:

``sudo apt install libcurl4-openssl-dev libssl-dev``

then try again.

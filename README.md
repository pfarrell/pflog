# Pflog
## A Foto Blog generator

Pflog (will build on the simple concept of using email as an input interface for a system.
Yes, I know this idea for this application is like "beating a dead horse".  That's part of
its name.

The basic idea is that pflog will exist in two parts

An agent that will:
1. monitor an email address for new messages
1. an email is parsed to extract 
  * video, photo, documents, any MIME type
  * information from the sender, subject and message body
1. information can be stored in some datastore (say SQLite or even git)

A classic website to display the uploaded info

## Getting Started

### Set up environment
This project is built on Python3, uses Sqlite for storage, and assumes agent
email address is hosted on gmail.  

These instructions should get you up and running, but certainly can be 
modified if you know what you're doing.

For Ubuntu/Debian, use apt to install 
* `libmagickwand-dev`
* `python3-opencv`

Smartcrop is using an unreleased version which is not in pip.  To install you should
`pip install git+https://github.com/epixelic/python-smart-crop`

Before you begin, you should set up a new gmail email address, enable IMAP support, 
enable 2FA, and generate an application password for pflog. 
As of 2022, this seems to be the best way to connect to gmail from a 3rd party app.

#### Clone project and change to root directory
```
git clone git@github.com/pfarrell/pflog.git 
cd pflog
export PYTHONPATH=$(pwd)
```
#### Set up a virtual environment, activate, and install project requirements
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.py
```
#### Initialize Database
```
./bin/init.sh
```
This script will prompt you for the agent's email address credentials and store them 
in a sqlite database created in the project's root directory

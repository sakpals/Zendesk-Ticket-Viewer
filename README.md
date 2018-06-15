# Zendesk-Ticket-Viewer
This app allows users to view a ticket list and individual ticket descriptions of the available tickets on my Zendesk account. 

## Getting Started
These instructions will allow you to run the app locally on your local machine. This app has not been deployed on a live system.

### Prerequisites
You will require the following software:
```
Python 3.6.5
pip 3
```

### Installing
It is recommended to set up a python virtual environment to isloate the environment required to run this project.


#### OSX:


Install virtualenv:
```
pip3 install virtualenv
```


Create virtualenv:
```
virtualenv -p python3 <desired-path>
```


Activate virtualenv:
```
source <desired-path>/bin/activate
```


Deactivate (do this after installing packages from requirements.txt):
```
deactivate
```


#### Windows:



Install virtualenv:
```
pip3 install virtualenv
```


Create virtualenv:
```
virtualenv <desired-path>
```


Activate virtualenv:
```
path\to\<desired-path>\Scripts\activate


e.g. C:\Users\'Username'\venv\Scripts\activate.bat
```


Deactivate (do this after installing packages from requirements.txt):
```
path\to\<desired-path>\Scripts\deactivate
```

-------------------------------------------------------------------------------
Install package requirements:
```
pip3 install -r requirements.txt
```


### Usage
Run the (Flask) server for the app from the command line:
```
python3 run.py
```


Navigate to the URL specified:
 ```
 http://127.0.0.1:5000/
```

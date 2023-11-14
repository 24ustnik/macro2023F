# Main Readme for the Test full Flask Application (ZOTE)

**NOTE**: this should be in a fresh workspace just for this flask application.
If you did not use a new workspace, create a new one now and re-do the
steps to set this up.

This is a skeleton for an entire flask application that can be
run locally on your own computer.

To set up the flask application, we need to do a few things first:

* Set up a python virtual environment (aka "venv")
* set venv for python workspace
* activate the venv in VSCode
* install all the requirements
* run flask locally
* test the flask app

## VENV
to set up a new virtual environment, use

    python -m venv venv.flask

(the "venv.flask" is the name of your flask application)
**NOTE:** if during the venv creation, VSCode asks you if you want
to make the venv your workspace venv b/c it detected Python, then
choose "YES".  If you do this, you can skip the SET WORKSPACE VENV step.


## SET WORKSPACE VENV
**NOTE:** if during the venv creation, VSCode asks you if you want
to make the venv your workspace venv b/c it detected Python, then
choose "YES".  If you do this, you can skip this step b/c it is already done.

we also want to set the venv.flask as the python environment for our 
workspace.  You should open one of the python files and then in 
the lower right, where it shows the python version (eg., "3.11.5"), click 
it.  Then interpreter path and find the following dir:
    
    venv.flask\Scripts\python.exe

## ACTIVATE VENV
activate the venv

    venv.flask\Scripts\Activate.bat

and your prompt should now show

**(venv.flask)** at the front of it.  
This means you are working in the venv.


## REQUIREMENTS
to install the requirements, make sure your venv.flask is activated
and then use:

    pip install -r requirements.txt

Python should install all the required libraries that are listed in
the requirements.txt file

## FLASK RUN
Once all the libraries are installed, we can run our flask skeleton
(it doesn't do much).

to run flask: (configs are in the .flaskenv file)

    flask run

and you should see some output like :

 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 339-587-679


## TEST FLASK
to test the app, point your browser to :
   http://localhost:5001/root/

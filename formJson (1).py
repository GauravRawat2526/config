import os
import socket
import datetime
import sys
import re
import time
import requests
import types
import subprocess
import json
# to use dotenv , firstly execute this command: pip install python-dotenv
#from dotenv import load_dotenv

if __name__=="__main__":
    # the below function will load the evn variables that you have defined in env file on your system



# now we are defining the remaining evn variables, we cannot define these variables on .env file
# because here we have to use join method which is used only in python, so we have to define them
    # here


    #Values

#    LOGDIR = os.path.join(os.getenv("SRCDIR"), 'logs')
    #load_dotenv()

    # Now you can access the environment variables just like regular variables
    srcdir_value = r"C:\Users\ngaur\PycharmProjects\flex-erd-mstr-envbuild\envBuild\src\env_build"
    os.environ["SRCDIR"]=srcdir_value
    os.environ["LOCALHOST"]="127.0.0.1"

    # Get the name of the current script
    SCRIPT = os.path.basename(__file__)

    # Get the current date and time in the format 'YYYYMMDDHHMMSS'
    DATE = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    LOGDIR = os.path.join(os.environ["SRCDIR"], 'logs')

    # Create the log file name using the script name and the current date
    LOG = os.path.join(LOGDIR, f'{SCRIPT}_{DATE}.log')

    # Get the hostname of the machine
    HOSTNAME = socket.gethostname()

    # Extract the short hostname (without domain) from the full hostname
    SHORT_HOSTNAME = HOSTNAME.split('.')[0]

    # Set the path to a properties file
    PREREQS_FILE = os.path.join(os.environ["SRCDIR"], 'properties', 'pre_reqs.properties')

    # Set the path to the working directory
    WORKDIR = os.path.join(os.environ["SRCDIR"], 'work')

    # Set the path to the etc directory
    ETCDIR = os.path.join(os.environ["SRCDIR"], 'etc')

    # Set the path to a properties file
    MSTR_PROPERTIES_FILE = os.path.join(os.environ["SRCDIR"], 'properties', 'mstr.properties')

    # Set the path to another properties file
    ISSERVER_PROPERTIES_FILE = os.path.join(os.environ["SRCDIR"], 'properties', 'iserver-build-env.properties')

    # Set a flag indicating whether to log to STDOUT (standard output)
    LogToSTDOUT = False

    # Project Source Name
    LOCALHOST_PROJECT_SOURCE = os.environ["LOCALHOST"]

    # Cookie file for curl requests
    COOKIE_JAR = os.path.join(WORKDIR, 'cookieJar')


    class RecursiveNamespace(types.SimpleNamespace):
        def __init__(self, mapping):
            super().__init__(**{
                key: RecursiveNamespace(value) if isinstance(value, dict) else value
                for key, value in mapping.items()
            })

    # found multiple values of cluster.lead.host taken from n1
    my_dict = {
        "mstr": {"install": {"dir": "/opt/product/mstr/install"}, "home": {"dir": "/opt/product/mstr/home"},
                 "cluster": {"lead": {"host": "mstrapn1w1.paychex.com"}}},
        "isserver": {"admin": {"pswd": {
            "envbuild": "{TOTEM-ENCRYPTED}AAAAAQAAAAh8mp/YkqeAqgAAABBe5TmQjsUWSoqXz18OORPSAAAAsDKScFfe6A3ujyh8nMaagZE1B42KFaXbCKdIOEm0CyOM+/KnSuFYi3ahGPf+73zT9Ef0ahRFKqFlgJr9rIkKdwKB6a6mEtbpJkIBBh0hIl/KJm9KeyARf6Z+cZ8+39tzpohAYhNtT0Nl1ymeN7LunX44ym0mLt4vJspADjfc9G3AxQgNAR9QrX1WjNBEhxjWqRqtzNvTJ39eMG5KDdD2itFTbDj5rOKF1O9EjrOAYl1d"}}},
        "web": {"tier": {"tomcat": {"home": "/opt/appl/erd/mstr/tomcat"}}}
    }

    dict_obj = RecursiveNamespace(my_dict)
    mstr = dict_obj.mstr
    isserver = dict_obj.isserver
    web = dict_obj.web

    # Convert to a dictionary that can be serialized to JSON
    serializable_data = {
        "mstr": mstr.__dict__,
        "isserver": isserver.__dict__,
        "web": web.__dict__
    }

    # Code or functions taken from separate files
    # MicroStrategy Install
    MSTR_INSTALL_DIR = mstr.install.dir

    WEB_TOMCAT_HOME = web.tier.tomcat.home

    # MicroStrategy Java Home
    MSTR_JAVA_HOME = os.path.join(MSTR_INSTALL_DIR, '_jre')

    ISSERVER_ADMIN_PSWD = isserver.admin.pswd.envbuild

    applyConfigOutFile = os.path.join(WORKDIR, 'createRoles.out')

    # MicroStrategy Home
    MSTR_HOME_DIR = mstr.home.dir

    CLUSTER_LEAD_HOSTNAME = mstr.cluster.lead.host

    MSTR_SR_PORT = 8301

    MSTR_TS_PORT = 8443

    MSTR_RS_PORT = 6379

    MSTR_KS_PORT = 9092

    MSTR_ZS_PORT = 2181


    data={
        "SCRIPT": SCRIPT,
        "DATE":DATE,
        "LOGDIR":LOGDIR,
        "LOG":LOG,
        "HOSTNAME":HOSTNAME,
        "SHORT_HOSTNAME":SHORT_HOSTNAME,
        "PREREQS_FILE": PREREQS_FILE,
        "WORKDIR":WORKDIR,
        "ETCDIR":ETCDIR,
        "MSTR_PROPERTIES_FILE":MSTR_PROPERTIES_FILE,
        "ISSERVER_PROPERTIES_FILE":ISSERVER_PROPERTIES_FILE,
        "ISSERVER_ADMIN_PSWD":ISSERVER_ADMIN_PSWD,
        "LogToSTDOUT":LogToSTDOUT,
        "LOCALHOST_PROJECT_SOURCE":LOCALHOST_PROJECT_SOURCE,
        "COOKIE_JAR":COOKIE_JAR,
        "MSTR_INSTALL_DIR":MSTR_INSTALL_DIR,
        "WEB_TOMCAT_HOME":WEB_TOMCAT_HOME,
        "MSTR_JAVA_HOME":MSTR_JAVA_HOME,
        "ISSERVER_ADMIN_PSWD":ISSERVER_ADMIN_PSWD,
        "applyConfigOutFile":applyConfigOutFile,
        "MSTR_HOME_DIR":MSTR_HOME_DIR,
        "CLUSTER_LEAD_HOSTNAME":CLUSTER_LEAD_HOSTNAME,
        "MSTR_SR_PORT":MSTR_SR_PORT,
        "MSTR_TS_PORT": MSTR_TS_PORT,
        "MSTR_RS_PORT" : MSTR_RS_PORT,
        "MSTR_KS_PORT" : MSTR_KS_PORT,
        "MSTR_ZS_PORT" : MSTR_ZS_PORT
    }


    with open("config_commonFuncs.json","w") as config_file:
        json.dump(data,config_file,indent=4)


    print("Success")


# OMC-Dyn-Integration
This repository outlines a solution demo utilizing Oracle Management Cloud &amp; Dyn Web Application Firewall Logs. The solution leverages Log Analytics &amp; Security Monitoring and Analytics to give increased insight into perimeter and interior activity.

### Disclaimer
The following is intended to outline our general product direction. It is intended for information purposes only, and may not be incorporated into any contract. It is not a commitment to deliver any material, code, or functionality, and should not be relied upon in making purchasing decisions. The development, release, and timing of any features or functionality described for Oracle’s products remains at the sole discretion of Oracle.

### Lab Overview
The lab exercises in this guide will show you how to utilize Oracle Management Cloud to Ingest Web Application Firewall Logs, visualize them, and create custom dashboards based off the data to give insight into perimeter activity. It will also demonstrate how to configure Security Monitoring & Analytics Cloud Service (SMACS) to detect potential security incidents and threats based off internal user activity.

Upon Completion of this lab, you will be able to:
* Install a cloud agent on a linux box
* Ingest log data into Log Analytics
* Configure and create custom log sources and parsers
* Visualize log data & Create Custom Dashboards
* Configure SMACS to detect potential Security Events

### Lab Prerequisites
To perform this lab you will need:
* Access to this git repo and associated log data.
* An Oracle Infrastructure Tenancy
* An Oracle Management Cloud Tenancy
* A text editor (e.g. Atom, Sublime, etc)

## Lab 1: Installing a Cloud Agent on a Linux Box
Navigate to [Cloud Login Page](https://cloud.oracle.com/home)  and log in with your credentials. Click the navigation menu in the upper left and select "Compute > Instances > Create Intance." Name the Instance, select the AD (AD1 if possible) and select instance type (VM). Pair your SSH key with the instance. if you do not already have an ssh key you can generate one from the command line by running ```ssh-keygen```. Select the appropriate compartment, VCN and subnet. You may need to configure these if you have not already done so. Click "Create."
![1.)](/assets/pic1.png?raw=true)
![1.)](/assets/pic2.png?raw=true)
![1.)](/assets/pic3.png?raw=true)
![1.)](/assets/pic4.png?raw=true)
![1.)](/assets/pic5.png?raw=true)

When the instance is fully provisioned it will appear green in your console. Select the instance and copy the public IP Address. You will need this for the next portion of the lab.
![1.)](/assets/pic6.png?raw=true)
![1.)](/assets/pic7.png?raw=true)

## Lab 2: Installing a Cloud Agent on your Linux Box
Log in to your Oracle Management Cloud Tenancy. Select "Administration > Agents."
![1.)](/assets/pic8.png?raw=true)
![1.)](/assets/pic9.png?raw=true)

Select "Download" and under Agent Type select "Cloud Agent." Download the Cloud Agent- Linux (64 Bit). Additionally make sure to copy the tenant name and OMC_URL as you will need them later.
![1.)](/assets/pic10.png?raw=true)

Select the "Registration Keys" tab. If there are no current registration keys create one and then copy the key value.
![1.)](/assets/pic11.png?raw=true)

Navigate to your terminal. from the main directory cd into the ssh directory using the command ``` cd .ssh```. From this directory run the following command ```ssh -i YOUR_KEY_NAME opc@PUBLIC_IP_OF_INSTANCE```.


## Lab 3: Cleaning of Web Application Firewall Data
Open terminal (or your OS' command line) and clone this repo by running the following command: ```git clone https://github.com/dbrett90/OMC-Dyn-Integration.git```. Make sure that you are not on a corporate network as it will interfere with the cloning process. 

Navigate to logFiles > dyn_newest_logs.csv and inspect the data. You will notice a number of fields included that will not be relevant for data visualization and a number of fields that need to be standardized for OMC's parsers. Specifically we will be updating the timestamp to be in POSIX format and removing columns 6, 11, & 17. 

Navigate to the python scripts directory. Feel free to inspect masterClean.py, which contains all the methods necessary to clean the Dyn Data. When finished, run ```python masterClean.py``` from your command line. The file we will be using is dyn_data_final.csv. You may ignore all the other log files created. Make sure you know where this file is saved as we will need access to it later.

## Lab 4: Configuring Log Parsers & Sources  

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

Navigate to your terminal. from the main directory cd into the ssh directory using the command ``` cd .ssh```. From this directory run the following command ```scp -i YOUR_KEY /Path/To/Cloud/Agent  opc@PUBLIC_IP_OF_INSTANCE:/home/opc/```. This will copy the cloud agent  onto your linux box.
![1.)](/assets/pic12.png?raw=true)

After the cloudagent has been successfully copied over we will need to ssh into the actual box. Run ```ssh -i YOUR_KEY opc@PUBLIC_IP_OF_INSTANCE```. run a ```ls``` command (bash) or ```dir``` (windows) and make sure you are in the same directory as your zipped cloud agent. By default this directory is ```/home/opc```. Unzip the agent by running ```unzip NAME_OF_CLOUD_AGENT_ZIP```.  
![1.)](/assets/pic13.png?raw=true)

You now need to provide the cloud agent with some information. Access the agent.rsp file from the command line by running ```vim agent.rsp```. Provide the Tenant Name, Agent Registration Key and OMC URL you copied down earlier. For agent base directory use ```/home/opc/agent```. Make sure the file is updated.
![1.)](/assets/pic14.png?raw=true)

Run ```./AgentInstall.sh```. You can confirm that the agent is up and running by navigating to the bin folder (```cd agent/agent_inst/bin```) and running ```./omcli status agent```.
![1.)](/assets/pic15.png?raw=true)

You can also confirm that the agent is active from the OMC console by navigating to Administration > Agents > Cloud Agents. An active agent will have a green arrow.
![1.)](/assets/pic16.png?raw=true)

You have now successfully configured a cloud agent for your linux box.


## Lab 3: Cleaning of Web Application Firewall Data
Open terminal (or your OS' command line) and clone this repo by running the following command: ```git clone https://github.com/dbrett90/OMC-Dyn-Integration.git```. Make sure that you are not on a corporate network as it will interfere with the cloning process.

Navigate to logFiles > dyn_newest_logs.csv and inspect the data. You will notice a number of fields included that will not be relevant for data visualization and a number of fields that need to be standardized for OMC's parsers. Specifically we will be updating the timestamp to be in POSIX format and removing columns 6, 11, & 17.

Navigate to the python scripts directory. Feel free to inspect masterClean.py, which contains all the methods necessary to clean the Dyn Data. When finished, run ```python masterClean.py``` from your command line. When prompted for column deletions enter 6,11, and 17 respectively. For length enter 501. For timestamps enter 1. The file we will be using is dyn_data_final.csv. You may ignore all the other log files created. Make sure you know where this file is saved as we will need access to it later.

## Lab 4: Configuring Log Parsers & Sources  

Navigate back to your OMC console. Select Administration > Log Admin > Fields. We will be creating a log parser for the data, but first need to specify a few custom fields contained in our Dyn WAF Logs which do not come prepackaged with OMC.
![1.)](/assets/pic17.png?raw=true)

If you open up the WAF Log file (in texteditor, **NOT** in Excel) you will see a number of fields that we need to create. These include WAF Alerts, Request URL, Referrer, Response Code, Response Size & Fingerprint. We will need to make custom fields for each of these. Simply click the create button, name the field and add the type (typically string). A description is optional. Click '"Save."
![1.)](/assets/pic18.png?raw=true)

Once you have created all necessary custom fields, click the log parsers tab. Select "Create". Name the parser and paste one line from the log file (from text editor, **NOT** Excel as Excel won't copy as comma-delimited) into the example log content block. Select "Next". Highlight the entire block and click "Next."
![1.)](/assets/pic19.png?raw=true)

Highlight each field and match with the corresponding field. Make sure that each field passes the parser test (will highlight green if successful). For timestamp make sure this is in POSIX format. Click create when done.
![1.)](/assets/pic20.png?raw=true)

In the OMC Console go to Log Sources > Create.
![1.)](/assets/pic21.png?raw=true)

Name the parser and leave the source type as "file." Select "Cloud Agent" as entity type and the name of the parser you created under file parser. For included patterns if you have the Dyn Logs on your linux box (could use a ```scp``` command) you will need to give the parser the filepath (EX: ```/home/opc/dynLogs/*.csv```) and either name the file or give it a generic ```*.csv``` extension. If you have these logs stored on your local host the next lab will explain how to upload those files directly into OMC. Make sure you click save to enable the log Source.
![1.)](/assets/pic22.png?raw=true)




## Lab 5: Uploading Data & Creating Dashboards

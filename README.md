# OMC-Dyn-Integration
This repository outlines a solution demo utilizing Oracle Management Cloud &amp; Dyn Web Application Firewall Logs. The solution leverages Log Analytics &amp; Security Monitoring and Analytics to give increased insight into perimeter and interior activity.

### Disclaimer
The following is intended to outline our general product direction. It is intended for information purposes only, and may not be incorporated into any contract. It is not a commitment to deliver any material, code, or functionality, and should not be relied upon in making purchasing decisions. The development, release, and timing of any features or functionality described for Oracle’s products remains at the sole discretion of Oracle.

### Lab Overview
The lab exercises in this guide will show you how to utilize Oracle Management Cloud to Ingest Web Application Firewall Logs, visualize them, and create custom dashboards based off the data to give insight into perimeter activity. It will also demonstrwate how to configure Security Monitoring & Analytics Cloud Service (SMACS) to detect potential security incidents and threats based off internal user activity.

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

# Table of Contents
* [Lab 1: Creating Your Linux Server](https://github.com/dbrett90/OMC-Dyn-Integration#lab-1-creating-your-linux-server)
* [Lab 2: Installing a Cloud Agent on your Linux Box](https://github.com/dbrett90/OMC-Dyn-Integration#lab-2-installing-a-cloud-agent-on-your-linux-box)
* [Lab 3: Cleaning of Web Application Firewall Data](https://github.com/dbrett90/OMC-Dyn-Integration#lab-3-cleaning-of-web-application-firewall-data)
* [Lab 4: Configuring Log Parsers & Sources](https://github.com/dbrett90/OMC-Dyn-Integration#lab-4-configuring-log-parsers--sources)
* [Lab 5: Uploading Data & Creating Dashboards](https://github.com/dbrett90/OMC-Dyn-Integration#lab-5-uploading-data--creating-dashboards)
* [Lab 6: Configuring Security Monitoring & Analytics](https://github.com/dbrett90/OMC-Dyn-Integration#lab-6-configuring-security-monitoring--analytics)


## Lab 1: Creating Your Linux Server
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

Highlight each field and match with the corresponding field. Make sure that each field passes the parser test (will highlight green if successful). For timestamp make sure this is in POSIX format. Click next when done and create the parser.
![1.)](/assets/pic20.png?raw=true)

In the OMC Console go to Log Sources > Create.
![1.)](/assets/pic21.png?raw=true)

Name the parser and leave the source type as "file." Select "Cloud Agent" as entity type and the name of the parser you created under file parser. For included patterns if you have the Dyn Logs on your linux box (could use a ```scp``` command) you will need to give the parser the filepath (EX: ```/home/opc/dynLogs/*.csv```) and either name the file or give it a generic ```*.csv``` extension. If you have these logs stored on your local host the next lab will explain how to upload those files directly into OMC. Make sure you click save to enable the log Source.
![1.)](/assets/pic22.png?raw=true)


## Lab 5: Uploading Data & Creating Dashboards

If you have not securely copied the Dyn log file to your compute node, you can manually upload it into OMC. Navigate to `Log Admin` > `Uploads` > `New Upload`.
![1.)](/assets/pic23.png?raw=true)

Name the Upload, select the files from your browser and click the `>` button. Now make sure to associate the upload with the log source you just created and the entity with your cloud agent. Click the > button. Review and Upload.
![1.)](/assets/pic24.png?raw=true)

On the uploads page click the hamburger menu next to your upload and select "View in Log Explorer."
![1.)](/assets/pic25.png?raw=true)

If the log parser was correctly configured you should be able to click into a given record and see the information in human readable form. If done incorrectly there will be a blue "i" next to the entry.
![1.)](/assets/pic26.png?raw=true)

We can now start creating visualizations. Change the graph on the visualization option and drag the field (from the other dropdown) into the "Group By" box. Click "Save > Save As."
![1.)](/assets/pic27.png?raw=true)

Name the graphic, select "Add to Dashboard" and choose the "New Dashboard" option. Name the Dashboard and click save. Continue making and adding graphics to this dashboard until you are satisfied with visuals.
![1.)](/assets/pic28.png?raw=true)

View your dashboards by going Home > Dashboards. You can move visuals around by pressing the edit button.
![1.)](/assets/pic29.png?raw=true)
![1.)](/assets/pic30.png?raw=true)

## Lab 6: Configuring Security Monitoring & Analytics

Security Monitoring and Analytics can be configured for any given piece of Cloud Infrastructure, but this will also require specific configuration of identity context. To speed the process up we will upload our own custom log files to demonstrate a number of specific threats that will also showcase identity context.

First, Navigate to `Menu Icon` > `Home` > `Administration` > `Entities Configuration` > `Licensing`. Click on each licensing configuration to match the below screenshot (i.e. Log Collection = Enabled, SMA Enrichment = Enabled, Assignment = Enterprise + Config & Compliance)
![1.)](/assets/pic31.png?raw=true)

ssh into your linux box. Create the Create the directory `/u01/stage`. Copy the zipped [SMA data](logFiles/smaData/sma-sample.zip) to `/u01/stage` and unzip the file.

In addition to log data, sample user context data will be added to OMC as well to provide a richer experience by mapping users identified in security logs to detailed corporate directory sourced from the company’s Identity Service. In real production setting, this data will come from an Identity Service such as IDCS and by means of integration.

In your linux host session, navigate to /u01/stage
1.	From [My Cloud Services Dashboard](https://myservices.us2.oraclecloud.com/mycloud/cloudportal/dashboard), toggle "Identity Domain" selector to your "Traditional" domain, then click on `Management Cloud` as shown below

	![1.)](/assets/pic32.png?raw=true)

1.	Get the Tenant ID, OMC Service Instance Name, and OMC Username as shown below

	![1.)](/assets/pic33.png?raw=true)

1. 	Using the items gathered above, update environment variables accordingly as shown in this example
```
export tenantID=acmeinc			#Tenant ID
export instanceName=ops			#OMC Service Instance Name
export username=John.Doe@gmail.com	#OMC Username
```
3.	Execute the Unix shell script `omc_upload_usr_context.sh` and type in your OMC account password when prompted to upload User context file

```
[cdsma@myhost]$ ./omc_upload_usr_context.sh
```

For the benefit of this lab, you will be uploading sample Linux Secure logs files to OMC covering the following 3 security threats types:

   - `Target Account Attack `
   - `Multiple Failed Login `
   - `Brute Force Attack `

In real production setting, this data will be continuously streamed to OMC by OMC cloud agents and API integration. SMA supports uploading user data available in SCIM or LDIF format. The former will be used.

1.	From the same Linux host as indicated earlier and still with the environment variables set, run the Unix shell script `omc_upload_security_events.sh` to upload Linux secure logs.

```
[cdsma@myhost]$ ./omc_upload_security_events.sh
```


Once you have successfully uploaded the three log files, navigate back to the Uploads page. Refresh the page to see your uploaded log files. If you go to the Security Monitoring & Analytics page you should now be able to see potential threats.

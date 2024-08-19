Setting up BBX
==============
BBX and Rey may be set up as follows; more specific instructions are provided in each tool's repository. Please note that some steps (e.g., setting up an elastic search database) have excellent documentation, which will simply be referenced.

Assumptions
-----------
The following instructions assume `sysmon <https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon>`_ event logging for windows hosts, a frequent use case. BBX comes configured with a set of alert rules which query windows sysmon logs. Many other types of logging (e.g., powershell scriptblock) can also be done; BBX simply needs a set of alert rules appropriate for such logs. Logs from other types of hosts (e.g., linux) can be processed similarly. BBX also assumes event logs are stored in an Elasticsearch database. However, a modular layer of code can be replaced so as to query another log database (e.g., Splunk) instead.

Steps
-----

1. Install sysmon on each Windows Host and Begin Logging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Decide which windows hosts you want to log, and install sysmon on those hosts. Numerous online help sites and video tutorials exist (search on "install and configure sysmon"). The high level procedure is:

- Download `sysmon <https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon>`_ from microsoft.
- Extract the .zip file, run the .exe file as administrator
- Download and install a sysmon configuration file, such as the popular `SwiftOnSecurity <https://github.com/SwiftOnSecurity/sysmon-config>`_ config.

Sysmon configuration is crucial because it filters out many irrelevant events, significantly decreasing log volume.

2. Setup an Elasticsearch Database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Several options exist, including installation on a local analysis host, cloud installation, and paying for a managed service. Instructions for a local elastic installation using a docker container are `here <https://www.elastic.co/guide/en/elasticsearch/reference/current/run-elasticsearch-locally.html>`_.

3. Setup Winlogbeat to Forward Host Logs to Elasticsearch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Winlogbeat is a log forwarding program. Winlogbeat should be installed, configured and run on each host being logged. Winlogbeat's general installation and configuration instructions are `here <https://www.elastic.co/guide/en/beats/winlogbeat/current/winlogbeat-installation-configuration.html>`_.

Note that you'll need to configure winlogbeat to look for sysmon logs in particular (using the configuration "winlogbeat.event_logs: - name: Microsoft-Windows-Sysmon/Operational").

You also need to configure winlogbeat to point to the elasticsearch database server you just set up, so a winlogbeat index will be created there to receive the host sysmon logs. `Here <https://www.elastic.co/guide/en/beats/winlogbeat/current/elasticsearch-output.html>`_ is a guide to designating the Elasticsearch database server.

3.5 Interlude
^^^^^^^^^^^^^

*Congratulations!* You should now have host-based sysmon events from your network showing up in the database on your analysis server. At this point, you can test the connections to make sure log data is being collected, generate suspicious activity on a host (e.g., using a tool like Caldera), and examine the resulting logs using kibana (part of the elastic installation).

`Here <https://medium.com/@concanno/how-to-hunt-on-sysmon-data-67f6661fd166>`_ is an excellent "threat hunting" article on the process so far (sysmon to winlogbeat to elastic) and using kibana to examine suspicious activity. Using BBX and Rey's condensed visual format will greatly simplify and enrich this process: providing more insight faster and requiring less cybersecurity skill and experience.

4. Install and Configure BBX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BBX queries the log events in the winlogbeat index of the elastic database, applies alert rules, and then generates Activity Set graphs as JSON files. Detailed BBX instructions describing this process (including code, documentation, install scripts, and command line options) are ==here==. However, here are the major steps involved:

- Install BBX. It is convenient, but not necessary, to install BBX on the same server as Elasticsearch.
- Configure BBX to query the elastic database containing the events.
- Configure BBX's rules as needed for events of local interest.
- Configure BBX's whitelisting to ignore commonly occurring activity.

5. Generate Activity Sets
^^^^^^^^^^^^^^^^^^^^^^^^^

In BBX, choose a location for generated Activity Set files (==how?==). Then begin BBX running. There are several BBX parameters that can be configured in an associated YAML file, including for example how frequently BBX queries the elastic database.

BBX generates two types of files:

1. xxx.json (where xxx is a long hash-like unique id)
2. xxx.meta.json

The file xxx.json contains the Activity Set itself (format described :ref:`here <activity_sets_section>`). The file xxx.meta.json contains useful summary metadata useful to Rey, or any analysis program, such as the start and stop times, a list of users and hosts involved, and a list of the detected ATT&CK `Techniques <https://attack.mitre.org/techniques/enterprise/>`_.
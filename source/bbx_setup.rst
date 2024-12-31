Setting up BBX
==============

Assumptions
-----------

The following instructions assume `Sysmon <https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon>`_ event logging for Windows hosts, a frequent use case. 
BBX comes configured with a set of alert rules which query Windows sysmon logs. Many other types of logging (e.g., Powershell Scriptblock) can also be done; 
BBX simply needs a set of ATT&CK-labeled alert rules appropriate for such logs. Logs from other types of hosts (e.g., Linux) and other sources (e.g., network PCAP) can be processed similarly,
given a set of alert rules.
BBX currently assumes event logs are stored in an Elasticsearch database. However, a modular layer of code can be replaced so as to query another log database (e.g., Splunk) instead.

Steps
-----

1. Install Sysmon on each Windows Host and Begin Logging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Decide which Windows hosts you want to log, and install Sysmon on those hosts. Numerous online help sites and video tutorials exist (search on "install and configure sysmon"). The high level procedure is:

- Download `Sysmon <https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon>`_ from Microsoft.
- Extract the .zip file, run the .exe file as administrator
- Download and install a Sysmon configuration file, such as the popular `SwiftOnSecurity <https://github.com/SwiftOnSecurity/sysmon-config>`_ config.

Sysmon configuration is crucial because it filters out many irrelevant events, significantly decreasing log volume.

2. Setup an Elasticsearch Database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Several options exist, including installation on a local analysis host, cloud installation, and paying for a managed service. Instructions for a local Elastic installation using a Docker container are `here <https://www.elastic.co/guide/en/elasticsearch/reference/current/run-elasticsearch-locally.html>`_.

3. Setup Winlogbeat to Forward Host Logs to Elasticsearch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Winlogbeat is the Elastic stack's log forwarder; it should be installed, configured and run on each host being logged. Winlogbeat's general installation and configuration instructions are `here <https://www.elastic.co/guide/en/beats/winlogbeat/current/winlogbeat-installation-configuration.html>`_.

Note that you'll need to configure Winlogbeat to look for Sysmon logs in particular (using the configuration "winlogbeat.event_logs: - name: Microsoft-Windows-Sysmon/Operational").
You also need to configure Winlogbeat `to point to <https://www.elastic.co/guide/en/beats/winlogbeat/current/elasticsearch-output.html>`_ 
the Elasticsearch database server you just set up, so a Winlogbeat index will be created there to receive the host Sysmon logs.

3.5 Interlude
^^^^^^^^^^^^^

You should now have host-based sysmon events from your network showing up in your log database.
At this point, you can test the connections to make sure log data is being collected, generate suspicious activity on a host (e.g., using a tool like Caldera),
and examine the resulting logs using Kibana (part of the Elastic installation).

`Here <https://medium.com/@concanno/how-to-hunt-on-sysmon-data-67f6661fd166>`_ is an excellent "threat hunting" article on the process so far (sysmon to Winlogbeat to Elastic)
and using Kibana to examine suspicious activity. 
BBX and Rey's condensed visual format and multi-dimensional structure (i.e., organizing events along causal chains, time, and TTP) will simplify and enrich this process significantly.

4. Install and Configure BBX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

BBX queries events in the Winlogbeat index of the Elastic database in order to test alert rules, and then generates Activity Set graphs as JSON files.
Detailed setup instructions are in the Blue Agave BBX repository.  However, here are the major steps:

- Install BBX. It is convenient, but not necessary, to install BBX on the same server as Elasticsearch.
- Configure BBX to query the elastic database containing the events. You can edit the ``default.yml`` file.
- Configure BBX's rules as needed for events of local interest. A default configuration is in ``cascade_rules.yml``
- Configure BBX's whitelisting to ignore commonly occurring activity. The file `whitelist_rules.yml` has default settings.

5. Generate Activity Sets
^^^^^^^^^^^^^^^^^^^^^^^^^

In BBX, choose a directory for generated Activity Set files using the `--activity-set-dir` (or short-form, `-a`) command line argument for `bbx.py`. Then start BBX.
Several parameters can be configured in an associated YAML file, including how frequently BBX queries the Elastic database. Point to your config file using the `--config`/`-c` flag; a sample config is available in `config/defulat.yml`. 

BBX generates two types of files:

1. ``xxx.json`` (where xxx is a long hash-like unique id)
2. ``xxx.meta.json``

The file ``xxx.json`` contains the Activity Set itself (format described :ref:`here <activity_sets_section>`). The file ``xxx.meta.json`` contains summary metadata useful to Rey,
or any analysis program, such as start and stop times, a list of users and hosts involved, and a list of the detected ATT&CK `Techniques <https://attack.mitre.org/techniques/enterprise/>`_.

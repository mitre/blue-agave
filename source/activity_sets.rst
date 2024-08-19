.. _activity_sets_section:

Activity Sets
=============

Activity Sets are a useful format for the analysis and visualization of cyber detection data. This article: 

1. Defines Activity Sets
2. Explains why they are important
3. Describes how they can be generated
4. Provides a data model

Definition
----------

An Activity Set is a graph-based causally-linked representation of presumed-malicious activity. Graph nodes are detected system events (represented in a data model such as `ECS <https://www.elastic.co/guide/en/ecs/current/ecs-reference.html>`_ or `CAR <https://car.mitre.org/data_model/>`_) and their associated ATT&CK-labeled alerts (e.g., representing the firing of detection rule in a SIEM). The directed edges represent causal relationships, such as parent-to-child process, process-to-flow, process-to-registry, process-to-file, process-to-process memory access. All nodes in an Activity Set are linked in a single (weakly) connected directed graph.

Importance & Utility
--------------------

Activity Set graphs can play several important roles:

1. **Bounded subspace for threat hunting:** The game board of cybersecurity can be thought of as a three-dimensional space involving time, hosts, and TTPs. Because there is so much of each dimension to search in a large operational network, it is valuable to have a scoping mechanism bounding this 3-space to a productive locus for analytic investigation / threat hunting (both manual and automated). An Activity Set A isolates an episode of adversary activity within exactly such a useful scope through a) A's time bounds T1 and T2, b) the set of hosts touched by the events belonging to A, c) the set of TTPs implicated by the triggered alerts in A.
2. **Useful object for human analysis.** As illustrated in the examples above, Activity Sets often “tell a story” of adversary activity when examined, such as TTP progression along the "kill chain", making them an insight-yielding visualization object.
3. **Automatic detection of malicious activity.** The semantically-rich features of an Activity Set graph (e.g., diversity of ATT&CK techniques, highest out degree of a node) can be used by a trained ML classifier to automatically distinguish malicious behavior from benign activity.
4. **Whitelisting benign activity.** Benign activity (e.g., software patching, boot sequence actions, security tool behaviors) can generate Activity Sets as well. Well-characterized benign Activity Sets can act as a unit of whitelisting.
5. **Compact representation:** Activity Sets are a compact way to represent adversary activity, because every event will appear at most once (see Generation below) and most non-adversarial events are omitted.
6. **Same-actor ID:** When multiple adversaries operate in a network simultaneously, it is highly likely a single Activity Set comprises the activity of a single actor/adversary (the exceptions are unusual cases, such as two adversaries injecting into the same 3rd party process).

Relationship to Other Formats
-----------------------------

Activity Sets are complementary to  `BSF <https://github.com/mitre/brawl-public-game-001?tab=readme-ov-file#brawl-shared-format>`_ and `Attack Flows <https://center-for-threat-informed-defense.github.io/attack-flow/>`_, time-ordered representations of malicious activity, emphasizing TTPs.

Activity Sets are similar to `provenance graphs <https://arxiv.org/pdf/2006.01722>`_; both are graphs of system level malicious activity. Activity Sets are event-centric: graph nodes are system events (e.g., process creation, network access). Provenance graphs are object centric: graph nodes are system objects (e.g., process, network port). This is an intentional decision, as Activity Sets are intended to improve on standard event-centric logs and their interfaces (such as `kibana <https://www.elastic.co/kibana>`_) by organizing kibana-style events into ATT&CK-labelled causally linked graphs, providing deeper insights and making them much easier to examine. A valuable future task would be transforming back and forth between Activity Sets and provenance graphs.

Generation
----------

Activity Sets can be generated as follows:

1. Pick a set of triggered analytic "alerts". This set can be delimited by a forensic or real-time time window (i.e., between times T1 and T2), and possibly some other criteria such as a type of alert.
2. "Investigate" each alert, forming individual alert graphs. Given an event E that triggers an analytic A, investigation builds a graph of all other system events reachable from E through causal relationships ("pivots"). The resulting directed alert graph will include: the initial triggered analytic A and its initiating event E, all events reachable via pivots, directed edges for each pivot, and potentially "second pass" alerts, as described in "more details" below. Given N alerts, this will result in N alert graphs. (These may stretch temporally beyond T1 and T2 due to investigation.)
3. The Activity Set(s) between T1 and T2 are the distinct connected components resulting from performing a set union on these N alert graphs. Specifically: 1) Where any two alert graphs share a common event, merge the two graphs so there is only one instance of each common event, all alerts on merged events have been combined, and the directed pivot relationships between events have been preserved. 2) Stop merging when every event is in a unique Activity Set graph.

More details:

- **Second pass alerts:** The recall of Investigation graphs can be improved by applying additional "second pass" (otherwise too-noisy) alert rules to generate further alerts. The presumed-malicious semantic context of the original alert reduces the false positive rate of these otherwise noisy alert rules, keeping precision at an acceptable level. 
- **Need for an event database.** Investigation necessitates access to a database of archived events (e.g., ElasticSearch, Splunk), because computing parent event pivots requires looking backward in time from the current event, and cannot be done by only looking at a real-time stream.
- **Truncating investigation toward the boot sequence:** If parent process pivots are followed all the way back to machine boot, every single event since boot, including a vast number of benign ones, will be joined into a single huge Activity Set. Such an Activity Set is not helpful for cyber analysis (although it is very instructive wrt operating system behavior!). Therefore, both a) whitelisting of the boot sequence, and b) a heuristic to truncate the investigation process as close as possible to the initial malicious implant and its alerts, are needed.
- **Efficiency:** The three step Activity Set generation process above is descriptive, however more efficient approaches exist. In particular, steps two and three can be merged saving a good bit of time.

Code:

- *Need a link to BBX repo ==here==.*

Activity Set Data Model
-----------------------

Activity Set Objects
^^^^^^^^^^^^^^^^^^^^

The following JSON data structure represents a single Activity Set. Each Activity Set contains:

a. An ID. (e.g. A hash of the timestamp of earliest event in this Activity Set.)
b. An array of event objects.
c. An array of edge (pivot) objects.
d. An array of "analytic result" (i.e. alert) objects.

.. code-block:: javascript
    :linenos:

    {
        "activity_set_id" : "xyz",
        "events" : [{Ev1}, ... {Evj}],
        "alerts" : [{A1}, ... {Ai}],
        "edges"  : [{Ed1}, ... {Edk}],
    }

Here are structures for individual event, edge, and alert objects. All fields are mandatory unless stated as "optional".

Event
^^^^^

Events follow the `CAR data model <https://car.mitre.org/data_model/>`_.

.. code-block:: javascript
    :linenos:

    {
        "event_id": "xyz",        // (Unique ID)
        "object": "xyz",          // (e.g. 'process')
        "action": "xyz",          // (e.g. 'create')
        "time": "xyz",            // (Time this event actually happened)
        "host": "xyz",            // (Host identifier for where this event happened)
        "user": "xyz",            // (Optional. User account responsible for this event)
        "process_guid": "xyz",    // (Optional. If a process is involved, a globally-unique process id)
        "other_event_fields": ... // (Optional. Other specific fields pertaining to this object and action, such as a file path or a ppid)
    }

Edge
^^^^

.. code-block:: javascript
    :linenos:

    {
        "edge_id": "xyz",    // (Unique ID)
        "src_event": "xyz",  // (Foreign key to an event which is the causal source)
        "dest_event": "xyz", // (Foreign key to an event which is the causal destination)
        "source": "xyz",     // (Optional. How this edge was determined: e.g., pivot, or inference)
        "confidence": 0.5    // (Optional. For inferred edges, e.g., via predicate logic, how sure we are)
    }

Analytic Result
^^^^^^^^^^^^^^^

.. code-block:: javascript
    :linenos:

    {
        "analytic_result_id": "xyz",  // (Unique ID)
        "analytic_id": "xyz",         // (A unique ID for the triggered analytic)
        "analytic_name": "xyz",       // (A human understandable name for the triggered analytic)
        "attack_technique_id": "xyz", // (An ATT&CK Technique ID that this analytic is attempting to detect, e.g., T1016)
        "attack_tactic": "xyz",       // (ATT&CK Tactic for this Technique, e.g., Discovery)
        "key_event": "xyz",           // (Foreign key to the event that triggered this alert)
        "source": "xyz",              // (Optional: The way this alert was generated: "first pass", "second pass")
        "alert_id": "xyz",            // (Optional: A unique ID for ????)
    }

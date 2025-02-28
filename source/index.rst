Blue Agave
==========

Blue Agave is an *ATT&CK Graph Analysis and Visualization Environment* (AGAVE) for defenders.
The vision of this project is to provide a powerful low-overhead
defensive cyber detection and analysis capability.

Blue Agave consists of two tightly coupled tools:  **BBX** and **Rey**.
BBX is a python application that detects suspicious activity on network hosts,
labels it with ATT&CK identifiers and organizes it into causal graphs called Activity
Sets which can be analyzed by humans or applications (e.g., classifiers).
Rey is a browser-based javascript application that allows a human user to explore
activity set graphs along the dimensions of time, causality, TTP, and network host.
Rey users can visualize high-level sequences of TTPs over time,
or drill down to study the fine-grained details of any event.

.. toctree::
   :maxdepth: 2
   :caption: Overview

   introduction
   demo

.. toctree::
   :maxdepth: 2
   :caption: Setup Guides
   
   bbx_setup
   rey_setup

.. toctree::
   :maxdepth: 2
   :caption: System Architecture

   activity_sets


Acknowledgements
----------------
We gratefully acknowledge MITRE Corporation IR&D funding 
provided by Dr. George Roelke and Dr. Stan Barr.

BBX development was led by Steven Gianvecchio; Rey development was led by Michael Carenzo.
Ken Smith was PI of the IR&D projects.
Activity sets are modeled on an idea from the `CASCADE <https://github.com/mitre/cascade-server/>`_
project led by Ross Wolf and Henry Foster.
Hongying Lan, Andrew Sillers, Alex Tsow and many others contributed significantly
to the research, development and testing of Blue Agave.


Notice
------

© |copyright_years| The MITRE Corporation. Approved for public release. Document number(s) |prs_numbers|.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

This project makes use of ATT&CK®: `ATT&CK Terms of Use
<https://attack.mitre.org/resources/legal-and-branding/terms-of-use/>`__



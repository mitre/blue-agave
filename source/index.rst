Blue Agave
==========

BBX and Rey are coupled open source tools that together provide a baseline cyber detection and analysis capability.
**BBX** is a python application that detects suspicious activity on network hosts, labels it with ATT&CK identifiers and organizes it into graphs called Activity Sets.
**Rey** is a browser-based javascript application that allows an analytic user to explore these graphs along the dimensions of time, causality, TTP, and network host.
Rey users can visualize high-level sequences of TTPs over time, or drill down to study fine-grained event-level details.

.. toctree::
   :maxdepth: 2
   :caption: Overview

   introduction

.. toctree::
   :maxdepth: 2
   :caption: Setup Guides
   
   bbx_setup
   rey_setup

.. toctree::
   :maxdepth: 2
   :caption: System Architecture

   activity_sets

Notice
------

© |copyright_years| The MITRE Corporation. Approved for public release. Document number(s) |prs_numbers|.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

This project makes use of ATT&CK®: `ATT&CK Terms of Use
<https://attack.mitre.org/resources/legal-and-branding/terms-of-use/>`__
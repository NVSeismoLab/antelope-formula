antelope-formula
================

Salt modules and states for BRTT Antelope software

Modules
-------
### antelope

Execution  module with the following commands
 * install - install Antelope from ISO or directory structure
 * update - run Antelope update command
 * run - run any Antelope command
 * is_updated - return whether uninstalled patches are available
 * is_installed - return whether a given version is installed
 * rtinit - run rtinit in a specified directory
 * rtexec (beta) - Start/stop control for rtexec (still flakey)


States
------
### antelope
State which satifies dependencies and installs the sofware using the command module. In future, could use a custom state.

### antelope.dependencies
State to install dependent packages for Antelope. For all OS's, there are packages needed by the installer itself, as well as packages and services needed to run the software.

### antelope.python
State to setup python for use with Antelope. For both system python and the version included with the software, this state properly adds the Antelope python modules to the path via the `sitecustomize.py` file. Also adds some static links to compiled libs used by the Antelope python version for cross-system support.

### antelope.pf.license
State to install the software license file, with keys from a pillar. See `pillar.example` for details.

### antelope.pf.site
State to install site.pf file from pillar info

### antelope.pf.rtexec
(Alpha) test state to deploy instances of rtexec, not fully implemented, may work better as a custom state.


License
-------
Copyright 2014 [Mark Williams](https://github.com/markcwill) at [Nevada Seismological Laboratory](http://www.seismo.unr.edu)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

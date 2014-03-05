#
# Salt state file for Antelope
#
# This could be written in python rather than jinja, but a better upgrade
# would be to write a state module using other states, or an execution
# module, which the state module then calls.
#
{% from "antelope/map.jinja" import antelope with context %}

##############################################################################
# 1) Install dependencies
#
# - per os, maybe have a 'standalone' one you can disable if you set up
#   separate states for things and break them out
include:
    - antelope.dependencies


##############################################################################
# 2) run an install command
# - Right now, call the execution function directly
# - ideally, this should be a state module which calls an execution module
#

run_installer:
    module.run:
        - func: antelope.install
        - source: {{ antelope.source }}
        - version: {{ antelope.version }}


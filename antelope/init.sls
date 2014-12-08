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
# - If source is a package URL, call pkg
# - Else assume source is ISO or directory of ISO mount, call module install
# - Right now, assumes ISO exists locally (copied or NFS access, e.g.)
#   (Could enforce this with file.managed in revision)
#
antelope_install:
{% if antelope.source.endswith('.deb') or antelope.source.endswith('.rpm') %}
  pkg.installed:
    - sources:
      - antelope: {{ antelope.source }}
{% else %}
  module.run:
    - name: antelope.install
    - source: {{ antelope.source }}
    - version: {{ antelope.version }}
{% endif %}

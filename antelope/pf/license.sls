#
# saltstack state to manage Antelope license files
#

{% from "antelope/map.jinja" import antelope with context %}

antelope_license:
    file:
        - managed
        - name: {{ antelope.install }}/{{ antelope.version }}/data/pf/license.pf
        - source: {{ antelope.files }}/license.pf
        - template: jinja
        - defaults:
            version: {{ antelope.version }}


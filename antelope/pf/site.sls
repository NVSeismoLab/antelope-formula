#
# saltstack state to manage Antelope license files
#

{% from "antelope/map.jinja" import antelope with context %}

antelope_site:
    file:
        - managed
        - name: {{ antelope.install }}/{{ antelope.version }}/data/pf/site.pf
        - source: {{ antelope.files }}/site.pf
        - template: jinja



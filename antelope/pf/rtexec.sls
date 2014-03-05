#
# saltstack state to manage Antelope rtexec files
#

{% from "antelope/map.jinja" import antelope with context %}

antelope_rtexec:
    file:
        - managed
        - name: /tmp/rtexec.pf
        - source: {{ antelope.files }}/rtexec.pf
        - template: jinja
        - defaults: {{ salt['pillar.get']('antelope:pf:rtexec:generic',{}) }}


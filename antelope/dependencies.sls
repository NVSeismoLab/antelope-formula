#
# SaltStack state file for Antelope dependencies
#
# Keep a list of depends
{% from "antelope/map.jinja" import depends with context %}

# Installer won't run without these - ridiculous
{% if depends.installer %}
installer_dependencies:
    pkg:
        - installed
        - pkgs:
            {% for pkgname in depends.installer %}
            - {{ pkgname }}
            {% endfor %}
{% endif %}

# Required packages, files, services for Antelope to work
#
# (Force unique names to avoid collision)

# TODO: Insert future yum group installs here:
# for grp in  depends.groups
# [pkg using groupinstall option...]
# endfor
# ** (for now any yum groupinstalls must be done with/after update
#     on machine setup)**

# Program dependencies - for proper functioning
{% for pkgname in depends.programs %}
ant_pkg_{{ pkgname }}:
    pkg:
        - installed
        - name: {{ pkgname }}
{% endfor %}

# Service dependencies - for proper functioning
# TODO: add -require: - pkg statements
# TODO: related, restart lightdm, etc, otherwise need reboot
#       for loading xfont paths. PITA.
{% for srv in depends.services %}
ant_srv_{{ srv }}:
    service:
        - running
        - enable: True
        - name: {{ srv }}
{% endfor %}



#
{% from 'antelope/map.jinja' import antelope with context %}

{% set sitecustomize = 'salt://antelope/python/files/sitecustomize.py' %}
# Ubuntu 12.04+, use system python, append to system sitecustomize file
# TODO: add RedHat 7
{% if grains['os'] == 'Ubuntu' %}

/etc/python2.7/sitecustomize.py:
    file.append:
        - sources:
            - {{ sitecustomize }}

# md5 package in Antelope python hardcodes lib names, link em
/usr/lib/x86_64-linux-gnu/libssl.so.10:
    file.symlink:
        - target: /lib/x86_64-linux-gnu/libssl.so.1.0.0

/usr/lib/x86_64-linux-gnu/libcrypto.so.10:
    file.symlink:
        - target: /lib/x86_64-linux-gnu/libcrypto.so.1.0.0

{% endif %}

#
# Antelope ships with out-of-date non-patched 2.7.2, no sitecustomize file, so just add one.
#
{% if antelope.version|string == '5.3' %}
/opt/antelope/python2.7.2/lib/python2.7/site-packages/sitecustomize.py:
    file.managed:
        - source: {{ sitecustomize }}
{% endif %}

{% if antelope.version|string == '5.2-64' %}
/opt/antelope/python2.7.2-64/lib/python2.7/site-packages/sitecustomize.py:
    file.managed:
        - source: {{ sitecustomize }}
{% endif %}


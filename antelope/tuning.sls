#
# These are not optimal settings for many things, use for a dedicated 
# Antelope server, esp one running real-time with no commercial stuff
#
/etc/security/limits.d/antelope-files.conf:
  file.managed:
    - user: root
    - group: root
    - contents: |
        *                soft    nofile          8192
        *                hard    nofile          65535

/etc/security/limits.d/antelope-procs.conf:
  file.managed:
    - user: root
    - group: root
    - contents: |
        *                soft    nproc           8192
        *                hard    nproc           65535



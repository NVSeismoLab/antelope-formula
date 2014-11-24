# 
# Salt state for sitecustomize.py
#
# Standard site customization file for NSL Antelope python
# - by Mark Jan 2013
#
# Python site customizing, easier than changing PYTHONPATH for all users, 
# and arguably more proper. This is a foolproof way to ensure that the 
# antelope package location is always in sys.path before importing.
#
# (Alternately, could append PYTHONPATH in Antelope setup file... but then
# other versions of python (2.6 anyone? will choke on the libs...)
#
# INSTRUCTIONS:
# This file goes in /opt/antelope/pythonX.X.X/lib/pythonX.X/site-packages.
# It is automatically looked for and run by python during initialization.
#
import site, os
dir1 = ['data','python']
dir2 = ['local'] + dir1
version_defaults = {'python2.7.2-64': '5.2-64',
                    'python2.7.2': '5.3',
                    'python2.7.6': '5.4'}
if 'ANTELOPE' in os.environ:
    site.addsitedir(os.path.join(os.environ['ANTELOPE'],*dir1))
    site.addsitedir(os.path.join(os.environ['ANTELOPE'],*dir2))
else:
    self_dir = os.path.abspath(__file__)
    py_version = self_dir.split(os.sep)[3]
    if py_version in version_defaults:
        version = version_defaults[py_version]
        ant_default = os.path.join(os.path.sep,'opt','antelope', version)
        site.addsitedir(os.path.join(ant_default, *dir1))
        site.addsitedir(os.path.join(ant_default, *dir2))


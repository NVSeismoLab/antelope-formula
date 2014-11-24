# -*- coding: utf-8 -*-
"""
Salt execution module for managing Antelope software

Loosely based on "antelope_install_wrapper" from UCSD-ANF
modified by NSL for use by SaltStack

"""
import os
import sys
import re
import logging
import StringIO
from salt.exceptions import CommandExecutionError

# log for debugging, info
LOG = logging.getLogger('salt.modules.antelope')

##############################################################################
# Defaults (when none are specified)
##############################################################################
INSTALL_ROOT = ['opt', 'antelope']
INSTALLER_CMD_NAME='Install_antelope'
INSTALLER_ARGS= ['-tuv']
VERSION = '5.4'  # default version if none passed
#----------------------------------------------------------------------------#

def _base_dir(install=INSTALL_ROOT):
    return os.path.join(os.sep, *install)


def _env(version=VERSION):
    return os.path.join(_base_dir(), str(version))


def _run_installer(path, args=INSTALLER_ARGS):
    """
    Run Antelope installer script from a location

    path : str path of the location of install script
           (ususally mount point of cd/iso)
    
    args : list of str of args to be passed to installer
           (defaults to ['-tuv'])
    
    """
    installer_cmd = os.path.join(path, INSTALLER_CMD_NAME)
    cmd = '{0} {1}'.format(installer_cmd, ' '.join(INSTALLER_ARGS))
    # dict of 'retcode', 'stderr', 'stdout'
    return __salt__['cmd.run_all'](cmd)


def _mount_iso(isofile, mnt_point):
    """
    SaltStack migration - mount ISO

    isofile : str name of ISO file
    mnt_point : str path of mount point

    """
    # Make the 
    MKMNT = False
    if not os.path.exists(mnt_point):
        MKMNT = True
    # check to see if it's there already?
    #mounts = __salt__['mount.active']()
    return __salt__['mount.mount'](mnt_point, isofile, mkmnt=MKMNT,
                                   fstype='iso9660', opts='loop')

def _unmount_iso(mnt_point):
    """
    SaltStack migration - unmount ISO
    """
    #mounts = __salt__['mount.active']()
    return __salt__['mount.umount'](mnt_point)
    

def _run(command, version=VERSION, **kwargs):
    """
    Run an antelope command
    
    version : str of Antelope version to use (optional)

    **kwargs : all additional keywords passed to 'cmd.run'
               (i.e. 'runas', etc)
    """
    ENV = _env(version)
    cmd = os.path.join(ENV, 'bin', command)
    return __salt__['cmd.run_all'](cmd, env={'ANTELOPE': ENV}, **kwargs)


class _AntelopeInstaller(object):
    """
    Wrapper class for main to call installer functions and gracefully deal
    with errors and logging.
    """
    logger = LOG  # mainly for debugging
    logstream = StringIO.StringIO()   # save log to stream to return on error
    version = None
    source = None
    mount_point = os.path.join(os.sep, 'mnt')
    _mounted = False
    
    @classmethod
    def log_to_stream(cls, level='DEBUG'):
        """
        Setup a logger.
        
        Inputs
        ------
        level : string of valid logging level ('DEBUG')
        
        Generates a logging.Logger available at the 'logger' attribute
        -> contains one handler to log to stderr stream
        -> Stream handler logging level specified by 'level'

        """
        cls.logger.setLevel(logging.DEBUG)
        # create console handler and set level
        ch = logging.StreamHandler(cls.logstream) # default stream=sys.stderr
        lvl = getattr(logging, level.upper())
        ch.setLevel(lvl)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        cls.logger.addHandler(ch)

    def __init__(self, source='', mount_point=None, version='', debug=False):
        """
        Construct away
        """
        self.log_to_stream()
        self.version = str(version)
        if mount_point is not None:
            self.mount_point = mount_point
        # Possible to pass a directory structure too 
        if source.endswith('.iso'):
            self.logger.info("Attempting to mount %s to %s" % (source, self.mount_point))
            self._mounted = _mount_iso(source, self.mount_point)
            self._source = source
            self.source = self.mount_point
        elif source.endswith(INSTALLER_CMD_NAME):
            self.source = source.rstrip(INSTALLER_CMD_NAME)
        elif os.path.isdir(source):
            self.source = source
        # Verify the installer script is there
        ant_install = os.path.join(self.source, INSTALLER_CMD_NAME)
        if not os.path.exists(ant_install):
            raise OSError("Not a valid path to Antelope install: " + ant_install)

    @property
    def _version(self):
        """
        Return a tuple of major, minor, suffix related to the antelope version
        """
        m = re.match(r"^(\d+)\.(\d+)(.*)$", self.version)
        return m.group(1,2,3)

    def get_installer_args(self):
        (major, minor, suffix) = self._version
        if int(major) == 5 and int(minor) < 3:
            args = []
        elif int(major) < 5:
            args = []
        else:
            args = ['-S']
        args.extend(INSTALLER_ARGS)
        return args

    def is_installed(self):
        """
        Check if a version is installed by presence of a test file
        (default is 'Release.txt' in /opt/antelope/<version>/)
        """
        test_file = os.path.join(_env(self.version),'Release.txt')
        return os.path.exists(test_file)

    def run(self, force=True):
        try:
            if force or not self.is_installed():
                self.logger.info("Installing Antelope %s" % self.version)
                out = _run_installer(self.source, args=self.get_installer_args())
                self.logger.info(out)
            else:
                self.logger.info("Antelope %s is installed, use 'force' to reinstall" % self.version)
        except Exception as e:
            self.logger.warn("Something went wrong")
            self.logger.exception(e)
        finally:
            if self._mounted is True:
                self.logger.info("Unmounting %s" % self.mount_point)
                _unmount_iso(self.mount_point)
            self.logstream.flush()
            self.logstream.seek(0)
            return self.logstream.read()
        return True

##############################################################################
# Module commands
##############################################################################

def install(source, mnt='/mnt', version=VERSION, force=False):
    """
    Install Antelope software from an ISO file
    
    Inputs
    ======
    source : str of full path of install media (ISO)
               or path to install script
    
    Optional
    --------
    mnt : str of mount point for media ('/mnt')

    version : str of Antelope version (defaults to current version in module)

    force : bool of whether to install over an existing install (False)

    """
    return _AntelopeInstaller(source=source, mount_point=mnt, version=version).run(force)


def is_installed(version=VERSION):
    """
    Check if a version is installed by presence of a test file
    (default is 'Release.txt' in /opt/antelope/<version>/)
    """
    test_file = os.path.join(_env(version),'Release.txt')
    return os.path.exists(test_file)


def is_updated(version=VERSION):
    """
    Check if there are unapplied patches to the Antelope install

    Returns: True if there are no pending unapplied patches
             False otherwise (including not installed)
    """
    if not is_installed(version):
        return False
    ENV = _env(version)
    opts = '-tL'
    exe = os.path.join(ENV,'bin','antelope_update')
    cmd = '{0} {1}'.format(exe, opts)
    # Returns new line separated list of patches
    out = __salt__['cmd.run_all'](cmd, env={'ANTELOPE': ENV})
    if out['retcode']:
        return out['stderr']
    
    updates = out['stdout'].split('\n')
    for patch in updates:
        if patch.startswith('*'):
            return False
    
    return True


def update(version=VERSION):
    """
    Run antelope update if there are updates to be updated with update
    """
    if not is_installed(version):
        return False
    ENV = _env(version)
    opts = '-tQ'
    exe = os.path.join(ENV,'bin','antelope_update')
    cmd = '{0} {1}'.format(exe, opts)
    out =  __salt__['cmd.run_all'](cmd, env={'ANTELOPE': ENV})
    if out['retcode']:
        return out['stderr']
    return True


def patch(tarball, dest=None, version=None):
    """
    Patch Antelope from a tarball
    
    INPUTS
    ======
    tarball : str of gzipped tarfile, can be relative to
              /opt/antelope/<vers>/patches if 'version' is defined

    dest : destination top level to untar in [/opt/antelope]
    version : specify a version to use 'patches' dir

    NOTES
    -----
    - Only works on Salt version 2014.1.0??
    
    """
    if dest is None:
        dest = _base_dir()
    
    if not __salt__['file.file_exists'](tarball) and version:
        tarball = os.path.join(_env(version), 'patches', tarball)
    
    ret = __salt__['archive.tar']('xzf', tarball, dest=dest, template='jinja')
    if ret:
        return ret
    return True


def check_license(opts=[], version=VERSION, **kwargs):
    """
    Check license of an Antelope version

    version : str of Antelope version to use (optional)

    **kwargs : all additional keywords passed to 'cmd.run'
               (i.e. 'runas', etc)
    """
    if not is_installed(version):
        return False
    out = _run('check_license', version)
    if out['retcode']:
        return out['stderr']
    return out['stdout']


def rtinit(directory, opts=[], version=VERSION, **kwargs):
    """
    Run rtinit in a directory
    
    directory : str passed to 'cwd' of where to run from
    opts : iterable of str of options for 'rtinit'
    version : str of Antelope version to use (optional)

    **kwargs : all additional keywords passed to 'cmd.run'
               (i.e. 'runas', etc)
    """
    ENV = _env(version)
    exe = os.path.join(ENV,'bin','rtinit')
    options = ' '.join(opts)
    cmd = '{0} {1}'.format(exe, options)
    out =  __salt__['cmd.run_all'](cmd, cwd=directory, env={'ANTELOPE': ENV}, **kwargs)
    if out['retcode']:
        return out['stderr']
    return True


def rtexec(directory, action=None, version=VERSION, **kwargs):
    """
    Run rtexec in a directory
    
    directory : str passed to 'cwd' of where to run from
    opts : iterable of str of options for 'rtinit'
    version : str of Antelope version to use (optional)

    **kwargs : all additional keywords passed to 'cmd.run'
               (i.e. 'runas', etc)
    """
    OPTS = [] # the -s option breaks remote exec somehow...
    ENV = _env(version)
    exe = os.path.join(ENV,'bin','rtexec')
    options = ' '.join(OPTS)
    
    # Optionally, use keywords instead of options?
    # This may go away:
    if action == "restart":
        options = '-f ' + options
    elif action == "stop":
        options = '-fk  Auto-killed by salt'

    cmd = '{0} {1}'.format(exe, options)
    out =  __salt__['cmd.run_all'](cmd, cwd=directory, env={'ANTELOPE': ENV}, **kwargs)
    if out['retcode']:
        return out['stderr']
    return True


def run(command, version=VERSION, **kwargs):
    """
    Run an antelope command
    
    version : str of Antelope version to use (optional)

    **kwargs : all additional keywords passed to 'cmd.run'
               (i.e. 'runas', etc)
    """
    ENV = _env(version)
    cmd = os.path.join(ENV, 'bin', command)
    return __salt__['cmd.run_all'](cmd, env={'ANTELOPE': ENV}, **kwargs)



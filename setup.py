#!/usr/bin/env python
import os, subprocess, re
from distutils.core import setup, Command
from distutils.command.sdist import sdist as _sdist

# The following code is taken from
# https://github.com/warner/python-ecdsa/blob/f03abf93968019758c6e00753d1b34b87fecd27e/setup.py
# which is released under the MIT license (see LICENSE for the full license
# text) and (c) 2012 Brian Warner
VERSION_PY = """
# This file is originally generated from Git information by running 'setup.py
# version'. Distribution tarballs contain a pre-generated copy of this file.

__version__ = '%s'
"""

def update_version_py():
    if not os.path.isdir(".git"):
        print "This does not appear to be a Git repository."
        return
    try:
        p = subprocess.Popen(["git", "describe",
                              "--tags", "--dirty", "--always"],
                             stdout=subprocess.PIPE)
    except EnvironmentError:
        print "unable to run git, leaving lala/__init__.py alone"
        return
    stdout = p.communicate()[0]
    if p.returncode != 0:
        print "unable to run git, leaving lala/__init__.py alone"
        return
    ver = stdout.strip()
    f = open("lala/__init__.py", "w")
    f.write(VERSION_PY % ver)
    f.close()
    print "set lala/__init__.py to '%s'" % ver

def get_version():
    try:
        f = open("lala/__init__.py")
    except EnvironmentError:
        return None
    for line in f.readlines():
        mo = re.match("__version__ = '([^']+)'", line)
        if mo:
            ver = mo.group(1)
            return ver
    return None

class Version(Command):
    description = "update lala/__init__.py from Git repo"
    user_options = []
    boolean_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        update_version_py()
        print "Version is now", get_version()

class sdist(_sdist):
    def run(self):
        update_version_py()
        # unless we update this, the sdist command will keep using the old
        # version
        self.distribution.metadata.version = get_version()
        return _sdist.run(self)

# Here ends the code taken from Brian Warner

setup(name="lala",
        version=get_version(),
        author="Wieland Hoffmann",
        author_email="themineo@gmail.com",
        scripts=["run-lala.py"],
        packages=["lala", "lala.plugins"],
        package_dir = {"lala": "lala"},
        requires=["Twisted"],
        download_url=["https://github.com/mineo/lala/tarball/master"],
        url=["http://github.com/mineo/lala"],
        license="MIT",
        classifiers=["Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: End Users/Desktop",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7"],
        data_files=[("usr/share/doc/lala", ["config.example"])],
        cmdclass={"version": Version, "sdist": sdist}
        )

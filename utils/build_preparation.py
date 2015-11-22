#!/usr/bin/env python

# Coded for both python2 and python3.

'''
Copy all resources for out-of-source documentation build

Since we provide a build for Linux, MacOSX, and Windows,
this tool must be multiplatform.  If only for Linux
(and possibly MacOSX), it might be possible to use a form of::

  cp -a ../base_classes ./
  cp -a ../applications ./
  cp -a ../contributed_definitions ./
  cp -a ../manual ./
  ...

Here, we identify and copy all resources to build.
The target directory is assumed to be the current directory.

'''

# TODO: make target resources dependent on changes in relevant source resources 
# for now, re-run this code to bring in any changed files, forces a complete rebuild

from __future__ import print_function
import os, sys, re
import local_utilities
import shutil


ROOT_DIR_EXPECTED_RESOURCES = {
    'files': '''COPYING LGPL.txt Makefile NXDL_VERSION
                nxdl.xsd nxdlTypes.xsd README.md
             '''.split(),
    'subdirs': '''applications base_classes contributed_definitions manual
                 package utils www
               '''.split(),
}
REPLICATED_RESOURCES = '''
    LGPL.txt  Makefile  nxdl.xsd  nxdlTypes.xsd  NXDL_VERSION
    base_classes  applications  contributed_definitions 
    manual  utils
'''.split()


def is_definitions_directory(basedir):
    '''test if ``basedir`` is a NeXus definitions directory'''
    # look for the expected files and subdirectories in the root directory
    for item_list in ROOT_DIR_EXPECTED_RESOURCES.values():
        for item in item_list:
            if not os.path.exists(os.path.join(basedir, item)):
                return False
    return True


def qualify_inputs(source_dir, target_dir):
    '''raise error if this program cannot continue, based on the inputs'''
    if not os.path.exists(source_dir):
        raise RuntimeError('Cannot find ' + source_dir)

    if not os.path.isdir(source_dir):
        raise RuntimeError('Not a directory: ' + source_dir)

    if not is_definitions_directory(source_dir):
        msg = 'Not a NeXus definitions root directory ' + source_dir
        raise RuntimeError(msg)
    
    if source_dir == target_dir:
        msg = 'Source and target directories cannot be the same'
        raise RuntimeError(msg)


def command_args():
    '''get the command-line arguments, handle syntax errors'''
    import argparse
    doc = __doc__.strip().splitlines()[0]
    parser = argparse.ArgumentParser(prog=sys.argv[0], description=doc)
    parser.add_argument('defs_dir',
                        action='store', 
                        help="path to NeXus definitions root directory")
    parser.add_argument('build_dir',
                        action='store', 
                        default=None,
                        nargs='?',
                        help="path to target directory (default: current directory)")
    return parser.parse_args()


def main():
    '''
    standard command-line processing
    
    source directory (NeXus definitions dir) named as command line argument
    target directory is specified (or defaults to present working directory)
    '''
    cli = command_args()
    defs_base_directory = os.path.abspath(cli.defs_dir)
    target_dir = cli.build_dir or os.path.abspath(os.getcwd())
    qualify_inputs(defs_base_directory, target_dir)
    
    for resource_name in sorted(REPLICATED_RESOURCES):
        source = os.path.join(defs_base_directory, resource_name)
        target = os.path.join(target_dir, resource_name)
        local_utilities.printf('cp %s %s\n', source, target)
        local_utilities.replicate(source, target)


def __developer_build_setup__():
    '''for use with source-code debugger ONLY'''
    import shutil
    # sys.argv.append('-h')
    os.chdir('../')
    if os.path.exists('build'):
        shutil.rmtree('build')
    os.mkdir('build')
    os.chdir('build')
    sys.argv.append('..')


if __name__ == '__main__':
    # __developer_build_setup__()
    main()


# NeXus - Neutron and X-ray Common Data Format
# 
# Copyright (C) 2008-2015 NeXus International Advisory Committee (NIAC)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For further information, see http://www.nexusformat.org

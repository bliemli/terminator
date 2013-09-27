#!/usr/bin/env python
# Description: Installs a launchdaemon on OS X that forces a shutdown every day at a defined time.
# Author: bliemli

import argparse
import time
import os
import sys
import subprocess

class Terminator():
    def __init__(self):
        self.launchdaemon_file = '/Library/LaunchDaemons/ch.bliemli.terminator.plist'

    def install(self, t):
        self.create_plist(t)
        self.load_launchdaemon()

    def remove(self):
        self.unload_launchdaemon()
        self.remove_plist()

    def create_plist(self, t):
        self.launchdaemon_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ch.bliemli.terminator</string>
    <key>UserName</key>
    <string>root</string>
    <key>ProgramArguments</key>
    <array>
        <string>shutdown</string>
        <string>-h</string>
        <string>now</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Minute</key>
        <integer>''' + time.strftime('%M', t) + '''</integer>
        <key>Hour</key>
        <integer>''' + time.strftime('%H', t) + '''</integer>
    </dict>
</dict>
</plist>'''

        with open(self.launchdaemon_file, 'w') as f:
            f.write(self.launchdaemon_content + '\n')

    def load_launchdaemon(self):
        try:
            subprocess.call(['launchctl', 'load', self.launchdaemon_file])
        except OSError:
            sys.stderr.write('ERROR: Unable to execute launchctl command!\n')

    def unload_launchdaemon(self):
        try:
            subprocess.call(['launchctl', 'unload', self.launchdaemon_file])
        except OSError:
            sys.stderr.write('ERROR: Unable to execute launchctl command!\n')

    def remove_plist(self):
        try:
            os.remove(self.launchdaemon_file)
        except OSError:
            sys.exit('ERROR: Unable to remove plist file!')

def mktime(timestr):
    return time.strptime(timestr, '%H:%M')

def main():
    ver = '0.2'
    term = Terminator()
    
    parser = argparse.ArgumentParser(description = 'Install a LaunchDaemon that forces shutdown at a defined time.', formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--install', action='store_true')
    group.add_argument('-r', '--remove', action='store_true')
    parser.add_argument('-t', '--time', help='set desired execution time', type=mktime, default='22:30')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + ver)

    args = parser.parse_args()

    if args.install:
        term.install(args.time)
    elif args.remove:
        term.remove()

if __name__ == '__main__':
    if not os.geteuid() == 0:
        sys.exit('WARNING: Script must be run as root!')
    main()

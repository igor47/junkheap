#!/usr/bin/python

import sys, commands

device='/dev/sg0'
libTool='libTool'

class Fatal(Exception):
	"""Fatal Error"""
	pass

class Positioning(Exception):
	"""Positioning Error"""
	pass

class Slot(object):
	def __init__(self,id,empty=True):
		self.id = id
		self.empty = empty


def getStatus():
	cmd = "%s %s -l" % (libTool, device)
	status, output = commands.getstatusoutput(cmd)

	if status != 0:
		sys.stderr.write("<none> %s" % output)
		raise Fatal
	
	status = { }
	for line in output.split('\n'):
		line = line.split()
		if len(line) < 3: continue
		if line[0] == 'Slot':
			slotId = "S%s" % line[1]
			if line[2] == '[Empty]': empty=True
			else: empty=False
			status[line[1]] = Slot(slotId,empty)
		if line[0] == 'Drive':
			slotId = ""

	currentId = file("/var/tmp/tape-changer.status").read()


def loadSlot(slot):
	status = getStatus()
	slotId = status[slot].id
		sys.stderr.write("%s no slot '%s'" % (slot, slot))
		raise Fatal
	unloadDrive()
	
		

def main(argv):
	try:
		if len(argv) == 0:
			sys.stderr.write("<none> invalid command")
			raise Fatal
		elif argv[0] == '-slot':
			try:
				loadSlot(argv[1])
			except KeyError:
				sys.stderr.write("<none> slot missing")
				raise Fatal
		elif argv[0] == '-info':
			printInfo()
		elif argv[0] == '-reset':
			loadSlot('first')
		elif argv[0] == '-eject':
			unloadDrive()
	except Positioning:	return 1
	except Fatal:			return 2
	else: 					return 0


if __name__ == __main__:
	sys.exit(main(sys.argv[1:]))

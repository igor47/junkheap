#!/usr/bin/python

import sys, os, os.path, re

class wordFinder(object):
	"""Creates a hash of all words in all files in <path> that start with <letter>"""
	def __init__(self, path, letter = False):
		"""Creates the variables and starts the search rolling"""
		if letter:
			self.wordRe = re.compile(r'\b%c\w*\b' % letter, re.IGNORECASE)
		else:
			self.wordRe = re.compile(r'\b\w+\b', re.IGNORECASE)

		self.words = {}
		for dirname, dirs, files in os.walk(path):
			for f in files:
				self.findWords(os.path.join(dirname,f))

	def findWords(self, f):
		"""Puts all the words in file f that match self.wordRe into self.words"""
		for line in open(f).readlines():
			for wordM in self.wordRe.finditer(line):
				word = wordM.group().lower()
				try:
					self.words[word] += 1
				except KeyError:
					self.words[word] = 1

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print "usage: %s <path> [<letter>]" % sys.argv[0]
		sys.exit(1)
	elif len(sys.argv) == 2:
		finder = wordFinder(sys.argv[1])
	else:
		finder = wordFinder(sys.argv[1], sys.argv[2])

	#strange little sorting algorithm - i think this 
	#has a name? but I can't remember it
	toprint = ["%09d|%s" % (count, word) for word, count in finder.words.items()]
	toprint.sort()					#use python to sort the list in-place
	for v in toprint:
		count, word = v.split('|')			#extract the original values
		print "%s\t:\t%d" % (word, int(count))

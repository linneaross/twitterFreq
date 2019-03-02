# coding: utf-8

import sys
import re
from collections import defaultdict
import random
import math

## EXTRA CREDIT ##
def rand(hist):
	rnum = random.uniform(0,1)
	for x in hist:
		rnum -= hist[x]
		if rnum < 0: return x
	return x

## PART 1 ##
def clean(line):
	line = line.decode('utf8')
	line = re.sub(u'(https://t.co/)(\w+)', 'www', line)
		#urls
	line = re.sub(u'[!$%^&*()-+=,.?:;(\u2026)(\u0022)(\u201C)(\u201D)]', '', line)
		#punctuation
	line = re.sub(u'(@)(\w+)', '@@@', line)
		#usernames
	line = re.sub(u'(#)(\w+)', '###', line)
		#hashtags
	line = re.sub(u'((^\s+)|(\s+\Z))', '', line)
		#leading and trailing whitespace
	line = line.lower()
		#set it all to lowercase
	return line

## PART 2 ##
def normalize(hist):
	sum = 0.0
	for key in hist:
		sum = sum + hist[key]
	for item in hist:
		hist[item] = hist[item]/sum

def get_freqs(f):
	wordfreqs = defaultdict(lambda: 0)
	lenfreqs = defaultdict(lambda: 0)

	for line in f.readlines():
		#print line
		line = clean(line)
		words = re.split(u'\s+|\s+[-]+\s+', line)
		#print line
		#print '============='
		lenfreqs[len(words)]+=1
		for word in words:
			wordfreqs[word.encode('utf8')]+=1

	normalize(wordfreqs)
	normalize(lenfreqs)
	return (wordfreqs,lenfreqs)

## PART 3 ##
def save_histogram(hist,filename):
	outfilename = re.sub("\.txt$","_out.txt",filename)
	outfile = open(outfilename,'w')
	print "Printing Histogram for", filename, "to", outfilename
	rank = 0
	for word, count in sorted(hist.items(), key = lambda pair: pair[1], reverse = True):
		rank = rank+1
		log1 = math.log(count)
		log2 = math.log(rank)
		output = "%-13.6f\t%s\t%f\t%f\n" % (count,word,log1,log2)
		outfile.write(output)

## PART 4 ##
def get_top(hist,N):
	result = []
	ticker = 0
	rank = 0
	for word, count in sorted(hist.items(), key = lambda pair: pair[1], reverse = True):
		if (ticker==N):
			break
		rank = rank+1
		log1 = math.log(count)
		log2 = math.log(rank)
		result.append(word)
		ticker = ticker +1
	# return a list of the N most frequent words in hist
	return result

def filter(hist,stop):
	for word in stop:
		if word in hist: hist.pop(word)
	normalize(hist)

def main():
	file1 = open(sys.argv[1])
	(wordf1, lenf1) = get_freqs(file1)
	stopwords = get_top(wordf1, 100)
	save_histogram(wordf1,sys.argv[1])

	for fn in sys.argv[2:]:
		file = open(fn)
		(wordfreqs, lenfreqs) = get_freqs(file)
		filter(wordfreqs, stopwords)
		save_histogram(wordfreqs,fn)

		## EXTRA CREDIT ##
		print "Printing random tweets from",fn
		for x in range(5):
			n = rand(lenfreqs)
			print n, "random words:"
			for i in range(n):
				print ' ',rand(wordfreqs),
			print

## This is special syntax that tells python what to do (call main(), in this case) if this  script is called directly
## this gives us the flexibility so that we could also import this python code in another script and use the functions
## we defined here
if __name__ == "__main__":
    main()

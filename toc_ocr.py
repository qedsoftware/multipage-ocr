#!/usr/bin/env python

# toc_ocr.py
# 2013-03-08 
# William Wu 

# import packages
import copy, sys
from pyPdf import PdfFileWriter, PdfFileReader
import os, subprocess, getopt, hashlib, time, numpy
import string
import random

# usage
def usage():
	print('Usage:\n\t%s [input_file]' % sys.argv[0])
	print('Optional:')
	print('\t-n [integer]	number of bytes to extract')
	print('\t-m 		search extract from middle')
	print('\t-r 		search extract from random location')
	print('\t-a 		search all (entire file)')
	
# check that an argument has been provided
if len(sys.argv) < 2:
	usage()
	sys.exit()

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

# main method
def main(argv):

	input_file = ""
	output_file = "toc.txt"
	density = 300
	depth = 8

	# command-line arguments
	try:
		# gnu_getopt allows interspersing of option and non-option arguments
		opts, args = getopt.gnu_getopt(argv, "hi:o:d:b:", ["help", "input=", "output=", "density=", "depth="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-i", "--input"):
			input_file = arg
		elif opt in ("-o", "--output"):
			output_file = arg
		elif opt in ("-d", "--density"):
			density = int(arg)
		elif opt in ("-b", "--depth"):
			depth = int(arg)
	
	# check if the file provided as argument exists
	if not os.path.exists(input_file):
		sys.exit('ERROR: Input file \'%s\' was not found!' % input_file)

	# check if input file is a PDF
	if not input_file.endswith(".pdf"):
		sys.exit('ERROR: Input file should be a PDF.')

	# extract basename
	basename, ext = os.path.splitext(os.path.basename(input_file))

	# get number of pages
	num_pages = PdfFileReader(file(input_file)).getNumPages()
	print "Number of pages: %d" % num_pages

	# random hash
	random_id = id_generator()

	# iterate through pages
	text_files = []
	# num_pages = 2
	for i in xrange(0,num_pages):
		# convert PDF to TIFF
		cmd = ("convert -density %d -depth %d " % (density,depth)) + ("%s.pdf[%d] -background white %s_%d.tif" % (basename,i,basename,i))
		print cmd
		os.system(cmd)
		# execute OCR
		f = random_id + "_output_" + str(i) + ".txt"
		text_files.append(f)
		cmd = "tesseract %s_%d.tif %s_output_%d" % (basename,i,random_id,i)
		print cmd
		os.system(cmd)

	print text_files
	print " ".join(text_files)

	# concatenate results and delete them
	cmd = "cat %s > %s" % (" ".join(text_files), output_file)
	print cmd
	os.system(cmd)

	# cleanup
	for f in text_files:
		os.system("rm " + f)


# invoke main
if __name__ == "__main__":
	main(sys.argv[1:])

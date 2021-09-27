#!/usr/bin/python
# FileName: Subsampling.py 
# Version 1.0 by Tao Ban, 2010.5.26
# This function extract all the contents, ie subject and first part from the .eml file 
# and store it in a new file with the same name in the dst dir.
# Tweaked to function in Python3

import email.parser
import os, sys, stat
import shutil


def extract_sub_payload(filename):
	# Extract the subject and payload from the .eml file.
	if not os.path.exists(filename):  # dest path doesnot exist
		print("ERROR: input file does not exist:", filename)
		exit(1)
	fp = open(filename)
	msg = email.message_from_file(fp)
	payload = msg.get_payload()
	if isinstance(payload, list):  # type(payload) == type(list())
		payload = payload[0]  # only use the first part of payload
	sub = msg.get('subject')
	sub = str(sub)
	if not isinstance(payload, type('')):  # type(payload) != type('')
		payload = str(payload)

	return sub + payload


def extract_body_from_dir(srcdir, dstdir):
	"""Extract the body information from all .eml files in the srcdir and
    save the file to the dstdir with the same name."""
	if not os.path.exists(dstdir):  # dest path does not exist
		os.makedirs(dstdir)
	files = os.listdir(srcdir)
	for file in files:
		srcpath = os.path.join(srcdir, file)
		dstpath = os.path.join(dstdir, file)
		src_info = os.stat(srcpath)
		if stat.S_ISDIR(src_info.st_mode):  # for subfolders, recurse
			extract_body_from_dir(srcpath, dstpath)
		else:  # copy the file
			body = extract_sub_payload(srcpath)
			dstfile = open(dstpath, 'w')
			dstfile.write(body)
			dstfile.close()


###################################################################
# main function start here
# srcdir is the directory where the .eml are stored
if __name__ == '__main__':
	print('Input source directory: ')  # ask for source and dest dirs
	srcdir = input()
	if not os.path.exists(srcdir):
		print('The source directory %s does not exist, exit...' % (srcdir))
		sys.exit()
	# dstdir is the directory where the content .eml are stored
	print('Input destination directory: ')  # ask for source and dest dirs
	dstdir = input()
	if not os.path.exists(dstdir):
		print('The destination directory is newly created.')
		os.makedirs(dstdir)

	extract_body_from_dir(srcdir, dstdir)

###################################################################

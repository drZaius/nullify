#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################################################################
############################################################################################################
# this file is part of the nulling tool (see nullify.py)
############################################################################################################
############################################################################################################

from __future__ import print_function 
import binascii
import time
import subprocess
import os
from subprocess import PIPE
import time
import math


############################################################################################################
# this functions displays a dialog, where the user can choose which check the tool will do after erasing
# the device

def chooseCheckType(blocks):
	whichCheck = 0
	print("After the nulling process, a full check or a quick check of the device can\nbe done, to make sure erasing the device was successful.\n")
	print("Full check will check " + str(int(blocks)) + " blocks of size 512 Byte.")
	print("Quick check will check every 10th block of size 512 Byte: " + str(int(blocks / 10)) + " Blocks.")
	print("A full check is highly recommended!")
	while True:
		print()
		whichCheck = input('\033[0m0 ----> Full Check\n' + \
							'1 ----> Quick Check\n' + \
							'2 ----> Skip Check (a check will not be done; not recommended!)\n' + \
							'Note: skipping the check will also be mentioned on the report!\n' + \
							'\nInput: \033[1m\033[37m')
		print()
		try:
			if whichCheck.isspace() or not whichCheck or len(whichCheck) > 1:
				print()
				print('Invalid input! Please choose a single digit between 0 and 3 or simply press <ENTER>.')
			else:				
				whichCheck = int(whichCheck)
				if whichCheck < 0 or whichCheck > 2:
					print()
					print('Invalid input! Please choose a single digit between 0 and 3 or simply press <ENTER>.')
				else:
					break
		except ValueError as e:
			print()
			print('Invalid input! Please choose a single digit between 0 and 3 or simply press <ENTER>.')
			print()
	print()

	return whichCheck


############################################################################################################
# depending on which check the user selected, this function will call the function 'check' with the right
# parameters 

def checkRoutine(filename, blocks, whichCheck):
	# full check
	if whichCheck == 0:
		print("Full Check: ")
		print("\033[0mBlock 0 to " + str(int(blocks)) + " will be checked.")
		print()
		print('\033[37m\033[1mchecking...')
		print()
		return check(filename, blocks, 0, blocks, 1)

	# quick check
	elif whichCheck == 1:
		print("Quick Check: ")
		print(str(int(blocks / 10)) + " out of " + str(int(blocks)) + " blocks will be checked.")
		print()
		print('\033[37m\033[1mchecking...')
		print()
		return check(filename, blocks, 0, blocks, 10)

	elif whichCheck == 2:
		print('Skipping Check')
		return 2, None

############################################################################################################
# this function provides a test routine of the drive that has been nulled by reading the drive in 512 byte blocks
# and comparing those to a static 512 byte block of zeros
# if a block turns out to have not been nullified, the user can choose how to proceed from there

def check(filename, blocks, start, end, step):
	falseBlock = False
	restart = 0
	abort = False
	prev_time = time.time()
	zeros = '00' * 512
	i = int(start)
	file = open(filename, 'rb')
	with file:
		while i != int(end):
			dt = time.time() - prev_time
			if dt > 5:
				try:
					print('\033[K\033[37m\033[1mchecking block ' + str(i) + ' of ' + str(int(end)) + ' ===> ' + str(math.floor((float(i) / end) * 100)) + '%', end='\r')
				except ValueError as ex:
					print(ex, '\r')
				prev_time = time.time()
			singleBlock = file.read(512)
			hexadecimal = binascii.hexlify(singleBlock).decode('ascii')

			if zeros != hexadecimal:
				while True:
					print()
					print('\033[0mBlock \033[37m\033[1m' + str(i) + ' \033[0mdoes not seem to have been properly erased...')
					print()
					print('What do you want to do now?')
					print('0 ----> check next block (current block will be discarded)\n' + \
						'1 ----> cancel (Program will terminate. No report will be created!)\n' + \
						'2 ----> start nulling again (recommended)')
					restart = input('Input: \033[37m\033[1m')
					print()
					try:
						restart = int(restart)
						if restart == 0:
							falseBlock = True
							break
						elif restart > 2:
							print('\033[91mInvalid input!')
							print('Please enter a single digit between 0 and 2!')
							print()
							continue
						else:
							return restart
					except ValueError as ex:
						print('\033[91mInvalid input!')
						print('Please enter a single digit between 0 and 2!')
			i += step
			file.seek(512 * i)
	# print()
	return restart, falseBlock

############################################################################################################
# this function returns the number of 512 byte blocks the size of the drive can be divided into, which
# will be needed for the checking routine

def getDeviceSize(device):
	p1 = subprocess.Popen(["blockdev", "--getsize64", device], stdout=PIPE)
	blocks = p1.stdout.read()
	p1.stdout.close()

	return blocks

############################################################################################################
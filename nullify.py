#!/usr/bin/env python3
# coding=utf-8

###########################################################################################################################################################
###########################################################################################################################################################
# This tool provides the functionality to invoke a nulling process of a selected (external) hard drive. Afterwards,
# a check will be done to determine whether the nulling process has been successful. Finally, a report (html
# and pdf) is created, which can optionally be printed.
###########################################################################################################################################################
# The tool consists of three files: nullify.py, __checking.py and __report.py
# Please read the README before use!
###########################################################################################################################################################
###########################################################################################################################################################

"""
This Python script offers the ability to erase hard drives forensically sound.
After the nulling process, the hard drive will be checked to ensure that the
process ended successfully. Finally, a report (HTML as well as PDF) will be
created, which can optionally be printed.
"""

__version__ = '2.3.7'
__date__ = '"April 2017"'


import time
from time import localtime
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
import signal
import sys
from sys import stdout
import os
import distutils.spawn
import re
import math
import shlex

modules = []

###########################################################################################################################################################
###########################################################################################################################################################
# this function is the main function of the tool
# it will guide the user through choosing a drive, nulling, checking, and reporting


def main():
	precourse()
	dependency_check()

	print('\033[1m\033[37m###############################################################################')
	print()

	while True:
		# accept only characters (upper/lower)
		name = input('\033[0mUser: \033[1m\033[37m')
		if not name or not re.match("^[a-zA-Z]+\s{0,1}[a-zA-Z]*", name) or name.isspace():
			print('\033[91mInvalid input! Please try again.')
			print()
		else:
			break
			

	while True:
		# accept only characters (upper/lower) and digits
		dtID = input('\033[0mCase number (this will be used when naming the report file): \033[1m\033[37m')
		if not dtID or not re.match("^\w+\s{0,1}[\w\W]*$", dtID) or dtID.isspace():
			print('\033[91mInvalid input! Please try again.')
			print()
		else:
			break
	print()
	print('\033[1m\033[37m###############################################################################')

	# blocksOkay = False
	while(True):
		print()
		print('\033[0mConnect the hard drive now (again) and confirm with <ENTER>. ' \
			+ '(the program will\nwait an additional 3 seconds to ensure the device is ready)\n')

		input('Waiting for user input... ')
		for i in range(1,4):
			print('\033[1m\033[37m' + str(i) + '\033[0m')
			time.sleep(1)

		diskToNull, attributes, index = chooseDisk()

		print('\033[1m\033[37m###############################################################################\033[0m')
		print()

		# blocks = __checking.getDeviceSize('/dev/' + attributes[0][index]) / 512
		# deviceSize = modules[1].getDeviceSize('/dev/' + attributes[0][index])
		deviceSize = attributes[4][index]
		blocks = deviceSize
		try:
			blocks = int(blocks) / 512
			break
		except ValueError as ex:
			print("\033[91mError: The size of the hard drive could not be determined.\033[0m")
			blocks = 0
			print()
			print("Program will terminate now, as it can not perform properly.")
			sys.exit()

	whichCheck = modules[1].chooseCheckType(blocks)	

	falseBlock = False
	restart = 1 # default is to terminate the program
	while True:
		print('\033[1m\033[37m###############################################################################')
		print()
		confirm(attributes, index, whichCheck)
		duration = nulling(diskToNull, attributes, index, deviceSize)
		print('\033[1m\033[37m###############################################################################')
		print()
		
		restart, falseBlock = modules[1].checkRoutine('/dev/' + attributes[0][index], blocks, whichCheck)
		if restart == 0 and falseBlock == False:
			print('/dev/\033[1m\033[37m' + attributes[0][index] + ' \033[0;32mhas been successfully nulled and checked.\033[0m')
		elif restart == 0 and falseBlock == True:
			print('/dev/\033[1m\033[37m' + attributes[0][index] + ' \033[0;91mhas not been successfully nulled, since at least one block was\ndetermined to not being zero.\033[0m')
		elif restart == 'skipped':
			print('/dev/\033[1m\033[37m' + attributes[0][index] + ' \033[0;32mhas been successfully nulled \033[91mBUT NOT CHECKED!\033[0m')
		elif restart == 1:
			sys.exit('Program will terminate now.\033[0m')
		elif restart == 2:
			continue

		# in case the report contains false information about the device, offer the possibility to change it
		print()
		print('\033[1m\033[37m###############################################################################\033[0m')
		print()
		attributes, dtID, name = modules[0].alterReport(name, dtID, duration, attributes, index)
		print()
		print('\033[1m\033[37m###############################################################################')

		reportFile = modules[0].createReport(name, dtID, duration, attributes, index, restart, falseBlock)
		print()

		while True:
			printReport = input("Do you want to print the report now? (y/n) ")
			# accept only, if printReport matches y or n
			if not printReport or printReport.isspace() or not re.match("^[yn]$", printReport):
				print('\033[91mInvalid input! Please try again.\033[0m')
				print()
			else:
				if printReport == 'y':
					os.system("lp " + reportFile)
				else:
					print('You can find the report in ' + reportFile)
				break
		print()
		print('Program will terminate now.\033[0m')
		sys.exit()

###########################################################################################################################################################
# this function provides the user the ability to choose a disk that will be nullified
# and returns the chosen disk

def chooseDisk():
	print()
	print('The following hard drives are available for erasing. Note that /dev/sda is\nbeing omitted due to safety reasons!')
	print()

	attributes = False
	while attributes == False:
		attributes = listDevices()
	print()

	print('Please note that before creating the report, you will have the opportunity to\nalter the report information (e.g., model or serial number).')
	print()

	while True:
		diskToNull = input('Choose a hard drive by entering the device name (sdb, sdc, ...): \033[1m\033[37m')

		if diskToNull not in attributes[0]:
			print('\033[91mNot found...\033[0m')
			print('Please choose again.')
		else:
			index = attributes[0].index(diskToNull)
			break
		print()
	print()

	return diskToNull, attributes, index

###########################################################################################################################################################
# this function will list all available devices using 'hdparm -I <device>' and adds
# the attributes 'logical name', 'model', 'serial' and 'size to  seperate lists,
# and returns a list called 'attributes' containing the previously mentioned lists

def listDevices():
	attributes = []
	logicalNamesfdisk = []
	modelshdparm = []
	serialshdparm = []
	sizesfdisk = []
	bytesfdisk = []

	out = check_output(['fdisk', '-l'])
	sizes = re.findall('\/dev\/sd[b-z]:.*ytes', out.decode('latin-1'))
	if sizes:
		for entry in sizes:
			device = entry.split()
			# get only device name in form of sdX
			# omit sda out of safety reasons
			device[0] = re.search('sd[b-z]', device[0]).group(0)

			print("\tName: \033[1m\033[37m", end='')
			# add new array entry and initialize with error value to ensure that for every device an entry exists
			# if for some reason for some devices, e.g., the size can not be determined, this will be displayed
			logicalNamesfdisk.append("could not determine logical name")
			modelshdparm.append("could not determine model")
			serialshdparm.append("could not determine serial")
			sizesfdisk.append("could not determine size")
			bytesfdisk.append("could not determine size")
			# suppress space between two print statements
			sys.stdout.softspace = 0
			# print sdb, sdc etc. in bold white
			print('/dev/' + device[0] + '\033[0m'),
			logicalNamesfdisk[len(logicalNamesfdisk) - 1] = device[0]
			deviceName = '/dev/' + device[0]

			try:
				hdparm_output = check_output(['hdparm', '-I', deviceName]).decode('latin-1')

				match = 'could not determine model'
				print("\tModel Number: ", end='')
				if "Model Number" in hdparm_output:
					match = re.search('(?<=Model Number\:).*', hdparm_output)
					if match:
						match = match.group(0).strip()
					try:
						match.encode('ascii')
					except UnicodeEncodeError as e:
						match = "could not determine model"
					modelshdparm[len(modelshdparm) - 1] = match
				print(match)

				match = "could not determine serial"
				print("\tSerial Number: ", end='')
				# check if output contains both Serial Number and Media Serial Num
				if "Serial Number" and "Media Serial Num" in hdparm_output:
					# first, extract Serial Number and strip it if it's not None
					match = re.search('(?<=Serial Number\:).*', hdparm_output)
					if match:
						match = match.group(0).strip()
						# if it is just garbage and not a proper serial number
						# extract Media Serial Num and strip it if it's not None
						try:
							match.encode('ascii')
						except UnicodeEncodeError as e:
							match = re.search('(?<=Media Serial Num\:).*', hdparm_output)
							if match:
								match = match.group(0).strip()
								# if it's just garbage, set serial accordingly
								try:
									match.encode('ascii')
								except UnicodeEncodeError as ex:
									match = "could not determine serial"
				# else if output only contains Serial Number
				elif "Serial Number" in hdparm_output:
					# extract serial and strip it if it's not None
					match = re.search('(?<=Serial Number\:).*', hdparm_output)
					if match:
						match = match.group(0).strip()
						# if it's just garbage, set serial accordingly
						try:
							match.encode('ascii')
						except UnicodeEncodeError as e:
							match = "could not determine serial"
				# else if output only contains Media Serial Num
				elif "Media Serial Num" in hdparm_output:
					# extract serial and stript it if it's not None
					match = re.search('(?<=Media Serial Num\:).*', hdparm_output)
					if match:
						match = match.group(0).strip()
						# if it's just garbage, set serial accordingly
						try:
							match.encode('ascii')
						except UnicodeEncodeError as e:
							match = "could not determine serial"
				serialshdparm[len(serialshdparm) - 1] = match
				print(match)

				match = 'could not determine size'
				print("\tDevice Size: ", end='')
				size = device[1] + ' ' + device[2] + ' ' + device[3] + ' ' + device[4]
				sizesfdisk[len(sizesfdisk) - 1] = size
				print(size)

				bytesfdisk[len(bytesfdisk) - 1] = device[3]

				print()
				attributes.append(logicalNamesfdisk)
				attributes.append(modelshdparm)
				attributes.append(serialshdparm)
				attributes.append(sizesfdisk)
				attributes.append(bytesfdisk)

			except UnicodeDecodeError as ude:
				print()
				print(ude)
				print('Error querying hdparm.')
				print('Trying again.')
				print()
				return False

	if not attributes:
		print('Could not find any device. Please connect a device and restart the tool.')
		sys.exit()

	return attributes

###########################################################################################################################################################
# confirmation

def confirm(attributes, index, checkNow):
	print('\033[0mPlease confirm the following operations: ')
	print()
	print('The following device will be irreversibly erased:')
	print()
	print("\t\033[37m\033[1m/dev/" + attributes[0][index] + '\n\t' + attributes[1][index] + '\n\t' + attributes[2][index] + '\n\t' + attributes[3][index] + '\033[0m')
	print()
	if checkNow == 0:
		print("Afterwards, a Full Check will be done.")
	elif checkNow == 1:
		print("Afterwards, a Quick Check will be done.")
	elif checkNow == 2:
		print("Afterwards, no Check will be done.")
	else:
		print("Afterwards, you can choose what kind of check to do.")
	print()
	confirm = input('To confirm, type \033[37m\033[1m' + attributes[0][index] + '\033[0m. Invalid input will terminate the program due to safety\nreasons.\n' + \
						'Input: \033[1m\033[37m')
	if confirm != attributes[0][index]:
		print()
		print('Operation not confirmed by the user.')
		print('Program will terminate now.\033[0m')
		sys.exit()


###########################################################################################################################################################
# this function povides the nulling routine
# for this, the unix command 'dd' is being leveraged

def nulling(device, attributes, index, deviceSize):
	print()
	print('\033[1m\033[37m###############################################################################')
	print()

	beginDay = time.strftime("%d.%m.%Y")
	beginTime = time.strftime("%H:%M:%S %Z", time.localtime())
	print('\033[1m\033[37mBegin: ' + beginDay + ', ' + str(beginTime))
	print('\033[1m\033[37mnulling...')
	print()


	# set block size for dd
	# if device size can be divided by 1024*1024, use bs=1M
	# else use bs=1M for most of the device then switch to bs=512
	# set number of blocks accordingly

	bs = '1M'
	blocks = 0
	remaining = 0
	seek = 0
	blocksProgress = 1
	count = ''
	deviceSize = int(deviceSize)

	cmd = "dd if=/dev/zero of=/dev/" + attributes[0][index] + " bs=" + bs + " seek=" + str(int(seek)) + " " + count

	# if deviceSize can be divided by 1024*1024 (1M) without rest, do only that
	# otherwise, calculate remaining blocks of size 512
	# deviceSize is being extracted from fdisk -l and must be a multiple of 512
	blocks = int(deviceSize / (1024*1024))
	if deviceSize % (1024*1024) != 0:
		remaining = int((deviceSize % (1024*1024)) / 512)
		blocksProgress = (int(blocks) * 1024*1024) / deviceSize

	# let user choose between three nulling types, if it can't be completely nulled using a block size of 1M
	nullType = 1 
	print("\033[0mChoose nulling type: ")
	print()
	print("0 ----> Use block size of 1M for " + str(blocks) + " 1M blocks, and block size of 512 for the\n\tremaining " + str(remaining) + " 512 Byte blocks.")
	print("1 ----> Use block size of 1M for the whole device (" + str(int(deviceSize / (1024*1024)) + 1) + " 1M Byte blocks).")
	print("2 ----> Use block size of 512 for the whole device (" + str(int(deviceSize / 512)) + " 512 Byte blocks).")
	print()
	while True:
		nullType = input('\033[0mInput: \033[1m\033[37m')
		if not nullType or not re.match("^[0-2]$", nullType) or nullType.isspace():
			print('\033[91mInvalid input! Please try again.\033[0m')
		else:
			break
	print()

	if nullType == '2':
		blocks = int(deviceSize / 512)
		remaining = 0
		bs = '512'
	elif nullType == '1':
		remaining = 0
	elif nullType == '0':
		count = 'count=' + str(int(blocks))

	print('Starting to null using a block size of ' + bs + ' for ' + str(int(blocks)) + ' blocks (' + str(math.floor(blocksProgress * 100)) + '%)')
	print()
	while True:
		print('dd if=/dev/zero of=/dev/' + attributes[0][index] + ' bs=' + bs + ' seek=' + str(int(seek)) + ' ' + count)
		dd = Popen(shlex.split(cmd), stderr=PIPE)

		while dd.poll() is None: # check if child process has terminated
			time.sleep(5)
			dd.send_signal(signal.SIGUSR1)
			while 1:
				output = dd.stderr.readline()
				output = output.decode('latin-1')
				if 'bytes' in output:
					bytesWritten = output.split()[0]
					try:
						progress = output.strip() + ' ===> ' + str(math.floor((float(bytesWritten) / int(deviceSize)) * 100)) + '%'
						print('\033[K' + progress, end='\r') # clear line, then print, then go back to previous line (the line, where just printed to)
					except ValueError as ex:
						print('\033[KError receiving output from dd. Continuing nulling process.', end='\r')
					break
		
		if remaining != 0:
			print()
			# set seek to skip already nulled blocks
			# but adjust it a little to avoid a possible gap
			# adjust variable blocks accordingly
			seek = (int(blocks) * (1024 * 1024)) / 512
			if(seek > 100 * 512):
				seek -= 100 * 512
				blocks = remaining + (100 * 512)
			else:
				blocks = seek
				seek = 0
			bs = '512'
			blocks = remaining
			blocksProgress = int(blocks * 512) / deviceSize
			print()
			print('Continuing to null using a block size of ' + bs + ' for ' + str(int(blocks)) + ' blocks (' + str(math.ceil(blocksProgress * 100)) + '%)')
			print()
			cmd = "dd if=/dev/zero of=/dev/" + attributes[0][index] + " bs=" + bs + " seek=" + str(int(seek)) + " " + count
			remaining = 0
		else:
			break

	endDay = time.strftime("%d.%m.%Y")
	endTime = time.strftime("%H:%M:%S %Z", time.localtime())
	print()
	print('\033[1m\033[37mEnd: ' + endDay + ', ' + endTime)
	print('\033[0;32m\033[1mNulling ended successfully!')
	print()

	duration = []
	duration.append(beginDay)
	duration.append(beginTime)
	duration.append(endDay)
	duration.append(endTime)

	return duration

###########################################################################################################################################################
# this function checks whether necessary dependencies are available
# if not, the program will terminate

def dependency_check():
	print('Checking dependencies...')

	moduleNames = ['__report', '__checking', 'weasyprint']
	# tools = ['lsblk', 'dd', 'fdisk', 'lp', 'cupsd', 'wkhtmltopdf', 'hdparm', 'weasyprint']
	tools = ['lsblk', 'dd', 'fdisk', 'lp', 'cupsd', 'hdparm', 'weasyprint']

	# check for tools that are used for this tool
	for tool in tools:
		installed = distutils.spawn.find_executable(tool)
		if installed == None:
			print()
			print('\033[91m' + tool + ' is not installed, but required for this program to fully do its work.\nAfter installing, restart the program.\033[0m')
			print()
			print('Program will terminate now.')
			sys.exit()

	# check for python libraries that are used for this tool
	for module in moduleNames:
		try:
			modules.append(__import__(module, globals={"__name__": __name__}))
		except ImportError as ex:
			# print(ex)
			print('\033[91m' + module + ' is not installed, but required for this program to fully do its work.\nAfter installing, restart the program.\033[0m')
			print()
			print('Program will terminate now.')
			sys.exit()
	print('Dependency check was succesfull.')
	print()

###########################################################################################################################################################

def precourse():
	print("""\033[0;32m\033[1m
###############################################################################
###############################################################################
####                                                                       ####
####     ###   ##  ##    ##  ##       ##       ##  ###   ##     ####       ####
####     ####  ##  ##    ##  ##       ##       ##  ####  ##   ##           ####
####     ## ## ##  ##    ##  ##       ##       ##  ## ## ##  ##   ####     ####
####     ##  ####  ##    ##  ##       ##       ##  ##  ####   ##    ##     ####
####     ##   ###    ####    #######  #######  ##  ##   ###     ####       ####
####                                                                       ####
####                                                                       ####
####                ########    ####        ####     ##                    ####
####                   ##     ##    ##    ##    ##   ##                    ####
####                   ##    ##      ##  ##      ##  ##                    ####
####                   ##     ##    ##    ##    ##   ##                    ####
####                   ##       ####        ####     #######               ####
####                                                                       ####
####                            \033[22mNulling Tool v"""+__version__+"""\033[1m                        ####
####                                                                       ####
###############################################################################
###############################################################################
\033[37m
###############################################################################

This Python script offers the ability to erase hard drives forensically sound.
After the nulling process, the hard drive will be checked to ensure that the
process ended successfully. Finally, a report (HTML as well as PDF) will be
created, which optionally can then be printed.

###############################################################################
  \033[m""")

###########################################################################################################################################################

if __name__ == '__main__':
    main()
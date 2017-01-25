#!/usr/bin/env python3
import os
import sys
import re
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time
from time import localtime
import signal
import distutils.spawn
import math
from sys import stdout
from tempfile import SpooledTemporaryFile as tempfile


def main():
	# print(os.path.dirname(os.path.realpath(__file__)))
	path = '/dev/sdc'
	# path = '/home/leo/test_random'
	# bs = '1M'
	# seek = 0
	# blocks = 100
	zeros = '00' * (1024 * 1024)


	deviceSize = 4005560320

	bs = '1M'
	blocks = 0
	remaining = 0
	skip = 0
	deviceSize = int(deviceSize)
	count = 1

	# if deviceSize can be divided by 1024*1024 (1M) without rest, do only that
	# otherwise, calculate remaining blocks of size 512
	# deviceSize is being extracted from fdisk -l and must be a multiple of 512
	blocks = int(deviceSize / (1024*1024))
	if deviceSize % (1024*1024) != 0:
		remaining = int((deviceSize % (1024*1024)) / 512)
		blocksProgress = (int(blocks) * 1024*1024) / deviceSize
	# size = 10485760
	# blocks512 = size / 512
	# blocks1M = size / (1024*1024) # 3820
	# blocks1M = int(blocks1M)
	# skip = 0
	# count = 1
	# i = 1

	# foo = 100

	# blocks1M = 220

	# while foo > 0:
	# 	dd = subprocess.Popen(['dd', 'if=' + path, 'bs=' + str(bs), 'seek=' + str(seek), 'count=' + str(count)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	# 	od = subprocess.check_output(('od'), stdin=dd.stdout)
	# 	# od.poll()
	# 	output = dd.stderr.readline()
	# 	output = output.decode('latin-1')
	# 	print(output)
	# 	print(od.decode('latin-1'))
	# 	foo = foo - 1

	blocks = 1
	bs = 1024*1024
	while skip != blocks:
		print('skip: ' + str(skip))
		# print('round ' + str(i) + ': ' + str(blocks1M) + ', ' + str(count) + ', ' + str(skip))
		print('dd if=' + path + ' bs=' + str(bs) + ' skip=' + str(skip) + ' count=' + str(count))

		# # dd = subprocess.Popen(['dd', 'if=/dev/zero', 'of=test_zero2', 'bs=' + str(bs), 'seek=' + str(seek), 'count=' + str(count)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		dd = subprocess.Popen(['dd', 'if=' + path, 'bs=' + str(bs), 'skip=' + str(skip), 'count=' + str(count)], stdout=PIPE, stderr=STDOUT)
		output = dd.stdout.readline()
		foo = re.search(b"(\\x00)*", output).group(0)
		# foo = output
		print('##')
		# print(foo)
		print('##')

		# p = Popen(['grep', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
		# grep_stdout = p.communicate(input=foo)[0]
		# print('##')
		# print(grep_stdout)
		# print('##')

		f = tempfile()
		f.write(foo)
		f.seek(0)
		# print Popen(['/bin/grep','f'],stdout=PIPE,stdin=f).stdout.read()


		# ^0{7}\s(0{6}\s){8}\*\s\d0{2}\d0{3}$

		# foo = None
		# with open(grep_stdout, "r+") as f:
		od = subprocess.check_output(('od'), stdin=f)
		f.close()

		if re.search("^0{7}\s(0{6}\s){8}\*\s\d{7}$", od.decode()):
			print('empty')
		else:
			print('nope')

		# print(od.decode())
		


		# od.stdin = ""
		# od.communicate()[0]
		# output2 = od
		# print('##')
		# # print(foo.count('\x00'))
		# print(foo)
		# print('##')


		# od = subprocess.check_output(('od'), stdin=dd.stdout)
		# # # od.poll()
		# while dd.poll is None:
		# print(output)
		# pattern = re.compile(b"\\x00")
		# foo = re.search(b"(\\x00)*", output)
		# print(foo.group(0).decode())
		# print(output.count(b'\x00'))
		# output = output.decode('latin-1')
		# # print(output)
		# while 1:
		# 	output = dd.stderr.readline()
		# 	output = output.decode('latin-1')
		# 	if 'bytes' in output:
		# 		bytesWritten = output.split()[0]
		# 		try:
		# 			# progress = output.strip() + ' ===> ' + str(math.floor((float(bytesWritten) / int(deviceSize)) * 100)) + '%'
		# 			progress = output.strip() + ' ===>'
		# 			print('\033[K' + progress, end='\r') # clear line, then print, then go back to previous line (the line, where just printed to)
		# 			# stdout.write('\r%s' %progress)
		# 		except ValueError as ex:
		# 			print('\033[K' + str(ex), end='\r')
		# 			# stdout.write('\r%s' %ex)
		# 		break
		# 	# stdout.write('\n')
		# 	# print(dd.stder
		# # # print(od.decode('latin-1'))
		# # if re.match('^(0{7,7}\s)(0{6,6}\s){8,8}\*', od.decode('latin-1')):
		# # 	print('y ')
		# # else:
		# # 	print('n ')

		skip += 1


		# print('fo')
		# while dd.wait() is None:
		# 	# time.sleep(1)
		# 	dd.send_signal(signal.SIGUSR1)
		# 	while 1:
		# 		print(od.decode('latin-1'))
		# 		output = dd.stderr.readline()
		# 		output = output.decode('latin-1')
		# 		if 'bytes' in output:
		# 			bytesWritten = output.split()[0]
		# 			try:
		# 				# progress = output.strip() + ' ===> ' + str(math.floor((float(bytesWritten) / int(deviceSize)) * 100)) + '%'
		# 				progress = output.strip() + '===>'
		# 				print('\033[K' + progress, end='\r') # clear line, then print, then go back to previous line (the line, where just printed to)
		# 				# stdout.write('\r%s' %progress)
		# 			except ValueError as ex:
		# 				print('\033[K' + str(ex), end='\r')
		# 				# stdout.write('\r%s' %ex)
		# 			break
		# 	stdout.write('\n')
		# 	print(dd.stderr.read(), end='\r')

		# if blocks1M - count > 0:
		# 	blocks1M = blocks1M - count
		# 	# seek = seek + 
		# else:
		# 	count = blocks1M
		# 	blocks1M = 0
		# skip = skip + count
		# # print('after')
		# # print('round ' + str(i) + ': ' + str(blocks1M) + ', ' + str(count) + ', ' + str(seek))
		# # print()

		# i = i + 1


		# while dd.poll() is None:
		# 	time.sleep(3)
		# 	dd.send_signal(signal.SIGUSR1)
		# 	while 1:
		# 		print(od.decode('latin-1'))
		# 		output = dd.stderr.readline()
		# 		output = output.decode('latin-1')
		# 		if 'bytes' in output:
		# 			bytesWritten = output.split()[0]
		# 			try:
		# 				# progress = output.strip() + ' ===> ' + str(math.floor((float(bytesWritten) / int(deviceSize)) * 100)) + '%'
		# 				progress = output.strip() + '===>'
		# 				print('\033[K' + progress, end='\r') # clear line, then print, then go back to previous line (the line, where just printed to)
		# 				# stdout.write('\r%s' %progress)
		# 			except ValueError as ex:
		# 				print('\033[K' + str(ex), end='\r')
		# 				# stdout.write('\r%s' %ex)
		# 			break
		# 	stdout.write('\n')
		# 	print(dd.stderr.read(), end='\r')



	# dd.wait()
	# print('#######')
	# print(od.decode('latin-1'))
	# print('#######')
	# print(dd.stderr.read().decode('latin-1'))


	# dd = Popen(['dd', 'if=' + path, 'bs=' + bs, 'seek=' + str(int(seek)), 'count=' + str(int(blocks))], stderr=PIPE)
	# 	while dd.poll() is None: # check if child process has terminated
	# 		time.sleep(5)
	# 		dd.send_signal(signal.SIGUSR1)
	# 		while 1:
	# 			output = dd.stderr.readline()
	# 			output = output.decode('latin-1')
	# 			if 'bytes' in output:
	# 				bytesWritten = output.split()[0]
	# 				try:
	# 					progress = output.strip() + ' ===> ' + str(math.floor((float(bytesWritten) / int(deviceSize)) * 100)) + '%'
	# 					print('\033[K' + progress, end='\r') # clear line, then print, then go back to previous line (the line, where just printed to)
	# 					# stdout.write('\r%s' %progress)
	# 				except ValueError as ex:
	# 					print('\033[K' + ex, end='\r')
	# 					# stdout.write('\r%s' %ex)
	# 				break
	# 	stdout.write('\n')
	# 	print(dd.stderr.read()),

	# image = '~/foo'
	# image = os.path.expanduser('~/foo')
	# with open(image) as f:
	# 	content = f.readlines()
	# 	print(content)

	# path = os.path.expanduser('~/ffkkaa')
	# print(path)
	# if not os.path.exists(path):
	# 	os.system("mkdir " + path)
	# 	print('foo')
	# print('abc')
	# for x in ['abc', 1]:
		# print('\033[K', end='\r')

		# print('\033[K' + str(x), end='\r')

		# stdout.write(str(x))
		# sys.stdout.write("\033[K")
    	# print '{}\r'.format(x),
	# print('foo')
	# print('\x1b[2K\r'),
	# sys.stdout.write("\033[K") # Clear to the end of line

	# print('f')

	# dd = subprocess.getoutput('dd if=/dev/zero of=/dev/sdb bs=1M')
	# dd = subprocess.Popen(['dd', 'if=/dev/zero', 'of=/dev/sdc', 'bs=1M'], stderr=PIPE)
	# while dd.poll() is None: # check if child process has terminated
	# 	time.sleep(5)
	# 	dd.send_signal(signal.SIGUSR1)
	# 	while 1:
	# 		output = dd.stderr.readline()
	# 		# output = output.split()
	# 		output = output.decode('ascii')
	# 		# print(output.decode('ascii'))
	# 		# print()
	# 		# if 'records in' in output:
	# 		# 	print(output[:output.index('+')], 'records', end='\r'),
	# 		if 'bytes' in output:
	# 			bytesWritten = output.split()[0]
	# 			try:
	# 				progress = output.strip() + ' ===> ' + str(math.floor((float(bytesWritten) / int(4005560320)) * 100)) + '%'
	# 				# print('a' + progress, end='\r')
	# 				# stdout.write("\033[K") # Clear to the end of line

	# 				# stdout.write('\r%s' %progress)
	# 				# stdout.write("\033[K") # Clear to the end of line


	# 				# stdout.flush()
	# 				# print('', end='\r')
	# 				print('\033[K' + progress, end='\r')
	# 				# print('\033[K' + output.strip() + ' ===> ' + str(math.floor((float(bytesWritten) / int(4005560320)) * 100)) + '%', end='\r'),
	# 			except ValueError as ex:
	# 				stdout.write('\r%s' %ex)
	# 				# print(ex, '\r'),
	# 			break
	# stdout.write('\n')
	# print(dd.stderr.read()),



	# foo = Popen(['ls', '-l'], stdout=subprocess.PIPE)
	# for line in foo.stdout:
		# print(line.split())

main()
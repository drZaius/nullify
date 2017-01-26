#!/usr/bin/env python3
# -*- coding: utf-8 -*-

############################################################################################################
############################################################################################################
# this file is part of the nulling tool (see nullify.py)
############################################################################################################
############################################################################################################

# import webbrowser
import time
# import pdfkit
import os
import subprocess
from weasyprint import HTML
import re

############################################################################################################
# this function creates an html as well as a pdf report of the nulling and checking process
# a report basically consists of two parts:
# at the top center, a full report is shown, which contains all necessary info for determining the device
# that was nulled as well as the case in which it was used
# furthermore, the user invoking the erasing process will be mentioned
# at the right bottom corner, a short report will be shown, containing only necessary info for determining 
# the case in which it was used
# the short report is supposed to be put on to the device

def createReport(name, digiTraceID, duration, attributes, index, checked, falseBlock):
	# image that will be shown on the report
	# change path to custom image if necessary
	scriptDir = os.path.dirname(os.path.realpath(__file__))
	image = scriptDir + '/__DigiTrace_Logo_claim.png'

	print('\033[1m\033[37mCreating report...\033[0m') 
	print

	# check if directory for reports already exists
	# create otherwise
	reports = scriptDir + '/reports'
	if not os.path.exists(reports):
		os.system("mkdir " + reports)

	# open html report file for writing
	reportName = reports + '/nulling_report_' + str(digiTraceID) + '_' + time.strftime("%d.%m.%Y_%H:%M:%S_%Z", time.localtime())
	f = open(reportName + '.html', 'w')

	# check was not skipped and every block was zero
	status = ''
	shortStatus = ''
	if checked != 'skipped' and falseBlock == False:
		shortStatus = '<i>Vollst&auml;ndig genullt + unformatiert + gepr&uuml;ft</i><br><br>'
		status = '<i>Hiermit best&auml;tigt DigiTrace, dass nachfol-<br>gender Datentr&auml;ger vollst&auml;ndig IT-foren-<br>sisch gel&ouml;scht und gepr&uuml;ft wurde:</i>'
	# check was not skipped, but at least one block was not zero
	elif checked != 'skipped' and falseBlock == True:
		shortStatus = '<i>Nullen war fehlerhaft</i><br><br>'
		status = '<i>Hiermit best&auml;tigt DigiTrace, dass nachfol-<br>gender Datentr&auml;ger nicht vollst&auml;ndig IT-foren-<br>sisch gel&ouml;scht und gepr&uuml;ft wurde:</i>'
	else:
		shortStatus = '<i>Vollst&auml;ndig genullt + unformatiert + ungepr&uuml;ft</i><br><br>'
		status = '<i>Hiermit best&auml;tigt DigiTrace, dass nachfol-<br>gender Datentr&auml;ger nicht vollst&auml;ndig IT-foren-<br>sisch gel&ouml;scht und gepr&uuml;ft wurde:</i>'




	# headline of full report
	top = \
	'<h1>' \
	+ '<b>L&ouml;schbest&auml;tigung</b>'

	# body of short report
	# depending on whether a check has been done, mention this on the report
	confirmation = '<p>' \
			+ status \
			+ '</p>'
	shortReport = '<p style="margin:0">' \
			+ shortStatus \
			+ 'Fall: ' + str(digiTraceID) + '<br>' \
			+ 'Beginn: ' + duration[1] + ', ' + duration[0] + '<br>' \
			+ 'Ende: ' + duration[3] + ', ' + duration[2] + '<br>' \
			+ 'DigiTrace Mitarbeiter: ' + name + '<br>' \
			+ '<br><br>'\
			+ 'Unterschrift' \
		+ '</p>'

	# full report
	fullReport = '<p>' \
			+ 'Fall: ' + str(digiTraceID) + '<br>' \
			+ 'Modell: ' + attributes[1][index] + '<br>' \
			+ 'S/N: ' + attributes[2][index] + '<br>' \
			+ 'Gr&ouml;&szlig;e: ' + attributes[3][index] + '<br>' \
			+ 'Beginn: ' + duration[1] + ', ' + duration[0] + '<br>' \
			+ 'Ende: ' + duration[3] + ', ' + duration[2] + '<br>' \
			+ 'DigiTrace Mitarbeiter: ' + name + '<br>' \
			+ '<br><br>'\
			+ 'Unterschrift' \
		+ '</p>'

	# beginning of html DOM tree
	# adjust size of image if necessary
	tree = \
	"""<!DOCTYPE html>
		<html>
			<head></head>
			<body style="background-color:#ffffff">
				<div style="margin-left: 1.5in;">
					<div>
						<img src=""" + image + """ alt="DigiTrace_Logo" style="max-width:300px">
					</div>
					<div id="top">
						""" + top + """
					</div>
					<div id="confirmation">
						""" + confirmation + """
					</div>
					<div id="main">
						""" + fullReport + """
					</div>
				</div>
				<div style="position: absolute; width: 510px; border: 1px solid #000; padding: 5px; bottom: -75px; left: 200px">
					<div style="float:right;">
						<img src=""" + image + """ alt="DigiTrace_Logo" style="max-width:145px">
					</div>
					<div>
						""" + shortReport + """
					</div>
				</div>
			</body>
		<html>
	"""

	# write html file
	f.write(tree)
	f.close()

	# convert html to pdf
	HTML(reportName + '.html').write_pdf(reportName + '.pdf')	

	return reportName + '.pdf'

############################################################################################################
# this function provides the ability to alter the information that will be mentioned in the report

def alterReport(name, digiTraceID, duration, attributes, index):
	print('The following will be included in the report:')
	print()
	print('\t\033[1m\033[37mFall: ' + digiTraceID)
	print('\tModell: ' + attributes[1][index])
	print('\tS/N: ' + attributes[2][index])
	print('\tGröße: ' + attributes[3][index])
	print('\tBeginn: ' + duration[1] + ', ' + duration[0])
	print('\tEnde: ' + duration[3] + ', ' + duration[2])
	print('\tDigiTrace Mitarbeiter: ' + name)
	print('\033[0m')
	option = 0
	print('If necessary, this information can now be altered.')
	print()
	print('Please choose an option.')
	print('\t0: data is correct, create report')
	print('\t1: Fall')
	print('\t2: Modell')
	print('\t3: S/N')
	print('\t4: Größe')
	print('\t5: DigiTrace Mitarbeiter')
	print()
	while True:
		option = input('Input: ')
		if not option or not re.match("^[0-9]$", option) or option.isspace():
			print('Invalid input.')
			print()
		elif int(option) == 0:
			break
		else:
			if int(option) == 1:
				while True:
					case = input('Enter case number: ')
					if not case or not re.match("^[\w]{1,}$", case) or case.isspace():
						print('Invalid input.')
						print()
					else:
						digiTraceID = case
						break
			elif int(option) == 2:
				while True:
					model = input('Enter model: ')
					if not model or not re.match("^[\w]{1,}$", model) or model.isspace():
						print('Invalid input.')
						print()
					else:
						attributes[1][index] = model
						break
			elif int(option) == 3:
				while True:
					serial = input('Enter serial: ')
					if not serial or not re.match("^[\w]{1,}$", serial) or serial.isspace():
						print('Invalid input.')
						print()
					else:
						attributes[2][index] = serial
						break
			elif int(option) == 4:
				while True:
					size = input('Enter size (e.g., 1 TB, 500 GiB, 320 GB, 200 MB, 1234 Byte, ...: ')
					if not size or not re.match("^[\d]{1,}\s[a-zA-Z]{1,}$", size) or size.isspace():
						print('Invalid input.')
						print()
					else:
						attributes[3][index] = size
						break
			elif int(option) == 5:
				while True:
					employee = input('Enter name: ')
					if not employee or not re.match("^[A-Za-z]{1,}$", employee) or employee.isspace():
						print('Invalid input.')
						print()
					else:
						name = employee
						break
			print('Successfully changed.')
			print()
			print('Please choose an option.')

	return attributes, digiTraceID, name
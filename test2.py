#!/usr/bin/env python3
import os
import sys
import re
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
import time
from time import localtime
import signal
import distutils.spawn
import math
from sys import stdout
from weasyprint import HTML, CSS
import pdfkit






def createReport(name, digiTraceID, duration, attributes, index, checked):
	# image that will be shown on the report
	# change path to custom image if necessary
	image = '../__DigiTrace_Logo_claim.png'

	print('\033[1m\033[37mCreating report...\033[0m')
	print

	# check if directory for reports already exists
	# create otherwise
	if not os.path.isdir("reports"):
		os.system("mkdir reports")

	# open html report file for writing
	f = open('reports/nulling_report_' + str(digiTraceID)+ '.html', 'w')


	# headline of full report
	top = \
	'<h1>' \
	+ '<b>L&ouml;schbest&auml;tigung</b>'

	# body of short report
	# depending on whether a check has been done, mention this on the report
	if checked != 'skipped':
		confirmation = '<p>' \
		+ '<i>Hiermit best&auml;tigt DigiTrace, dass nachfol-<br>gender Datentr&auml;ger vollst&auml;ndig IT-foren-<br>sisch gel&ouml;scht und gepr&uuml;ft wurde:</i>' \
		+ '</p>'
		shortReport = '<p style="margin:0">' \
			+ '<i>Vollst&auml;ndig genullt + unformatiert + gepr&uuml;ft</i><br><br>' \
			+ 'Fall: ' + str(digiTraceID) + '<br>' \
			+ 'Beginn: ' + duration + ', ' + duration + '<br>' \
			+ 'Ende: ' + duration + ', ' + duration + '<br>' \
			+ 'DigiTrace Mitarbeiter: ' + name + '<br>' \
			+ '<br><br>'\
			+ 'Unterschrift' \
		+ '</p>'
	else:
		confirmation = '<p>' \
		+ '<i>Hiermit best&auml;tigt DigiTrace, dass nachfol-<br>gender Datentr&auml;ger vollst&auml;ndig IT-foren-<br>sisch gel&ouml;scht, aber nicht gepr&uuml;ft wurde:</i>' \
		+ '</p>'
		shortReport = '<p style="margin:0">' \
			+ '<i>Vollst&auml;ndig genullt + unformatiert + ungepr&uuml;ft</i><br><br>' \
			+ 'Fall: ' + str(digiTraceID) + '<br>' \
			+ 'Beginn: ' + duration + ', ' + duration + '<br>' \
			+ 'Ende: ' + duration + ', ' + duration + '<br>' \
			+ 'DigiTrace Mitarbeiter: ' + name + '<br>' \
			+ '<br><br>'\
			+ 'Unterschrift' \
		+ '</p>'

	# full report
	fullReport = '<p>' \
			+ 'Fall: ' + str(digiTraceID) + '<br>' \
			+ 'Modell: ' + attributes + '<br>' \
			+ 'S/N: ' + attributes + '<br>' \
			+ 'Gr&ouml;&szlig;e: ' + attributes + '<br>' \
			+ 'Beginn: ' + duration + ', ' + duration + '<br>' \
			+ 'Ende: ' + duration + ', ' + duration + '<br>' \
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
					<div style="float: right;">
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

	html = 'reports/nulling_report_bar.html'
	HTML('reports/nulling_report_testCase.html').write_pdf('/home/leo/Coding/Scripts/Python/nuller_beta/reports/test2.pdf')	


	# options for converting html to pdf
	options = {
    'page-size': 'A4',
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '2.5in',
    'encoding': "UTF-8",
	}
	
	# convert html to pdf
	# pdfkit.from_url('reports/nulling_report_' + str(digiTraceID)+ '.html', 'reports/nulling_report_' + str(digiTraceID) + '.pdf', options=options)

	return 'reports/nulling_report_' + str(digiTraceID) + '.pdf'


def main():
	html = 'reports/nulling_report_bar.html'

	# CSS(html='@page { size: A3; margin: 1cm }')

	options = {
    'page-size': 'A4',
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '2.5in',
    'encoding': "UTF-8",
	}

	# HTML(html).write_pdf('/home/leo/Coding/Scripts/Python/nuller_beta/reports/test2.pdf', stylesheets=[CSS(string='@page { margin-bottom: 0in}')])	

	# pdfkit.from_url('reports/nulling_report_bar.html', 'reports/test.pdf')

	createReport('foo', 'bar', 'foo', 'foo', 'foo', 'foo')


main()
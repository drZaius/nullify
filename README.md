This Python script offers the ability to erase hard drives forensically sound by utilizing the 'dd' tool. After the nulling
process, the hard drive will be checked to ensure that the process ended successfully. Finally, a report (HTML as well as PDF)
will be created.

INFORMATION:
	version: v2.3.6
	date: January 2017

The tool currently consists of three files: nullify.py, __checking.py and __report.py

Please note that this tool uses python3 commands and syntax. It will therefore only run without errors when using python3.


Dependencies:

	fdisk,hdparm 	--> retrieving device information
	dd 	   			--> erasing the device
	cups   			--> automatic printing
	lp     			--> printing the report

	weasyprint 		--> converting html to pdf
		to install, execute the following:
			pip3.x install WeasyPrint
		weasyprint depends on libffi-dev
			apt-get install libffi-dev
		to install pip3.x, execute the following:
			apt-get install python3-pip

In order to print the PDF report directy using this tool, the following is necessary. It is assumed that the tool
is being used on a server with no X server running (e.g., Ubuntu server):

	server:
		apt-get install cups
		apt-get install cups-client
	client:
		ssh -L 1234:localhost:631 server@ip
		\# navigate to localhost:1234 in a browser --> administration --> add printer
	server:
		lpstat -a # list all available printers as configured using the web interface of cups
		lpoptions -d <PRINTERNAME> # set default printer
		\# the configuration can now be tested using the command "lp <name>.pdf"

EXECUTE:
Run the tool as root using the command ./nullify
If you encounter the error "no space left" while nulling, don't panic. The tool will continue after a while.
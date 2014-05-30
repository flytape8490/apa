from __future__ import print_function
# Python 3.x/2.7
# APAssist  -- apa.py
# v 0.1

# A tool written to aid in the generation of APA files for the
# Kodak Prinergy system, written to work for both Python 2.7 and 3x

try:							# tkinter for 3.x
	from tkinter import *
except ImportError:				# tkinter for 2.7
	from Tkinter import *
from ttk import *				# tk themes

# HOW DO I WANT DATA STORED: PICKLE, SQL, or CSV?
# EACH WOULD REQUIRE ME TO LEARN HOW EACH WORKS...
# in any case, each APA entry is going to be a classed object
# ...but then I'd have to walk each object to get the names...
# maybe store each as a list of lists? I would then need a bunch of
# slice objects - but are those available in 2.7?
# I could have a dictionary where each key is the template name and
# the value points at a class... NOPE DOESN'T WORK


# set up functions
# set up variables
# start building interface

def dupe():
	print('dupe!')
def new():
	print('new!')
def eddn():
	print('editDone!')
	btnEdDn["text"]="Done!"
def delete():
	print('delete!')
def save():
	print('save!')
def test():
	print('test!')
def halp():
	print('help!')

root=Tk()
# setup text variables
apaVar=StringVar()
apaVar.set('APA Version:\n %s'%(0))
lastModDate=StringVar()
lastModDate.set('Last Modified:\n %s'%('da/te/14'))
root.title('APAssist')
appFrame=Frame(root, padding='7 7 7 7')
appFrame.grid(column=0, row=0, sticky=(N, W, E, S))
appFrame.columnconfigure(0, weight=1)
appFrame.rowconfigure(0, weight=1)
lstTemplate=Listbox(appFrame, height=10).grid(column=0, columnspan=2, row=1, rowspan=6, sticky=(W, E))
lblApaVer=Label(appFrame, textvariable=apaVar).grid(column=0, row=0, sticky=W)
lblLstMod=Label(appFrame, textvariable=lastModDate).grid(column=1, row=0, sticky=W)

btnDupe=Button(appFrame, text='Copy a New Version', command=dupe).grid(column=3, row=0, sticky=(W, E))
btnNew=Button(appFrame, text='New Entry', command=new).grid(column=3, row=1, sticky=(W, E))
btnEdDn=Button(appFrame, text='Edit Entry', command=eddn).grid(column=3, row=2, sticky=(W, E))
btnDelete=Button(appFrame, text='Delete Entry', command=delete).grid(column=3, row=3, sticky=(W, E))
btnSave=Button(appFrame, text='Save Changes', command=save).grid(column=3, row=4, sticky=(W, E))
btnTest=Button(appFrame, text='Test', command=test).grid(column=3, row=5, sticky=(W, E))
btnHalp=Button(appFrame, text='Help', command=halp).grid(column=3, row=6, sticky=(W, E))


# load-in data
	# if no data then generate a blank set
	# happens after interface so if the apa gets huge, it won't seem
	# like it isn't launching.
	# Maybe also set up a progress bar for loading?
root.mainloop() # this is so the interface doesn't close right after launch
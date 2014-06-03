# Python 3.x/2.7
# APAssist  -- apa.py
# v 0.2

# A tool written to aid in the generation of APA files for the
# Kodak Prinergy system, written to work for both Python 2.7 and 3x

	# rather than storing each to a dictionary of classObjects, couldn't
	# I just process the xml incrementally, pulling only the namelist
	# and version/date on load, then pull the data out live for each
	# template? might get better performance on load for a large XML

import shutil, xml.etree.ElementTree as xml
try:							# tkinter for 3.x
	from tkinter import *
	from tkinter.ttk import *
except ImportError:				# tkinter for 2.7
	from Tkinter import *
	from ttk import *

class template:
	def __init__(self,offset,size):
		self.offsetX=float(offset['x'])
		self.offsetY=float(offset['y'])
		self.sizeW=float(size['width'])
		self.sizeH=float(size['height'])
		self.comment=""
class apa:
	def lModUpdate():
		import time
		apa.lMod=time.strftime('%m/%d/%Y')
	def duplicate():
		shutil.copy('templates.xml','old/templates.r%s.xml'%apa.revision) #should also copy the APA
		shutil.copy('job.apa','old/job.r%s.apa'%apa.revision) #might need to enable the symbolic link argument when reusing this to move the APA into the MCDTemplate folder
		apa.revision+=1
	def updateFields(*args):
		cName=nameList[templateBox.curselection()[0]]
		cTemp=apa.templates[cName]
		templateNameBox.delete('1.0','2.0')
		templateNameBox.insert('1.0', cName)
		offsetXBox.delete('1.0','2.0')
		offsetXBox.insert('1.0', cTemp.offsetX)
		offsetYBox.delete('1.0','2.0')
		offsetYBox.insert('1.0', cTemp.offsetY)
		sizeWBox.delete('1.0','2.0')
		sizeWBox.insert('1.0', cTemp.sizeW)
		sizeHBox.delete('1.0','2.0')
		sizeHBox.insert('1.0', cTemp.sizeH)
		commentBox.delete('1.0','2.0')
		commentBox.insert('1.0', cTemp.comment)
		

# DATA READ-IN
library=xml.parse('templates.xml') #try if no file exists generate a new empty one. Also verify if there's an old folder. If not, make one.
root=library.getroot() # Current file is called template.xml - The old ones are moved to the OLD folder and renamed to be template.r%CURRENT REVISION , then the live revision var is updated

# pull the lmod and revision number from the XML file
apa.lMod=root.attrib['lMod']
apa.revision=int(root.attrib['revision']) 

# populate the dictionary of templates from the XML file
apa.templates={}
for child in root:
	tName=child.attrib['name']
	apa.templates[tName]=template(child[0].attrib,child[1].attrib)
	if 'comment' in child.attrib:
		apa.templates[tName].comment=child.attrib['comment']

# INTERFACE CONSTRUCTION
# set the main application window
app=Tk()
app.title('APAssist')
mainFrame=Frame(app, padding=(7,7,7,7)).grid(column=0, row=0, sticky=(N,W,E,S))
# app.grid_columnconfigure(0, weight=1)
# app.grid_rowconfigure(1, weight=1)

# set and grid date/r# labels
revisionLbl=Label(mainFrame, text='Revision: %s'%apa.revision)
revisionLbl.grid(column=0, row=0, sticky=(N,W,S))

lModLbl=Label(mainFrame, text='Last Modified: %s'%apa.lMod)
lModLbl.grid(column=1, row=0, sticky=(N,E,S))

# set and grid buttons
dupeBtn=Button(mainFrame, text='Duplicate APA', command=apa.duplicate)
dupeBtn.grid(column=3, row=0, sticky=(E,W))

newBtn=Button(mainFrame, text='New Entry', command=None)
newBtn.grid(column=3, row=1, sticky=(E,W))

delBtn=Button(mainFrame, text='Delete Entry', command=None)
delBtn.grid(column=3, row=2, sticky=(E,W))

editBtn=Button(mainFrame, text='Edit', command=None)
editBtn.grid(column=3, row=3, sticky=(E,W))

saveBtn=Button(mainFrame, text='Save APA', command=None) # should only be active if a change flag is on.
saveBtn.grid(column=3, row=4, sticky=(E,W))

testBtn=Button(mainFrame, text='Test', command=None)
testBtn.grid(column=3, row=5, sticky=(E,W))

helpBtn=Button(mainFrame, text='Help', command=None)
helpBtn.grid(column=3, row=6, sticky=(E,W))

# set, configure, and populate the templateBox list and its scrollbar
templateBox=Listbox(mainFrame, selectmode='single')
templateBox.grid(column=0, row=1, columnspan=2, rowspan=6, sticky=(N,E,W,S))

templateBoxScroll=Scrollbar(mainFrame, orient=VERTICAL, command=templateBox.yview)
templateBoxScroll.grid(column=2, row=1, rowspan=6, sticky=(N,S))
templateBox['yscrollcommand'] = templateBoxScroll.set

nameList=sorted(apa.templates)
for i in nameList:
	templateBox.insert('end', i)

# info frame and its objects
templateNameBox=Text(mainFrame, height=1, width=10)
templateNameBox.grid(column=4, row=1, columnspan=5, sticky=(E,W))
templateNameLbl=Label(mainFrame, text='Template Name:')
templateNameLbl.grid(column=4, row=0, sticky=W)

commentBox=Text(mainFrame, height=1, width=10)
commentBox.grid(column=4, row=5, columnspan=5, sticky=(W,E))
commentLbl=Label(mainFrame, text='Comments')
commentLbl.grid(column=4, row=4, sticky=W)

offsetBoxLbl=LabelFrame(mainFrame, text='Offset (in)')
offsetBoxLbl.grid(column=4, row=2, columnspan=2, rowspan=2)

offsetXBox=Text(offsetBoxLbl, height=1, width=10)
offsetXBox.grid(column=4, row=2, sticky=(E,W))
offsetXLbl=Label(offsetBoxLbl, text='x')
offsetXLbl.grid(column=5, row=2)

offsetYBox=Text(offsetBoxLbl, height=1, width=10)
offsetYBox.grid(column=4, row=3, sticky=(E,W))
offsetYLbl=Label(offsetBoxLbl, text='y')
offsetYLbl.grid(column=5, row=3)

sizeBoxLbl=LabelFrame(mainFrame, text='Size (in)')
sizeBoxLbl.grid(column=6, row=2, columnspan=2, rowspan=2)

sizeWBox=Text(sizeBoxLbl, height=1, width=10)
sizeWBox.grid(column=7, row=2, sticky=(E,W))
sizeWLbl=Label(sizeBoxLbl, text='width')
sizeWLbl.grid(column=8, row=2)

sizeHBox=Text(sizeBoxLbl, height=1, width=10)
sizeHBox.grid(column=7, row=3, sticky=(E,W))
sizeHLbl=Label(sizeBoxLbl, text='height')
sizeHLbl.grid(column=8, row=3)

# select item and populate fields
# nameofframe.insert('1.0', 'text')
templateBox.bind('<<ListboxSelect>>', apa.updateFields)

app.mainloop()
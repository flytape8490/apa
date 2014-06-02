from __future__ import print_function
# Python 3.x/2.7
# APAssist  -- apa.py
# v 0.2

# A tool written to aid in the generation of APA files for the
# Kodak Prinergy system, written to work for both Python 2.7 and 3x

try:							# tkinter for 3.x
	from tkinter import *
	from tkinter.ttk import *
except ImportError:				# tkinter for 2.7
	from Tkinter import *
	from ttk import *
import xml.etree.ElementTree as xml

class template:
	def __init__(self,offset,size):
		self.offsetX=float(offset['x'])
		self.offsetY=float(offset['y'])
		self.sizeW=float(size['width'])
		self.sizeH=float(size['height'])
		self.comment=None
class apa:
	def lModUpdate(self):
		import time
		self.lMod=time.strftime('%m/%d/%Y')
	def revisionUpdate(self):
		self.revision+=1
	
# DATA READ-IN
# rather than storing each to a dictionary of classObjects, couldn't
# I just process the xml incrementally, pulling only the namelist
# and version/date on load, then pull the data out live for each
# template? might get better performance on load for a large XML

library=xml.parse('templates.xml') #try if no file exists generate a new empty one. Also verify if there's an old folder. If not, make one.
root=library.getroot() # Current file is called template.xml - The old ones are moved to the OLD folder and renamed to be template.r%CURRENT REVISION , then the live revision var is updated
apa.lMod=root.attrib['lMod']
apa.revision=int(root.attrib['revision'])
apa.templates={}
for child in root:
	tName=child.attrib['name']
	apa.templates[tName]=template(child[0].attrib,child[1].attrib)
	if 'comment' in child.attrib:
		apa.templates[tName].comment=child.attrib['comment']
apa.tNameList=sorted(apa.templates)

root=Tk()
listbox=Listbox(root)
for item in sorted(apa.templates):
	listbox.insert(END,item)
listbox.pack()
root.mainloop()

# #############TKINTER STUFF BELOW HERE!
# def dupe():
	# print('dupe!')
# def new():
	# print('new!')
# def eddn():
	# print('editDone!')
# def delete():
	# print('delete!')
# def save():
	# print('save!')
# def test():
	# print('test!')
# def halp():
	# print('help!')

# root=Tk()
# setup text variables
# apaVar=StringVar()
# apaVar.set('APA Version:\n %s'%(0))
# lastModDate=StringVar()
# lastModDate.set('Last Modified:\n %s'%('da/te/14'))
# root.title('APAssist')
# appFrame=Frame(root, padding='7 7 7 7')
# appFrame.grid(column=0, row=0, sticky=(N, W, E, S))
# appFrame.columnconfigure(0, weight=1)
# appFrame.rowconfigure(0, weight=1)
# lstTemplate=Listbox(appFrame, height=10).grid(column=0, columnspan=2, row=1, rowspan=6, sticky=(W, E))
# lblApaVer=Label(appFrame, textvariable=apaVar).grid(column=0, row=0, sticky=W)
# lblLstMod=Label(appFrame, textvariable=lastModDate).grid(column=1, row=0, sticky=W)

# btnDupe=Button(appFrame, text='Copy a New Version', command=dupe).grid(column=3, row=0, sticky=(W, E))
# btnNew=Button(appFrame, text='New Entry', command=new).grid(column=3, row=1, sticky=(W, E))
# btnEdDn=Button(appFrame, text='Edit Entry', command=eddn).grid(column=3, row=2, sticky=(W, E))
# btnDelete=Button(appFrame, text='Delete Entry', command=delete).grid(column=3, row=3, sticky=(W, E))
# btnSave=Button(appFrame, text='Save Changes', command=save).grid(column=3, row=4, sticky=(W, E))
# btnTest=Button(appFrame, text='Test', command=test).grid(column=3, row=5, sticky=(W, E))
# btnHalp=Button(appFrame, text='Help', command=halp).grid(column=3, row=6, sticky=(W, E))


# load-in data
	# if no data then generate a blank set
	# happens after interface so if the apa gets huge, it won't seem
	# like it isn't launching.
	# Maybe also set up a progress bar for loading?
# root.mainloop() # this is so the interface doesn't close right after launch
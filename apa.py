# Python 3.x/2.7
# APAssist  -- apa.py
# v 0.7

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
	from tkinter import messagebox
except ImportError:				# tkinter for 2.7
	from Tkinter import *
	from ttk import *
	import tkMessageBox as messagebox
class template:
	def __init__(self,offset,size):
		self.offsetX=float(offset['x'])
		self.offsetY=float(offset['y'])
		self.sizeW=float(size['width'])
		self.sizeH=float(size['height'])
		self.comment=''
		self.flag=None
class apa:
	pass

def dupeAPA():
	shutil.copy('templates.xml','old/templates.r%s.xml'%apa.revision)
	shutil.copy('job.apa','old/job.r%s.apa'%apa.revision) #might need to enable the symbolic link argument when reusing this to move the APA into the MCDTemplate folder
	apa.revision+=1

# actions and buttonModes
def updateFields(*args):
	cName=nameList[int(templateBox.curselection()[0])]
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
def templateBoxRefresh():
	nameList.sort()
	templateBox.delete(0,'end')
	for i in nameList:
		if apa.templates[i].flag!='deleted':
			templateBox.insert('end', i)
def editMode():
	# set item states
	templateBox['state']='disabled'
	newBtn['text']='Cancel Entry'
	newBtn['command']=cancelEdit
	delBtn['state']='disabled'
	dupBtn['state']='disabled'
	edtBtn['text']='Apply Change'
	edtBtn['command']=apply
	savBtn['state']='disabled'
	tstBtn['state']='disabled'
def normalMode():
	# set button states
	templateBox['state']='normal'
	newBtn['text']='New Entry'
	newBtn['command']=newEntry
	delBtn['state']='normal'
	dupBtn['state']='normal'
	edtBtn['text']='Edit Entry'
	edtBtn['command']=edit
	savBtn['state']='normal'
	tstBtn['state']='normal'

# button actions
def newEntry():
	# set interaction flag to new
	interactionMode='new'
	# clear and fill fields
	templateNameBox.delete('1.0','2.0')
	templateNameBox.insert('1.0', 'New')
	offsetXBox.delete('1.0','2.0')
	offsetXBox.insert('1.0', 0)
	offsetYBox.delete('1.0','2.0')
	offsetYBox.insert('1.0', 0)
	sizeWBox.delete('1.0','2.0')
	sizeWBox.insert('1.0', 0)
	sizeHBox.delete('1.0','2.0')
	sizeHBox.insert('1.0', 0)
	commentBox.delete('1.0','2.0')
	editMode()
	# won't need to enable events for applying - the apply function should look at global flag and see what needs to be done in a given instance
def cancelEdit():
	# set field values
	# !!look for global flag, if editing then reset fields to original. If new, clear out
	interactionMode='normal'
	normalMode()
	# !!clear global flag
def deleteEntry():
	# !!qbox - are you sure?
	# get name and index info
	cIndex=int(templateBox.curselection()[0])
	cName=nameList[cIndex]
	if messagebox.askyesno(message='Are you sure you want to delete \'%s\' from the APA?'%(cName), icon='question', title='CAUTION!', default='no'):
		# remove from name list and templatebox
		templateBox.delete(cIndex)
		nameList.remove(cName)
		# set dict flag to delete
		apa.templates[cName].flag='deleted'
		# clear fields
		templateNameBox.insert('end',' was deleted!')
		offsetXBox.delete('1.0','2.0')
		offsetYBox.delete('1.0','2.0')
		sizeWBox.delete('1.0','2.0')
		sizeHBox.delete('1.0','2.0')
		commentBox.delete('1.0','2.0')
def dupeEntry():
	cIndex=int(templateBox.curselection()[0])+1
	cName=nameList[cIndex-1]
	apa.templates[cName+' COPY']=apa.templates[cName]
	cName+=' COPY'
	templateNameBox.insert('end', ' COPY')
	nameList.insert(cIndex,cName)
	templateBox.insert(cIndex,cName)
	# !!For some reason, it isn't reselecting...
	templateBox.see(cIndex)
	templateBox.activate(cIndex)
def edit():
	interactionMode='edit'
	editMode()
def apply():
	interactionmode='normal'
	# !!appy changes back to apa.templates
	# !!need a check for the templateName -
		# !!if changed:
			# !!the template has to be duped in apa.templates with the new name
			# !!the original name in apa.templates has to have its flag set to deleted
			# !!the original name has to be removed from nameList
			# !!the new name has to be appended to the name list
			# !!set the flag of the new item to 'new'
			# !!templateBoxRefresh()
		# !!else set the flag to edited
	normalMode()
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

# set interaction state to run
# !!do i really need interactionMode?
interactionMode='run'

# INTERFACE CONSTRUCTION
# set the main application window
app=Tk()
app.title('APAssist')
# !!Would a paned window be a better option?
mainFrame=Frame(app, padding=(7,7,7,7)).grid(column=0, row=0, sticky=(N,W,E,S))
# app.grid_columnconfigure(0, weight=1)
# app.grid_rowconfigure(1, weight=1)

# set and grid date/r# labels
revisionLbl=Label(mainFrame, text='Revision: %s'%apa.revision)
revisionLbl.grid(column=0, row=0, sticky=(N,W,S))

lModLbl=Label(mainFrame, text='Last Modified: %s'%apa.lMod)
lModLbl.grid(column=1, row=0, sticky=(N,E,S))

# set and grid buttons

newBtn=Button(mainFrame, text='New Entry', command=newEntry)
newBtn.grid(column=3, row=1, sticky=(E,W))

delBtn=Button(mainFrame, text='Delete Entry', command=deleteEntry)
delBtn.grid(column=3, row=2, sticky=(E,W))

dupBtn=Button(mainFrame, text='Duplicate Entry', command=dupeEntry)
dupBtn.grid(column=3, row=3, sticky=(E,W))

edtBtn=Button(mainFrame, text='Edit Entry', command=edit)
edtBtn.grid(column=3, row=4, sticky=(E,W))

savBtn=Button(mainFrame, text='Save', command=None, state='disabled') # should only be active if a change flag is on. 
savBtn.grid(column=3, row=5, sticky=(E,W)) # bring up a 'save as copy or save over' dialogue

tstBtn=Button(mainFrame, text='Test', command=None)
tstBtn.grid(column=3, row=6, sticky=(E,W))

hlpBtn=Button(mainFrame, text='Help', command=None)
hlpBtn.grid(column=3, row=7, sticky=(E,W))

# set templateBox list and its scrollbar
templateBox=Listbox(mainFrame, selectmode='single')
templateBox.grid(column=0, row=1, columnspan=2, rowspan=7, sticky=(N,E,W,S))

templateBoxScroll=Scrollbar(mainFrame, orient=VERTICAL, command=templateBox.yview)
templateBoxScroll.grid(column=2, row=1, rowspan=7, sticky=(N,S))
templateBox['yscrollcommand'] = templateBoxScroll.set

nameList=list(apa.templates)
templateBoxRefresh()

# info panel objects
templateNameBox=Text(mainFrame, height=1, width=10)
templateNameBox.grid(column=4, row=0, columnspan=5, sticky=(E,W))
templateNameLbl=Label(mainFrame, text='Template Name:')
templateNameLbl.grid(column=3, row=0, sticky=E)

commentBox=Text(mainFrame, height=4, width=10)
commentBox.grid(column=4, row=5, columnspan=5, rowspan=3, sticky=(W,E))
commentLbl=Label(mainFrame, text='Comments:')
commentLbl.grid(column=4, row=4, sticky=W)

offsetBoxLbl=LabelFrame(mainFrame, text='Offset (in)')
offsetBoxLbl.grid(column=4, row=1, columnspan=2, rowspan=3)

offsetXBox=Text(offsetBoxLbl, height=1, width=10)
offsetXBox.grid(column=4, row=1, sticky=(E,W))
offsetXLbl=Label(offsetBoxLbl, text='x')
offsetXLbl.grid(column=5, row=1)

offsetYBox=Text(offsetBoxLbl, height=1, width=10)
offsetYBox.grid(column=4, row=2, sticky=(E,W))
offsetYLbl=Label(offsetBoxLbl, text='y')
offsetYLbl.grid(column=5, row=2)

sizeBoxLbl=LabelFrame(mainFrame, text='Size (in)')
sizeBoxLbl.grid(column=6, row=1, columnspan=2, rowspan=3)

sizeWBox=Text(sizeBoxLbl, height=1, width=10)
sizeWBox.grid(column=7, row=1, sticky=(E,W))
sizeWLbl=Label(sizeBoxLbl, text='width')
sizeWLbl.grid(column=8, row=1)

sizeHBox=Text(sizeBoxLbl, height=1, width=10)
sizeHBox.grid(column=7, row=2, sticky=(E,W))
sizeHLbl=Label(sizeBoxLbl, text='height')
sizeHLbl.grid(column=8, row=2)

# EVENT BINDINGS
	# select item and populate fields
	# nameofframe.insert('1.0', 'text')
templateBox.bind('<<ListboxSelect>>', updateFields) # select a template on click

app.mainloop()
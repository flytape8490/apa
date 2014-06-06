# Python 3.x/2.7
# APAssist  -- apa.py
# v 0.7.5

# A tool written to aid in the generation of APA files for the
# Kodak Prinergy system, written to work for both Python 2.7 and 3x
	# rather than storing each to a dictionary of classObjects, couldn't
	# I just process the xml incrementally, pulling only the namelist
	# and version/date on load, then pull the data out live for each
	# template? might get better performance on load for a large XML
	
# comment syntax:
	# SECTION DECLARATION
	# subsection declaration or process description
	#-subsubsection
	#!!a note, question, or something to insert later
	#.a disabled line of code

import shutil, xml.etree.ElementTree as xml
try:							# tkinter for 3.x
	from tkinter import *
	from tkinter.ttk import *
	from tkinter import messagebox
except ImportError:				# tkinter for 2.7
	from Tkinter import *
	from ttk import *
	import tkMessageBox as messagebox

# set template object
class template:
	def __init__(self,offset,size):
		self.offsetX=float(offset['x'])
		self.offsetY=float(offset['y'])
		self.sizeW=float(size['width'])
		self.sizeH=float(size['height'])
		self.comment=''
		self.flag=None

# set apa container
#!!consider ditching the class and making it a global object
class apa:
	pass

# GENERAL ACTIONS
def clearFields():
	templateNameBox.delete('1.0','end')
	offsetXBox.delete('1.0','end')
	offsetYBox.delete('1.0','end')
	sizeWBox.delete('1.0','end')
	sizeHBox.delete('1.0','end')
	commentBox.delete('1.0','end')
def dupeAPA():
	shutil.copy('templates.xml','old/templates.r%s.xml'%apa.revision)
	#!!might need to enable the symbolic link argument when reusing this to move the APA into the MCDTemplate folder
	shutil.copy('job.apa','old/job.r%s.apa'%apa.revision)
	apa.revision+=1
def templateListBoxRefresh():
	nameList.sort()
	templateListBox.delete(0,'end')
	for i in nameList:
		if apa.templates[i].flag!='deleted':
			templateListBox.insert('end', i)
def updateFields(*args):
	cName=nameList[int(templateListBox.curselection()[0])]
	cTemp=apa.templates[cName]
	clearFields()
	templateNameBox.insert('1.0', cName)
	offsetXBox.insert('1.0', cTemp.offsetX)
	offsetYBox.insert('1.0', cTemp.offsetY)
	sizeWBox.insert('1.0', cTemp.sizeW)
	sizeHBox.insert('1.0', cTemp.sizeH)
	commentBox.insert('1.0', cTemp.comment)

# SET INTERFACE STATES
def editMode():
	# set button states
	templateListBox['state']='disabled'
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
	templateListBox['state']='normal'
	newBtn['text']='New Entry'
	newBtn['command']=newEntry
	delBtn['state']='normal'
	dupBtn['state']='normal'
	edtBtn['text']='Edit Entry'
	edtBtn['command']=edit
	savBtn['state']='normal'
	tstBtn['state']='normal'

# BUTTON ACTIONS
def apply():
	interactionMode='normal'
	#!!appy changes back to apa.templates
	#!!need a check for the templateName -
		#!!if changed:
			#!!the template has to be duped in apa.templates with the new name
			#!!the original name in apa.templates has to have its flag set to deleted
			#!!the original name has to be removed from nameList
			#!!the new name has to be appended to the name list
			#!!set the flag of the new item to 'new'
			#!!templateListBoxRefresh()
		#!!else set the flag to edited
	normalMode()
def cancelEdit():
	# set field values
	#!!look for global flag, if editing then reset fields to original. If new, clear out
	normalMode()
	interactionMode='normal'
def deleteEntry():
	# get name and index info
	#!!listbox active might be useful?
	cIndex=int(templateListBox.curselection()[0])
	cName=templateListBox.get('active')
	if messagebox.askyesno(message='Are you sure you want to delete \'%s\' from the APA?'%(cName), icon='question', title='CAUTION!', default='no'):
		# remove from name list and templateListBox
		templateListBox.delete(cIndex)
		nameList.remove(cName)
		# set dict flag to delete
		apa.templates[cName].flag='deleted'
		# set field state
		clearFields()
		templateNameBox.insert('1.0','%s was deleted!'%cName)
def dupeEntry():
	#!!repeated clicks won't copy copies, have to click off and then reselect the copy
	cIndex=int(templateListBox.curselection()[0])+1
	cName=templateListBox.get('active')
	apa.templates[cName+' COPY']=apa.templates[cName]
	cName+=' COPY'
	templateNameBox.insert('end', ' COPY')
	nameList.insert(cIndex,cName)
	templateListBox.insert(cIndex,cName)
	templateListBox.selection_clear(cIndex-1)
	templateListBox.selection_set(cIndex)
	updateFields()
	
def edit(*args):
	interactionMode='edit'
	editMode()
def newEntry():
	# set interaction flag to new
	interactionMode='new'
	# set initial field state
	clearFields()
	templateNameBox.insert('1.0', 'New')
	offsetXBox.insert('1.0', 0)
	offsetYBox.insert('1.0', 0)
	sizeWBox.insert('1.0', 0)
	sizeHBox.insert('1.0', 0)
	editMode()
	#!!need to add a same-name conflict

# DATA READ-IN
# parse the xmlfile
#!!if templates.xml doesn't exist
#!!	make one
#!!else:
library=xml.parse('templates.xml')
root=library.getroot()

# POPULATE
# set the last modified date (lMod) and revision#
apa.lMod=root.attrib['lMod']
apa.revision=int(root.attrib['revision'])

# set dictionary of templates
apa.templates={}
for child in root:
	tName=child.attrib['name']
	apa.templates[tName]=template(child[0].attrib,child[1].attrib)
	if 'comment' in child.attrib:
		apa.templates[tName].comment=child.attrib['comment']
# set list of template names
nameList=list(apa.templates)

# set interactionMode to run
#!!do i really need interactionMode?
#!!this might have some scope issues, look into it!
interactionMode='run'

# INITIALISE INTERFACE
# set the main application window
app=Tk()
app.title('APAssist')
#!!would a paned window be a better option?
mainFrame=Frame(app, padding=(7,7,7,7)).grid(column=0, row=0, sticky=(N,W,E,S))
# set grid weights for stretchy magic
#.app.grid_columnconfigure(0, weight=1)
#.app.grid_rowconfigure(1, weight=1)

# set revision label
revisionLbl=Label(mainFrame, text='Revision: %s'%apa.revision)
revisionLbl.grid(column=0, row=0, sticky=(N,W,S))

# set lMod label
lModLbl=Label(mainFrame, text='Last Modified: %s'%apa.lMod)
lModLbl.grid(column=1, row=0, sticky=(N,E,S))

# set templateListBox
templateListBox=Listbox(mainFrame, selectmode='single')
templateListBox.grid(column=0, row=1, columnspan=2, rowspan=7, sticky=(N,E,W,S))

# populate templateListBox
templateListBoxRefresh()

# set templateListBoxScroll
templateListBoxScroll=Scrollbar(mainFrame, orient=VERTICAL, command=templateListBox.yview)
templateListBoxScroll.grid(column=2, row=1, rowspan=7, sticky=(N,S))

# configure the scrollbar
templateListBox['yscrollcommand'] = templateListBoxScroll.set

# buttons
#-new entry
newBtn=Button(mainFrame, text='New Entry', command=newEntry)
newBtn.grid(column=3, row=1, sticky=(E,W))

#-delete entry
delBtn=Button(mainFrame, text='Delete Entry', command=deleteEntry)
delBtn.grid(column=3, row=2, sticky=(E,W))

#-duplicate entry
dupBtn=Button(mainFrame, text='Duplicate Entry', command=dupeEntry)
dupBtn.grid(column=3, row=3, sticky=(E,W))

#-edit (or apply changes to) entry
edtBtn=Button(mainFrame, text='Edit Entry', command=edit)
edtBtn.grid(column=3, row=4, sticky=(E,W))

#-save apa and xml
#!!activate only after an edit. Don't need to worry about new items or duplicates, those are meant to be edited anyway
savBtn=Button(mainFrame, text='Save', command=None, state='disabled')
savBtn.grid(column=3, row=5, sticky=(E,W))

#-test
tstBtn=Button(mainFrame, text='Test', command=None)
tstBtn.grid(column=3, row=6, sticky=(E,W))

#-help
hlpBtn=Button(mainFrame, text='Help', command=None)
hlpBtn.grid(column=3, row=7, sticky=(E,W))

# info panel objects
#-templateNameBox: template name field
templateNameLbl=Label(mainFrame, text='Template Name:')
templateNameLbl.grid(column=3, row=0, sticky=E)
templateNameBox=Text(mainFrame, height=1, width=10)
templateNameBox.grid(column=4, row=0, columnspan=5, sticky=(E,W))

#-commentBox: template comment field
commentLbl=Label(mainFrame, text='Comments:')
commentLbl.grid(column=4, row=4, sticky=W)
commentBox=Text(mainFrame, height=4, width=10)
commentBox.grid(column=4, row=5, columnspan=5, rowspan=3, sticky=(W,E))

#-offsetLblFrm: labelframe for template offsets
offsetLblFrm=LabelFrame(mainFrame, text='Offset (in)')
offsetLblFrm.grid(column=4, row=1, columnspan=2, rowspan=3)

#-offsetXBox: template offset x-value field
offsetXLbl=Label(offsetLblFrm, text='x')
offsetXLbl.grid(column=5, row=1)
offsetXBox=Text(offsetLblFrm, height=1, width=10)
offsetXBox.grid(column=4, row=1, sticky=(E,W))

#-offsetYBox: template offset y-value field
offsetYLbl=Label(offsetLblFrm, text='y')
offsetYLbl.grid(column=5, row=2)
offsetYBox=Text(offsetLblFrm, height=1, width=10)
offsetYBox.grid(column=4, row=2, sticky=(E,W))

#-sizeLblFrm: labelframe for template size
sizeLblFrm=LabelFrame(mainFrame, text='Size (in)')
sizeLblFrm.grid(column=6, row=1, columnspan=2, rowspan=3)

#-sizeWBox: template size width field
sizeWLbl=Label(sizeLblFrm, text='width')
sizeWLbl.grid(column=8, row=1)
sizeWBox=Text(sizeLblFrm, height=1, width=10)
sizeWBox.grid(column=7, row=1, sticky=(E,W))

#-sizeHBox: template size height field
sizeHLbl=Label(sizeLblFrm, text='height')
sizeHLbl.grid(column=8, row=2)
sizeHBox=Text(sizeLblFrm, height=1, width=10)
sizeHBox.grid(column=7, row=2, sticky=(E,W))

# EVENT BINDINGS
#!!set the command to a lambdaevent so i don't have to have *args?
#!!does it really save that much?
#!!as per https://www.inkling.com/read/programming-python-mark-lutz-4th/chapter-9/listboxes-and-scrollbars  
#!!find listbox.bind('<Double-1>', (lambda event: onDoubleClick()))

# select a template in templateListBox, update fields
templateListBox.bind('<<ListboxSelect>>', updateFields)
# double click a template in templateListBox, enter edit
#!!not working - why?
templateListBox.bind('<<Double-1>>', edit)

app.mainloop()
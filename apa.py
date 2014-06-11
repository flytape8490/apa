# Python 3.x/2.7
# v 0.9
# APAssist  -- apa.py

# A tool written to aid in the generation of APA files for the
# Kodak Prinergy system, written to work for both Python 2.7 and 3x
	
# comment syntax:
	# SECTION DECLARATION
	# subsection declaration or process description
	#-subsubsection
	#!!a note, question, or something to insert later
	#.a disabled line of code

import xml.etree.ElementTree as xml
# import tkinter as a try statement for 2.7/3x compatibility
# 3.X
try:
	from tkinter import *
	from tkinter.ttk import *
	from tkinter import messagebox
# 2.7
except ImportError:
	from Tkinter import *
	from ttk import *
	import tkMessageBox as messagebox

# set static global apa container
class apa:
	pass

# set template object
class template:
	def __init__(self,offset,size):
		self.offsetX=float(offset['x'])
		self.offsetY=float(offset['y'])
		self.sizeW=float(size['width'])
		self.sizeH=float(size['height'])
		self.comment=''
		self.flag=None

# GENERAL ACTIONS
def clearFields():
	templateNameBox.delete('1.0','end')
	offsetXBox.delete('1.0','end')
	offsetYBox.delete('1.0','end')
	sizeWBox.delete('1.0','end')
	sizeHBox.delete('1.0','end')
	commentBox.delete('1.0','end')
def dupeFile():
	import os, shutil
	# check for old folder. If not, make it.
	if not os.path.exists('old'):
		os.makedirs('old')
	# move and rename the xml and apa files
	shutil.move('templates.xml','old/templates.r%s.xml'%apa.revision)
	try:
		shutil.move('Job.apa','old/Job.r%s.apa'%apa.revision)
	except IOError: #!!filenameerror in python3
		pass
	# update the revision number
	apa.revision+=1
	lModLbl['text']='Last Modified: %s'%apa.lMod
	revisionLbl['text']='Revision: %s'%apa.revision
	messagebox.showinfo(message='Files successfully copied.')
def lockFields():
	templateNameBox['state']='disabled'
	offsetXBox['state']='disabled'
	offsetYBox['state']='disabled'
	sizeWBox['state']='disabled'
	sizeHBox['state']='disabled'
	commentBox['state']='disabled'
def tabFocus(event):
	event.widget.tk_focusNext().focus()
	return 'break'
def templateListBoxRefresh():
	#!!can i have this sort as if all uppercase entries, but still have them display in entered case? otherwise, entries starting with lowercase letters end up at the bottom of the list.
	# can't have the namelist reset here, because it would then pull in deletions. Namelist must ONLY be set to the apa.template at the start
	apa.nameList.sort()
	templateListBox.delete(0,'end')
	for i in apa.nameList:
		if apa.templates[i].flag!='deleted':
			templateListBox.insert('end', i)
	templateListBox.selection_set(0)
	#!!have this scroll to the newly edited/entered item?
def unlockFields():
	templateNameBox['state']='normal'
	offsetXBox['state']='normal'
	offsetYBox['state']='normal'
	sizeWBox['state']='normal'
	sizeHBox['state']='normal'
	commentBox['state']='normal'
def upDate():
	from datetime import date
	apa.lMod=date.today().strftime('%m/%d/%Y')
def updateFields(*args):
	unlockFields()
	#!!is there a better way to get the cName that i use elsewhere? maybe something.active?
	cName=apa.nameList[int(templateListBox.curselection()[0])]
	cTemp=apa.templates[cName]
	clearFields()
	templateNameBox.insert('1.0', cName)
	offsetXBox.insert('1.0', cTemp.offsetX)
	offsetYBox.insert('1.0', cTemp.offsetY)
	sizeWBox.insert('1.0', cTemp.sizeW)
	sizeHBox.insert('1.0', cTemp.sizeH)
	commentBox.insert('1.0', cTemp.comment)
	lockFields()
# SET INTERFACE STATES
def editMode(mode):
	# unlock fields
	unlockFields()
	# set button states
	templateListBox['state']='disabled'
	newBtn['text']='Cancel Entry'
	newBtn['command']=cancelEdit
	delBtn['state']='disabled'
	dupBtn['state']='disabled'
	edtBtn['state']='disabled'
	savBtn['text']='Apply Change'
	savBtn['command']=apply
	tstBtn['state']='disabled'
	# set interactionMode to mode
	apa.interactionMode=mode
	# store name for namechange checks
	apa.oName=templateNameBox.get('1.0','1.end')
def normalMode():
	# set button states
	templateListBox['state']='normal'
	newBtn['text']='New Entry'
	newBtn['command']=newEntry
	delBtn['state']='normal'
	dupBtn['state']='normal'
	edtBtn['state']='normal'
	savBtn['text']='Save'
	savBtn['command']=saveBtn
	tstBtn['state']='normal'
	# set interactionMode
	apa.interactionMode='normal'
	# lock fields
	lockFields()

# BUTTON ACTIONS
def apply():
	# get fields
	cName=templateNameBox.get('1.0','1.end')
	#break if name is a duplicate
	if apa.interactionMode=='new' and cName in apa.nameList:
		messagebox.showinfo(message='Can not have duplicate names!', icon='error')
		return 'break'
	# if the name has changed in an edit operation
	if apa.interactionMode=='edit' and apa.oName!=cName:
		if cName not in apa.nameList:
			del(apa.templates[apa.oName])
			apa.nameList.remove(apa.oName)
			apa.nameList.append(cName)
		else:
			messagebox.showinfo(message='Can not have duplicate names!', icon='error')
			return 'break'
	# translate fields into variables
	cOffs={'x':offsetXBox.get('1.0','1.end'),'y':offsetYBox.get('1.0','1.end')}
	cSize={'width':sizeWBox.get('1.0','1.end'),'height':sizeHBox.get('1.0','1.end')}
	cComm=commentBox.get('1.0','1.end')
	# if new entry, add to nameList
	if apa.interactionMode=='new':
		apa.nameList.append(cName)
	# apply to template
	apa.templates[cName]=template(cOffs,cSize)
	apa.templates[cName].comment=cComm
	normalMode()
	templateListBoxRefresh()
	updateFields()
def cancelEdit():
	normalMode()
	updateFields()
def deleteEntry():
	# get name and index info
	cIndex=int(templateListBox.curselection()[0])
	cName=templateListBox.get('active')
	if messagebox.askyesno(message='Are you sure you want to delete \'%s\' from the APA?'%(cName), icon='question', title='CAUTION!', default='no'):
		# remove from name list and templateListBox
		templateListBox.delete(cIndex)
		apa.nameList.remove(cName)
		# set fields
		unlockFields()
		clearFields()
		templateNameBox.insert('1.0','%s was deleted!'%cName)
		lockFields()
		#!!have the box scroll back to 0, don't select anything.
		# remove the entry from the apa.templates
		del(apa.templates[cName])
def dupeEntry():
	#!!repeated clicks won't copy copies, have to click off and then reselect the copy, maybe also set the active?
	cIndex=int(templateListBox.curselection()[0])+1
	cName=templateListBox.get('active')
	apa.templates[cName+' COPY']=apa.templates[cName]
	cName+=' COPY'
	templateNameBox.insert('end', ' COPY')
	apa.nameList.insert(cIndex,cName)
	templateListBox.insert(cIndex,cName)
	templateListBox.selection_clear(cIndex-1)
	templateListBox.selection_set(cIndex)
	updateFields()
def edit(*args):
	editMode('edit')
def newEntry():
	# set interaction flag to new
	apa.interactionMode='new'
	# set initial field state
	unlockFields()
	clearFields()
	templateNameBox.insert('1.0', 'New')
	offsetXBox.insert('1.0', 0)
	offsetYBox.insert('1.0', 0)
	sizeWBox.insert('1.0', 0)
	sizeHBox.insert('1.0', 0)
	lockFields()
	editMode('new')
def saveActn():
	upDate()
	lModLbl['text']=('Last Modified: %s'%apa.lMod)
	apaFile=open('Job.apa','w')
	xmlFile=open('templates.xml','w')
	apaString=('GEOM= "%s_[$].p[$].pdf" -%s -%s %s %s 1 1 0\n')
	xmlString=(
		'\t<template name="%s"%s>\n'+
		'\t\t<offset x="%s" y="%s" />\n'+
		'\t\t<size width="%s" height="%s" />\n'+
		'\t</template>\n'
		)
	xmlFile.write(
			'<file lMod="%s" revision="%s">\n'
			%(apa.lMod, apa.revision)
			)
	apaFile.write(
			'!APA 1.0\n!Last Modified: %s\n!Revision #%s\n'
			%(apa.lMod, apa.revision)
			)
	for cName in sorted(apa.templates):
		cTemp=apa.templates[cName]
		if cTemp.comment!='':
			cComm=(' comment="'+cTemp.comment+'"')
		else:
			cComm=''
		apaFile.write(apaString%(
				cName,
				cTemp.offsetX*72 ,cTemp.offsetY*72,
				cTemp.sizeW*72 ,cTemp.sizeH*72)
				)
		xmlFile.write(xmlString%(
				cName, cComm,
				cTemp.offsetX, cTemp.offsetY,
				cTemp.sizeW, cTemp.sizeH)
				)
	xmlFile.write('</file>')
	apaFile.close()
	xmlFile.close()
	#!!progress bar is gooooooo
	messagebox.showinfo(message='Files saved.')
	#!!clear the flags from the apa, rebuild library from text file
def saveBtn():
	state=messagebox.askyesnocancel(message='Do you want to create a new version?', icon='question', title='CAUTION!')
	if state: # dupe
		dupeFile()
		saveActn()
	elif state==False: # don't dupe
		if messagebox.askyesno(message='Are you sure you want to overwrite the existing files?', icon='question', title='CAUTION!'):
			saveActn()
		else:
			dupeFile()
			saveActn()
# DATA READ-IN
# open the library, or make an empty one if none is found.
try:
	library=xml.parse('templates.xml')
except IOError: #!!filenameerror in python3
	upDate()
	f=open('templates.xml','w')
	f.write(
		'<file lMod="%s" revision="0">\n\t<template name="New">\n\t\t<offset x="0" y="0" />\n\t\t<size width="0" height="0" />\n\t</template>\n</file>'
		%apa.lMod
		)
	f.close()
	library=xml.parse('templates.xml')
root=library.getroot()

# POPULATE
# set the last modified date (lMod) and revision#
apa.lMod=root.attrib['lMod']
apa.revision=int(root.attrib['revision'])

# set dictionary of templates
apa.templates={}
for child in root:
	cName=child.attrib['name']
	apa.templates[cName]=template(child[0].attrib,child[1].attrib)
	if 'comment' in child.attrib:
		apa.templates[cName].comment=child.attrib['comment']
# set list of template names
apa.nameList=list(apa.templates)

# set apa.interactionMode to run
apa.interactionMode='run'

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
templateListBoxScroll=Scrollbar(mainFrame, orient='vertical', command=templateListBox.yview)
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

#-edit entry
edtBtn=Button(mainFrame, text='Edit Entry', command=edit)
edtBtn.grid(column=3, row=4, sticky=(E,W))

#-save apa and xml
#!!activate only after an edit. Don't need to worry about new items or duplicates, those are meant to be edited anyway
savBtn=Button(mainFrame, text='Save', command=saveBtn)
savBtn.grid(column=3, row=5, sticky=(E,W))

#-test #!!still needs to be implemented
tstBtn=Button(mainFrame, text='Test', command=None, state='disabled')
tstBtn.grid(column=3, row=6, sticky=(E,W))

#-help #!!still needs to be implemented
hlpBtn=Button(mainFrame, text='Help', command=None)
hlpBtn.grid(column=3, row=7, sticky=(E,W))

# info panel objects
#-templateNameBox: template name field
templateNameLbl=Label(mainFrame, text='Template Name:')
templateNameLbl.grid(column=3, row=0, sticky=E)
templateNameBox=Text(mainFrame, height=1, width=10, wrap='none')
templateNameBox.grid(column=4, row=0, columnspan=5, sticky=(E,W))

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

#-commentBox: template comment field
commentLbl=Label(mainFrame, text='Comments:')
commentLbl.grid(column=4, row=4, sticky=W)
commentBox=Text(mainFrame, height=4, width=10)
commentBox.grid(column=4, row=5, columnspan=5, rowspan=3, sticky=(W,E))

# EVENT BINDINGS
# select a template in templateListBox, update fields
templateListBox.bind('<<ListboxSelect>>', updateFields)
# double click a template in templateListBox, enter edit
templateListBox.bind('<Double-1>', edit)
# press tab to switch focus
templateNameBox.bind('<Tab>', tabFocus)
offsetXBox.bind('<Tab>', tabFocus)
offsetYBox.bind('<Tab>', tabFocus)
sizeWBox.bind('<Tab>', tabFocus)
sizeHBox.bind('<Tab>', tabFocus)
commentBox.bind('<Tab>', tabFocus)
#!!press enter to apply edit
lockFields()
app.mainloop()
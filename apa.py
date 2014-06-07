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
def dupeFile():
	# copy and rename the xml to the old folder
	shutil.copy('templates.xml','old/templates.r%s.xml'%apa.revision)
	# move and rename the apa to the old folder - move because the APA is rewritten from the ground up
	shutil.move('Job.apa','old/Job.r%s.apa'%apa.revision)
	apa.revision+=1
	#!!set lmoddate
	messagebox.showinfo(message='Files duplicated into the old folder.')
def templateListBoxRefresh():
	nameList.sort()
	templateListBox.delete(0,'end')
	for i in nameList:
		if apa.templates[i].flag!='deleted':
			templateListBox.insert('end', i)
	templateListBox.selection_set(0)
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
def apply(): #!!combine and put as much as you can outside the if statements
	#!!THROW UP DUPE NAME ERROR
	#!!get the name from the templateNameBox - make sure it's a single line - might need to turn off wrapping
	cName=templateNameBox.get('1.0','1.end')
	if apa.interactionMode=='new':
		nameList.append(cName)
		apa.templates[cName]=template({'x':offsetXBox.get('1.0','1.end'),'y':offsetYBox.get('1.0','1.end')},{'width':sizeWBox.get('1.0','1.end'),'height':sizeHBox.get('1.0','1.end')})
		if commentBox.get('1.0','1.end')!='':
			apa.templates[cName].comment=commentBox.get('1.0','1.end')
	elif apa.interactionMode=='edit':
		#!!assuming template name is NOT changed
		apa.templates[cName]=template({'x':offsetXBox.get('1.0','1.end'),'y':offsetYBox.get('1.0','1.end')},{'width':sizeWBox.get('1.0','1.end'),'height':sizeHBox.get('1.0','1.end')})
		if commentBox.get('1.0','1.end')!='':
			apa.templates[cName].comment=commentBox.get('1.0','1.end')
		#!!if changed:
			#!!the template has to be duped in apa.templates with the new name
			#!!the original name in apa.templates has to have its flag set to deleted
			#!!the original name has to be removed from nameList
			#!!the new name has to be appended to the name list
			#!!templateListBoxRefresh()
			#!!need to change the interaction mode to either new or edited before exiting the elif edit
	apa.templates[cName].flag=apa.interactionMode
	apa.interactionMode='normal'
	normalMode()
	templateListBoxRefresh()
	#!!select the new or edited template
	updateFields()
def cancelEdit():
	# set field values
	#!!look for global flag, if editing then reset fields to original. If new, clear out
	normalMode()
	apa.interactionMode='normal'
	updateFields()
def deleteEntry():
	# get name and index info
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
	apa.interactionMode='edit'
	editMode()
def newEntry():
	# set interaction flag to new
	apa.interactionMode='new'
	# set initial field state
	clearFields()
	templateNameBox.insert('1.0', 'New')
	offsetXBox.insert('1.0', 0)
	offsetYBox.insert('1.0', 0)
	sizeWBox.insert('1.0', 0)
	sizeHBox.insert('1.0', 0)
	editMode()
	#!!need to add a same-name conflict
def saveActn():
	root.set('lMod',str(apa.lMod))
	root.set('revision',str(apa.revision))
	#!! for edit and delete, loop through the element tree and look at each element
	#!! if a comment is deleted, this miiiight not actually write the purged comment.
	for template in root.findall('template'):
		cName=template.attrib['name']
		cTemp=apa.templates[cName]
		cName=template.attrib['name']
		cOffX=str(cTemp.offsetX)
		cOffY=str(cTemp.offsetY)
		cSizW=str(cTemp.sizeW)
		cSizH=str(cTemp.sizeH)
		cComm=str(cTemp.comment)
		# if flagged as edit
		if cTemp.flag=='edit':
			if cComm!='':
				template.set('comment',cComm)
			offset=template.find('offset')
			size=template.find('size')
			offset.set('x',cOffX)
			offset.set('y',cOffY)
			size.set('width',cSizW)
			size.set('height',cSizH)		
		# if flagged as deleted
		elif cTemp.flag=='deleted':
			#!!isn't removing
			root.remove(template)
	for cName in apa.templates:
		cTemp=apa.templates[cName]
		if cTemp.flag=='new':
			#!!successfully applies a new item, but puts in the wrong info
			cOffX=str(cTemp.offsetX)
			cOffY=str(cTemp.offsetY)
			cSizW=str(cTemp.sizeW)
			cSizH=str(cTemp.sizeH)
			cComm=str(cTemp.comment)
			top=xml.Element('template')
			template.set('name',cName)
			if cComm!='':template.set('comment',cComm)
			off=xml.SubElement(template,'offset')
			off.set('x',cOffX)
			off.set('y',cOffY)
			#.siz=xml.SubElement(template,'size')
			siz.set('width',cSizW)
			siz.set('height',cSizH)
			#.xml.dump(template)
			cTemp.flag==None
	library.write('templates.xml')
	#!!progress bar is gooooooo
	messagebox.showinfo(message='Files saved.')
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
	cName=child.attrib['name']
	apa.templates[cName]=template(child[0].attrib,child[1].attrib)
	if 'comment' in child.attrib:
		apa.templates[cName].comment=child.attrib['comment']
# set list of template names
nameList=list(apa.templates)

# set apa.interactionMode to run
#!!do i really need apa.interactionMode?
#!!this might have some scope issues, look into it!
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
savBtn=Button(mainFrame, text='Save', command=saveBtn)
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
#!!set tab events for each entry box that will switch the focus to the next entry field

app.mainloop()
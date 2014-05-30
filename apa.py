# Python 3.x/2.7
# APAssist  -- apa.py
# v 0.1

# A tool written to aid in the generation of APA files for the
# Kodak Prinergy system, written to work for both Python 2.7 and 3x

try:							# tkinter for 3.x
	from tkinter import *
	from tkinter import ttk
except ImportError:				# tkinter for 2.7
	from Tkinter import *
	from Tkinter import ttk

# HOW DO I WANT DATA STORED: PICKLE, SQL, or CSV?
# EACH WOULD REQUIRE ME TO LEARN HOW EACH WORKS...
# in any case, each APA entry is going to be a classed object
# ...but then I'd have to walk each object to get the names...
# maybe store each as a list of lists? I would then need a bunch of
# slice objects - but are those available in 2.7?
# I could have a dictionary where each key is the template name and
# the value points at a class... NOPE DOESN'T WORK


# set up functions
# start building interface

root=Tk()
bEdit=ttk.Button(root, text='hi').grid()

# load-in data
	# if no data then generate a blank set
	# happens after interface so if the apa gets huge, it won't seem
	# like it isn't launching.
	# Maybe also set up a progress bar for loading?
root.mainloop() # this is so the interface doesn't close right after launch
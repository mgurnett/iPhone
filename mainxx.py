#!/usr/bin/python
import ui
from datetime import datetime
from database import *

DATABASE_NAME = 'Notions'
DATABASE_TABLE = 'ideas'
scale = 0
text = ''

def button_save (sender):
	currentDateTime = datetime.now().timestamp()
	write_data (DATABASE_NAME, DATABASE_TABLE, scale, text, currentDateTime)

def button_read (sender):
	sender.title = 'Hello'

def button_cancel (sender):
	sender.title = 'Hello'
	
def slider_action(sender):
	# Get the root view:
	v = sender.superview
	# Get the sliders:
	s = v['slider1'].value
	global scale
	scale = int(round(s * 4)) + 1
	v['label1'].text = str ( scale )
	
	
def textfield_action(textfield):
	global text
	text = textfield.text
	return text
	
def scrollview(sender):
	pass
	
t = ui.TextField()
t.action = textfield_action
	
ui.load_view('entry').present('fullscreen')

import ui
from datetime import datetime
from database import write_data, read_data, tally_data

DATABASE_NAME = 'Thoughts'
DATABASE_TABLE = 'ideas'
scale=1

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
	
def textfield_action (textfield):
	global text
	text = textfield.text

def button_save (sender):
	currentDateTime = datetime.now().timestamp()
	write_data (DATABASE_NAME, DATABASE_TABLE, scale, text, currentDateTime)
	#nav_view.close()
	add_right_buttonitem(main_view, read_subview)
    
def bt_close(sender):
    nav_view.close()

def add_close_buttonitem(v):
    close = ui.ButtonItem()
    close.image = ui.Image.named('ionicons-close-24')
    close.action = bt_close
    v.left_button_items = [close]

def add_right_buttonitem(v, action):
    right = ui.ButtonItem()
    right.image = ui.Image.named('ionicons-arrow-right-b-24')
    right.action = action
    v.right_button_items = [right]

def read_subview (sender):
    sub_view = ui.load_view ('read_data')
    sub_view['label2'].text = read_data (DATABASE_NAME, DATABASE_TABLE, 10)
    nav_view.push_view(sub_view)

def tally_subview (sender):
    sub_view = ui.load_view ('tally_data')
    sub_view['label2'].text = tally_data (DATABASE_NAME, DATABASE_TABLE)
    nav_view.push_view(sub_view)

main_view = ui.load_view ('main_view') 
# sets the name to the same as this filename unless the name is indicated
add_close_buttonitem(main_view)
add_right_buttonitem(main_view, read_subview)
add_right_buttonitem(main_view, tally_subview)

nav_view = ui.NavigationView (main_view)
nav_view.present("sheet",  hide_title_bar=True)

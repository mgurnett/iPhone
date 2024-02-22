import ui
from datetime import datetime
from database import *

DATABASE_NAME = 'Notions'
DATABASE_TABLE = 'ideas'
scale = 0
text = ''

v = ui.load_view()
enter_page = ui.load_view('enter_data')
read_page = ui.load_view('read_data')
tally_page = ui.load_view('tally_data')
L = ui.ListDataSource([])

L.highlight_color='#f1f1f1'
L.font=('Baskerville',23)
L.text_color='red'

read=read_page['text']

L.items=[
	{'title':'Record entry','image':ui.Image.named('iob:gear_a_32')},
	{'title':'Read all','image':ui.Image.named('iob:eye_32')},
	{'title':'Tally Data','image':ui.Image.named('iob:settings_32')},
	]

def row(sender):
	if sender.selected_row==0:
		nav.push_view(enter_page)
	elif sender.selected_row==1:
		nav.push_view(read_page)
	elif sender.selected_row==2:
		nav.push_view(tally_page)

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

table=v['Menu']
table.tint_color='green'
table.data_source=L
table.delegate = L
L.action=row
#v.present('sheet')

nav=ui.NavigationView(table)
nav.height=480
nav.width=320
nav.present('sheet',hide_title_bar=True)
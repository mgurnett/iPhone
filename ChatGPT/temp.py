import ui
from datetime import datetime
from database import write_data, read_data, tally_data

DATABASE_NAME = 'Thoughts'
DATABASE_TABLE = 'ideas'

class MainView(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()
 
    def setup_ui(self):
        # Load main screen from pyui file
        self.main_screen = ui.load_view('main_screen.pyui')
        self.main_screen.present('fullscreen', title_bar_color='#a3c3bf')
        self.main_screen['button1'].action = self.show_view1
        self.main_screen['button2'].action = self.show_view2
        self.main_screen['button3'].action = self.show_view3

    def update_slider_label(self, sender):
        # Update the label text with the value of the slider
        scale = int(round(sender.value * 4)) + 1
        sender.superview['label1'].text = f"{scale}"

    def show_view1(self, sender):
        view1 = ui.load_view('main_view')
        view1.present('sheet', hide_title_bar=True)
        view1['slider'].action = self.update_slider_label
        view1['save_button'].action = self.save_data
        view1['cancel_button'].action = self.cancel_save

    def cancel_save(self, sender):
        sender.superview.close()

    def save_data(self, sender):
        slider_value = sender.superview['slider'].value
        scale = int(round(slider_value * 4)) + 1
        text_value = sender.superview['textfield'].text
        # Process the slider value and text data as needed
        # print("Slider value:", scale)
        # print("Text value:", text_value)
        # Close the add data screen
        currentDateTime = datetime.now().timestamp()
        write_data(DATABASE_NAME, DATABASE_TABLE, scale, text_value, currentDateTime)
        sender.superview.close()

    def show_view2(self, sender):
        view2 = ui.load_view('read_view')
        data_list = read_data(DATABASE_NAME, DATABASE_TABLE, 0)
        if view2:
            view2.present('sheet')
            self.display_data_on_scrollview(view2, data_list)
        else:
            print("Failed to load view2")
        
    def show_view3(self, sender):
        view3 = ui.load_view('tally_view')
        data_list = tally_data(DATABASE_NAME, DATABASE_TABLE)
        # print(data_list)  # Print view3 to check if it's loaded correctly
        if view3:
            view3.present('sheet')
            self.display_data_on_scrollview(view3, data_list)
        else:
            print("Failed to load view3")

    def display_data_on_scrollview(self, view, data):
        scroll_view = view['scrollview']
        view_width = self.width  # Width of the main view
        total_height = len(data) * 40  # Calculate total height of all labels
        scroll_view.content_size = (view_width, total_height)  # Set content size of scroll view
        for index, item in enumerate(data):
            label = ui.Label(frame=(20, index * 40, view_width + 150, 40))
            label.text = item  # Assuming each item in data is a string
            label.flex = 'W'
            scroll_view.add_subview(label)

# Create and present the main view
main_view = MainView()

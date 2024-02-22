import ui

class MainView(ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_ui()

    def setup_ui(self):
        self.background_color = '#a3c3bf'
        # Create buttons for navigation
        self.button1 = ui.Button(title='Record', flex='W')
        self.button1.width = 100
        self.button1.height = 60
        self.button1.center = (self.width - 50, self.height - 75)
        self.button1.action = self.show_view1

        self.button2 = ui.Button(title='Read', flex='W')
        self.button2.width = 100
        self.button2.height = 60
        self.button2.center = (self.width -50, self.height - 50)
        self.button2.action = self.show_view2

        self.button3 = ui.Button(title='Tally', flex='W')
        self.button3.width = 100
        self.button3.height = 60
        self.button3.center = (self.width - 50, self.height - 0)
        self.button3.action = self.show_view3

        # Add buttons to the main view
        self.add_subview(self.button1)
        self.add_subview(self.button2)
        self.add_subview(self.button3)

        # main = ui.load_view ('main').present('sheet')

    def show_view1(self, sender):
        view1 = ui.load_view ('main_view').present('sheet')

    def show_view2(self, sender):
        view2 = ui.load_view ('read_view').present('sheet')

    def show_view3(self, sender):
        view3 = ui.load_view ('tally_view').present('sheet')

# Create and present the main view
main_view = MainView()
main_view.present('fullscreen', title_bar_color='#a3c3bf')
main_view.name='Thoughts'

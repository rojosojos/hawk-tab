from H60TabData import c_pwr_one_point_zero, c_pwr_point_nine

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder

Builder.load_file("tab_data.kv")

class MainInterface(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        press_alts = [0,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,10500,11000,11500,12000,12500,13000]

        pa_menu_items = [
            {
                "text": f"PA: {i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.pa_menu_callback(x),
            } for i in press_alts
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.button,
            items=pa_menu_items,
            width_mult=4,
        )

    def pa_menu_callback(self, text_item):
        self.ids.pa_label.text = str(text_item)
        # print(text_item)

class TabDataApp(MDApp):

    def build(self):
        return MainInterface()


if __name__=='__main__':
    TabDataApp().run()
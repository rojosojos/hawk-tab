from H60TabData import c_pwr_one_point_zero, c_pwr_point_nine

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.core.window import Window
from kivy.lang import Builder

# Set the app size
Window.size = (320, 568)

Builder.load_file("tab_data.kv")

class MainInterface(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        ## PRESSURE ALTITUDE MENU ##
        press_alts = [0,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,10500,11000,11500,12000,12500,13000]

        pa_menu_items = [
            {
                "text": f"PA: {i}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=i: self.pa_menu_callback(x),
            } for i in press_alts
        ]
        self.pa_menu = MDDropdownMenu(
            caller=self.ids.pa_button,
            items=pa_menu_items,
            width_mult=4,
        )

        ## OUTSIDE AIR TEMP MENU ##
        outside_air_temps = [-15,-10,-5,0,5,10,15,20,25,30,35,40]

        oat_menu_items = [
            {
                "text":f"{oat}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=oat: self.oat_menu_callback(x),
            } for oat in outside_air_temps
        ]
        self.oat_menu = MDDropdownMenu(
            caller=self.ids.oat_button,
            items=oat_menu_items,
            width_mult=4,
        )

    def pa_menu_callback(self, menu_item):
        self.ids.pa_label.text = str(menu_item)
        self.pa_menu.dismiss()

    def oat_menu_callback(self, menu_item):
        self.ids.oat_label.text = str(menu_item)
        self.oat_menu.dismiss()


class TabDataApp(MDApp):

    def build(self):
        return MainInterface()


if __name__=='__main__':
    TabDataApp().run()
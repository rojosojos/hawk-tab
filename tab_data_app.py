from H60TabData import c_pwr_one_point_zero, c_pwr_point_nine

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.lang import Builder

# Set the app size
Window.size = (320, 568)

Builder.load_file("tab_data.kv")

class MainInterface(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # sets the number of columns in the grid layout
        self.cols = 1

        ###### PRESSURE ALTITUDE DROPDOWN MENU #######
            # values for list times (will be strings)
        press_alts = [0,500,1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,7500,8000,8500,9000,9500,10000,10500,11000,11500,12000,12500,13000]
            # Iterates the list above to create list items with correct properties
        pa_menu_items = [{"text": f"{i}", "viewclass": "OneLineListItem", 
            "on_release": lambda x=i: self.dropdown_menu_callback(x, self.ids.pa_label, self.pa_menu)} for i in press_alts]
            # create the dropdown list
        self.pa_menu = MDDropdownMenu(caller=self.ids.pa_button, items=pa_menu_items, width_mult=3)

        ###### OUTSIDE AIR TEMP DROPDOWN MENU ########
            # values for list times (will be strings)
        outside_air_temps = [-15,-10,-5,0,5,10,15,20,25,30,35,40]
            # Iterates the list above to create list items with correct properties
        oat_menu_items = [{"text":f"{oat}","viewclass": "OneLineListItem",
            "on_release": lambda x=oat: self.dropdown_menu_callback(x, self.ids.oat_label, self.oat_menu),} for oat in outside_air_temps]
            # create the dropdown list
        self.oat_menu = MDDropdownMenu(caller=self.ids.oat_button, items=oat_menu_items, width_mult=3)

    ### Handles clicking of a dropdown menu ###
    def dropdown_menu_callback(self, menu_item, target_label, dropdown_menu):
        target_label.text = str(menu_item)
        dropdown_menu.dismiss()

    ### Calculate corrected HOGE MGW
    def calc_corrected_hoge_mgw(self):
        if self.ids.atf.text !="" and (self.ids.atf.text.isnumeric() or self.ids.atf.text[0]==".") and float(self.ids.atf.text)>=.9 and float(self.ids.atf.text)<=1.0:
            print("valid")

            ac_atf = float(self.ids.atf.text)
            atf_compensation = ((ac_atf*100)-90)
            print(atf_compensation)


        else:
            print("invalid")




    def calculate_values(self):
        pass


class TabDataApp(MDApp):

    def build(self):
        return MainInterface()


if __name__=='__main__':
    TabDataApp().run()
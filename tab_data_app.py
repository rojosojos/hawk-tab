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
        self.atf_compensation = 0
        self.pa = 0
        self.oat = 15
        self.zero_fuel_wt = 16500
        self.fuel_wt = 2400
        self.red = (1,0,0,1)
        self.black = (0,0,0,1)

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

    def no_error(self):
        self.ids.top_heading.text = "MH-60S TAB Data"
        self.ids.top_heading.color = self.black
    def show_error(self, message):
        self.ids.top_heading.text = f"Error in {message}"
        self.ids.top_heading.color = self.red


    # def resize_output


    ### Calculate base values (ATF correction, OAT, PA) - return false if unable / errors / blank data
    def check_input_values(self):
        
        try:
            self.pa = float(self.ids.pa_label.text)
            self.no_error()
        except:
            self.show_error("PA")
            print("PA didnt work")
            return False
        try:
            self.oat = float(self.ids.oat_label.text)
            self.no_error()
        except:
            self.show_error("OAT")
            print("OAT didnt work")
            return False
        try:
            self.zero_fuel_wt = float(self.ids.zero_fuel_wt.text)
            self.no_error()
        except:
            self.show_error("Zero Fuel Weight")
            print("zero fuel wt didn't work")
            return False
        try:
            self.fuel_wt = float(self.ids.fuel_wt.text)
            self.no_error()
        except:
            self.show_error("Fuel Weight")
            print("fuel weight didn't work")
            return False
        try:
            if self.ids.atf.text !="" and (self.ids.atf.text.isnumeric() or self.ids.atf.text[0]==".") and float(self.ids.atf.text)>=.9 and float(self.ids.atf.text)<=1.0:
                self.atf_compensation = ((float(self.ids.atf.text)*100)-90)
                self.no_error()
            else:
                self.show_error("ATF")
                print("atf compensation didnt work")
                return False
        except:
            self.show_error("ATF")
            print("atf compensation didnt work")
            return False

        return True


    ### Calculate a corrected MAX HOGE MGW 
    def calc_corrected_hoge_mgw(self):
            ## Lookup values from TAB chart
        max_hoge_wt_1 = c_pwr_one_point_zero[self.oat][self.pa]["mgw"]*100
        max_hoge_wt_pt_9 = c_pwr_point_nine[self.oat][self.pa]["mgw"]*100
        ## Correct for ATFs between .9 and 1.0
        ## how many pounds difference between .9 and 1.0
        mgw_difference = max_hoge_wt_1 - max_hoge_wt_pt_9
        ## 1/10 of the weight difference (to be multipled by the ATF correction (a number between 1 and 10))
        one_part_mgw_difference = mgw_difference/10
        ## figure out how much to add back when ATF is not 1.0 or .9
                    # parts to add back  * weight for each part 
        gw_atf_compensation = self.atf_compensation * one_part_mgw_difference
        ## Max gross weight that can be HOGEd corrected for ATFs 
        corrected_mgw = int(max_hoge_wt_pt_9 + gw_atf_compensation)
        self.ids.hoge_mgw_label.text = str(corrected_mgw)
        self.ids.hoge_mgw_label.font_size = 14


    ## the calculate button is clicked - runs multiple functions to validate inputs and create outputs
    def calculate_values(self):
        ## error check and update input values
        if self.check_input_values():
            ## UPDATE OUTPUT VALUES
            self.calc_corrected_hoge_mgw()


class TabDataApp(MDApp):

    def build(self):
        return MainInterface()


if __name__=='__main__':
    TabDataApp().run()
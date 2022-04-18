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
        # app variables
        self.atf_compensation = 0
        self.pa = 0
        self.oat = 15
        self.zero_fuel_wt = 16500
        self.fuel_wt = 2400
        self.ac_wt = 18900
        self.corrected_mgw = 18000
        self.rule_of_thumb_correction = 0
        self.red = (1,0,0,1)
        self.black = (0,0,0,1)
        self.green = (0,1,0,1)

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


    ### Handles displaying Errors during input data validation
    def no_error(self):
        self.ids.top_heading.text = "MH-60S TAB Data"
        self.ids.top_heading.color = self.black
    def show_error(self, message):
        self.ids.top_heading.text = f"Error in {message}"
        self.ids.top_heading.color = self.red


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


    ### Calculate a corrected MAX HOGE MGW - called after input data is validated
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
        self.corrected_mgw = int(max_hoge_wt_pt_9 + gw_atf_compensation)
        self.ids.hoge_mgw_label.text = str(self.corrected_mgw)


    ### calculate aircraft weight - called after input data is validated
    def calc_aircraft_wt(self):
        self.ac_wt = int(self.zero_fuel_wt + self.fuel_wt)
        self.ids.ac_weight_label.text = str(self.ac_wt)


    def calc_rot_correction(self):
        """Rule of thumb power correction 200lbs = 1% TRQ
             NOTE: must be called after calc_corrected_hoge_mgw so that self.corrected_mgw has been calculated
             NOTE: must be called after calc_aircraft_wt so that self.ac_wt has been calculated"""

         ## correction for aircraft weights less than max
         #BUG does not check if AC GW is greater than HOGE capability 23-9 
        self.rule_of_thumb_correction = int((self.corrected_mgw - self.ac_wt)/200)


    def calc_hoge_powers(self):
        """Calculate HOGE power required, HOGE power available, and power margin"""
     
        ## Lookup values from TAB chart
        max_hoge_trq_1 = c_pwr_one_point_zero[self.oat][self.pa]["oge"]
        max_hoge_trq_pt_9 = c_pwr_point_nine[self.oat][self.pa]["oge"]
        
        ## correction for ATF different than 1.0 or .9
        #BUG not sure why we would use ATF in power required calculation (because gross weight changes)
        hoge_trq_difference = max_hoge_trq_1 - max_hoge_trq_pt_9
        one_part_hoge_trq_difference = hoge_trq_difference/10
        hoge_trq_atf_compensation = (10-self.atf_compensation) * one_part_hoge_trq_difference

        ## OUTPUT - Power Available & HOGE POWER REQUIRED ##
        power_available = int(max_hoge_trq_1 - hoge_trq_atf_compensation)
        self.ids.power_available_label.text = str(power_available)

        hoge_trq_required = int(max_hoge_trq_1 - self.rule_of_thumb_correction - hoge_trq_atf_compensation)
        self.ids.hoge_pr_label.text = str(hoge_trq_required)

        ## Compute Power Margin
        self.ids.margin_label.text = str(power_available-hoge_trq_required)


    def calc_hige_power_required(self):
            #########  HIGE TORQUE REQUIRED    ############
        ## Lookup values from TAB chart
        max_hige_trq_1 = c_pwr_one_point_zero[self.oat][self.pa]["ige"]
        max_hige_trq_pt_9 = c_pwr_point_nine[self.oat][self.pa]["ige"]
        ## correction for ATF different than 1.0 or .9
        #BUG not sure why we would use ATF in power required calculation (because gross weight changes)
        hige_trq_difference = max_hige_trq_1 - max_hige_trq_pt_9
        one_part_hige_trq_difference = hige_trq_difference/10
        hige_trq_atf_compensation = (10-self.atf_compensation) * one_part_hige_trq_difference

        ## OUTPUT - HIGE POWER REQUIRED ##
        hige_trq_required = int(max_hige_trq_1 - self.rule_of_thumb_correction - hige_trq_atf_compensation)
        self.ids.hige_pr_label.text = str(hige_trq_required)


    def calculate_values(self):
        """calculate button is clicked - runs multiple functions to validate inputs and create outputs"""
        ## error check and update input values
        if self.check_input_values():
            ## UPDATE OUTPUT VALUES
            self.calc_corrected_hoge_mgw()
            self.calc_aircraft_wt()
            self.calc_rot_correction()
            self.calc_hoge_powers()
            self.calc_hige_power_required()


class TabDataApp(MDApp):
    def build(self):
        return MainInterface()


if __name__=='__main__':
    TabDataApp().run()
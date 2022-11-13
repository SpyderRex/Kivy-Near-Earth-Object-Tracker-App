from kivy.app import App
from kivy.uix.spinner import Spinner
import requests
from datetime import date
from kivy.uix.boxlayout import BoxLayout
import math

class MySpinner(Spinner):
    START_DATE = str(date.today())
    END_DATE = str(date.today())
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={START_DATE}&end_date={END_DATE}&api_key=G6AVpNb3am09sy8TtJEte7PGv75HeMEq8je6SLJz"
    response = requests.get(url)
    object_list = response.json()["near_earth_objects"][START_DATE]
    name_list = [sub["name"] for sub in object_list]
    date_list = [sub["close_approach_data"] for sub in object_list]
    close_date_list = [sub[0]["close_approach_date_full"] for sub in date_list]
    name_date_list = list(zip(close_date_list, name_list))
    final_object_list = [" ".join(i) for i in name_date_list]
    values = final_object_list

class MyBoxLayout(BoxLayout):
    def spinner_clicked(self, value):
        self.ids.object_spinner_id.text = str(value)
        
        START_DATE = str(date.today())
        END_DATE = str(date.today())
        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={START_DATE}&end_date={END_DATE}&api_key=G6AVpNb3am09sy8TtJEte7PGv75HeMEq8je6SLJz"
        response = requests.get(url)
        object_list = response.json()["near_earth_objects"][START_DATE]
        name_list = [sub["name"] for sub in object_list]
        date_list = [sub["close_approach_data"] for sub in object_list]       
        close_date_list = [sub[0]["close_approach_date_full"] for sub in date_list]
        name_date_list = list(zip(close_date_list, name_list))
        final_object_list = [" ".join(i) for i in name_date_list]
        
        self.ids.abs_mag.text = str(object_list[final_object_list.index(value)]["absolute_magnitude_h"]) 
        self.ids.obj_size.text = str(round(object_list[final_object_list.index(value)]["estimated_diameter"]["meters"]["estimated_diameter_min"], 2)) + " to " + str(round(object_list[final_object_list.index(value)]["estimated_diameter"]["meters"]["estimated_diameter_max"], 2)) + " " + "m"
        self.ids.obj_distance.text = str(math.ceil(float(object_list[final_object_list.index(value)]["close_approach_data"][0]["miss_distance"]["kilometers"]))) + " " + "km"
        self.ids.obj_speed.text = str(round(float(object_list[final_object_list.index(value)]["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]), 2)) + " " + "kph"
        self.ids.obj_hazard.text = str(object_list[final_object_list.index(value)]["is_potentially_hazardous_asteroid"])
        self.ids.obj_orbit.text = str(object_list[final_object_list.index(value)]["close_approach_data"][0]["orbiting_body"])
        self.ids.obj_sentry.text = str(object_list[final_object_list.index(value)]["is_sentry_object"])

class NEOApp(App):
    def build(self):
        return MyBoxLayout()

if __name__ == "__main__":
    NEOApp().run()       
import tkinter as tk
import tkintermapview
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from tkinter import messagebox
from opencage.geocoder import OpenCageGeocode

key = "b519060a670f4421993f91d56485a0e8"
root = tk.Tk()
root.geometry("500x600")

label1 = tk.Label(root, text="Phone number Tracker", font=('Helvetica', 14, 'bold'))
label1.pack(pady=10)

def getResult():
    num = number.get("1.0", tk.END).strip()
    try:
        num1 = phonenumbers.parse(num)
        if not phonenumbers.is_valid_number(num1):
            raise ValueError("Invalid phone number")

        location = geocoder.description_for_number(num1, "en")
        service_provider = carrier.name_for_number(num1, "en")

        ocg = OpenCageGeocode(key)
        query = str(location)
        results = ocg.geocode(query)

        if results:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']

            my_label = tk.LabelFrame(root)
            my_label.pack(pady=20)

            map_widget = tkintermapview.TkinterMapView(my_label, width=450, height=450, corner_radius=0)
            map_widget.set_position(lat, lng)
            map_widget.set_marker(lat, lng, text="Phone Location")
            map_widget.set_zoom(10)
            map_widget.pack()

            address_components = results[0]['components']
            street = address_components.get('road', 'N/A')
            city = address_components.get('city', address_components.get('town', address_components.get('village', 'N/A')))
            postal_code = address_components.get('postcode', 'N/A')

            result.delete("1.0", tk.END)  # Clear previous results
            result.insert(tk.END, "The country of this number is: " + location)
            result.insert(tk.END, "\nThe SIM card provider of this number is: " + service_provider)
            result.insert(tk.END, "\nLatitude is: " + str(lat))
            result.insert(tk.END, "\nLongitude is: " + str(lng))
            result.insert(tk.END, "\nStreet Address is: " + street)
            result.insert(tk.END, "\nCity Address is: " + city)
            result.insert(tk.END, "\nPostal code is: " + postal_code)
        else:
            result.delete("1.0", tk.END)
            result.insert(tk.END, "Could not find location information.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

number = tk.Text(root, height=1, width=20, font=('Helvetica', 12))
number.pack(pady=10)

button = tk.Button(root, text="Search", command=getResult, font=('Helvetica', 12))
button.pack(pady=10)

result = tk.Text(root, height=10, width=60, font=('Helvetica', 12))
result.pack(pady=10)

root.mainloop()

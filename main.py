import json
from tkinter import messagebox, Tk, Label, Button, StringVar, OptionMenu
from tkinter.ttk import Separator

import requests
from PIL import Image, ImageTk

# Create the main window
window = Tk()
window.title("Weather App")
window.geometry("400x650")
window.configure(bg="#F5F5F5")

# API Key and default city (Please add Your API key bellow ) for your convince Iam providing you my API key for now
api_key = "b86cf272ff9a43cbb1052718233006"
city = ""
state = "MH"
country = "IN"


# Function to retrieve weather data from the API
def get_weather():
    global city
    city = city_input.get().strip()

    if not city:
        messagebox.showerror("Input Error", "City name cannot be empty.")
        return

    # API call
    # IF you have api key of weatherapi then use bellow link else we have to change the link slightly
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city},{state},{country}&aqi=yes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        show_weather_info(data)
        set_background_image(city)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"An error occurred during the API request: {e}")
    except json.JSONDecodeError as e:
        messagebox.showerror("API Error", f"Failed to parse API response: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")


# Function to display weather information
def show_weather_info(data):
    location = data["location"]["name"]
    temperature = data["current"]["temp_c"]
    weather_desc = data["current"]["condition"]["text"]
    wind_speed = data["current"]["wind_kph"]
    humidity = data["current"]["humidity"]
    icon_url = data["current"]["condition"]["icon"]

    # Display weather information
    location_label.config(text=location)
    temperature_label.config(text=f"{temperature} °C")
    weather_desc_label.config(text=weather_desc)
    wind_speed_label.config(text=f"Wind Speed: {wind_speed} km/h")
    humidity_label.config(text=f"Humidity: {humidity}%")
    try:
        response = requests.get(f"http:{icon_url}", stream=True)
        response.raise_for_status()
        image_data = response.content

        # Save the image data to a file
        with open("weather_icon.png", "wb") as file:
            file.write(image_data)

        # Load the image using PIL
        image = Image.open("weather_icon.png")
        image = image.resize((100, 100))  # Resize the image to fit the label
        photo = ImageTk.PhotoImage(image)

        # Display the image in the window
        icon_label.config(image=photo)
        icon_label.image = photo  # Store a reference to the photo to prevent it from being garbage collected
    except Exception as e:
        print(f"Failed to load weather icon: {e}")


# Function to display weather description
def show_weather_description():
    weather_desc = weather_desc_label.cget("text")
    descriptions = {
        "overcast": "Cloudy with no sunshine.",
        "sunny": "Clear sky with abundant sunshine.",
        "rain": "Precipitation in the form of raindrops.",
        # We can add more descriptions for other weather conditions if needed...
    }
    description = descriptions.get(weather_desc.lower(), "No description available.")
    messagebox.showinfo("Weather Description", description)


# Function to set the background image based on city
def set_background_image(cityi):
    try:
        bg_image = Image.open(f"{cityi.lower()}_background.jpg")
        bg_image = bg_image.resize((400, 650), Image.ANTIALIAS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label.config(image=bg_photo)
        bg_label.image = bg_photo
    except FileNotFoundError:
        bg_label.config(image="")
        messagebox.showwarning("Background Image", f"Background image not found for city: {city}")


# Function to show the names and thanks
def show_names_and_thanks():
    messagebox.showinfo("About",
                        "Developed By:\n\n ""Pravin Paithankar \n Iam a Student at GHRCEM Pune \n Thanks for Visiting \n You can use This code in Your codes")


# Create and configure the widgets
bg_label = Label(window, bg="#F5F5F5")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

title_label = Label(window, text="Weather App", font=("Helvetica", 25, "bold", "italic"))
title_label.place(x=50, y=40)

location_label = Label(window, text="", font=("Helvetica", 20, "bold"))
location_label.place(x=50, y=120)

temperature_label = Label(window, text="", font=("Helvetica", 36))
temperature_label.place(x=50, y=180)

weather_desc_label = Label(window, text="", font=("Helvetica", 14))
weather_desc_label.place(x=50, y=240)

wind_speed_label = Label(window, text="", font=("Helvetica", 12))
wind_speed_label.place(x=50, y=280)

humidity_label = Label(window, text="", font=("Helvetica", 12))
humidity_label.place(x=50, y=310)

city_input = StringVar()
city_label = Label(window, text="Select a City:", font=("Helvetica", 12))
city_label.place(x=50, y=360)
city_entry = OptionMenu(window, city_input, "Pune", "Mumbai", "Nagpur", "Aurangabad")
city_entry.place(x=150, y=355)
city_input.set("Pune")

get_weather_button = Button(window, text="Get Weather", font=("Helvetica", 12), command=get_weather)
get_weather_button.place(x=250, y=410)

description_button = Button(window, text="Weather Description", font=("Helvetica", 12),
                            command=show_weather_description)
description_button.pack(pady=10)
description_button.place(x=50, y=410)

about_button = Button(window, text="About", font=("Helvetica", 9), width=4, relief="solid",
                      command=show_names_and_thanks)
about_button.place(x=350, y=20)

separator = Separator(window, orient='horizontal')
separator.place(x=50, y=480, width=300)

icon_label = Label(window)
icon_label.place(x=50, y=500)

# Call get_weather function to fetch weather information for the default city
get_weather()

# Run the main window loop
window.mainloop()

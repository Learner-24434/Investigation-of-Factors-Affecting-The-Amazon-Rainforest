from customtkinter import *
import datetime as dt
from PIL import Image



BORDER_COLOUR = "grey"
START_DATE = dt.date(2013, 1, 1)
END_DATE = dt.date(2025, 12, 1)
VARIABLES = [
    "NDVI",
    "EVI",
    "Sahara Surface Wind Speed",
    "Sahara Dust Density",
    "Ratio of Dust Deposition over Dust Emission",
    "Atlantic Wind Speed 850hPa",
    "Atlantic Dust Density"
    ]
LABEL_FONT = ("Roboto", 20, "bold")

# Initiate the app
app = CTk()
app.geometry("1600x900")
app.title("Investigation of Factors Affecting the Amazon")
app.configure(set_default_color_theme = "dark")

# Create title frame
title_Frame = CTkFrame(app, 1600, 100, border_width = 2, border_color=BORDER_COLOUR)
title_Frame.place(x=0, y=0)

title = CTkLabel(title_Frame, text = "Investigation of Factors Affecting the Amazon", font = ("Roboto", 50, "bold"))
title.pack(pady = 25)
title_Frame.pack_propagate(False)



# Create control frame
control_Frame = CTkFrame(app, 1200, 50, border_width = 2, border_color=BORDER_COLOUR)
control_Frame.place(x=0, y = 850)

var_x_label = CTkLabel(control_Frame, text = "Variable on y axis:", font = LABEL_FONT)
var_x_label.place(x = 15, y = 10)

var_x_menu= CTkOptionMenu(control_Frame, values = VARIABLES)
var_x_menu.place(x = 230, y = 10)



def apply():
    var_x = str(var_x_menu.get())
    match var_x_menu.get():
        case "NDVI":
            file = "../graphs/amazon_NDVI.png"
        case "EVI":
            file = "../graphs/amazon_EVI.png"
        case "Sahara Surface Wind Speed":
            file = "../graphs/Sahara_wind_speed_Time.png"
        case "Sahara Dust Density":
            file = "../graphs/Sahara_Dust_Density_Regression.png"
        case "Ratio of Dust Deposition over Dust Emission":
            file = "../graphs/ratio_time.png"
        case "Atlantic Wind Speed 850hPa":
            file = "../graphs/Atlantic_Speed850hpa_Time.png"
        case "Atlantic Dust Density":
            file = "../graphs/Atlantic_Dust_Density_Time.png"

    # Graph the stuff
    plot_img = CTkImage(light_image=Image.open(file), size=(1000, 750))  # Match the aspect ratio of your saved plot )

    # 2. Create a CTkLabel with text="" and attach the image
    img_label = CTkLabel(graph_Frame, image=plot_img, text="")
    img_label.place(x=0,y=0)  # Or use .pack() / .grid()

    var_detail.configure(text = DESCRIPTION[var_x])

apply_button = CTkButton(control_Frame, text = "Apply", width = 100, font = ("Roboto", 15, "bold"),command = apply)
apply_button.place(x = 885, y = 10)

# Create graph frame
graph_Frame = CTkFrame(app, 1000, 750, border_width = 2, border_color=BORDER_COLOUR)
graph_Frame.place(x=0, y=100)


# Create figure description frame
desc_Frame = CTkFrame(app, 600, 800, border_width=2, border_color=BORDER_COLOUR)
desc_Frame.place(x=1000, y=100)

DESCRIPTION = {
    "NDVI" : "NDVI: ",
    "EVI" : "EVI: ",
    "Sahara Surface Wind Speed": "Sahara Surface Wind Speed: ",
    "Sahara Dust Density" : "Sahara Dust Density: ",
    "Ratio of Dust Deposition over Dust Emission":"Ratio of Dust Deposition over Dust Emission: ",
    "Atlantic Wind Speed 850hPa" : "Atlantic Wind Speed 850hPa: ",
    "Atlantic Dust Density" : "Atlantic Dust Density: ",

    "Time" : f"Time: Our standard comparitive variable, used to demonstrate temporal variation for each variable under the recent time frame of {START_DATE.year} to {END_DATE.year}"
}


var_x = str(var_x_menu.get())

var_detail = CTkLabel(desc_Frame, text = f"{DESCRIPTION[var_x]}\n{DESCRIPTION["Time"]}", font = ("Roboto", 15), anchor = "w", justify = "left", wraplength = 600-30)
var_detail.place(x = 15, y = 15)

apply()


# Run the app
app.mainloop()
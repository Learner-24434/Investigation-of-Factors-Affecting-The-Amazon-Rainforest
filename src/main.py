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
    "NDVI" : "NDVI: [Normalised Difference Vegetation Index] A measurement of plant health via infrared radiation, gives values from -1 to 1, with 1 being healthiest and -1 being the least healthy. The NDVI has shown a weak negative correlation with the progression of time. The p value shows a value of 0.36, corroborating the correlation to show an insignificant statistical significance.",
    "EVI" : "EVI: [Enhanced Vegetation Index], A measurement of plant health with adjusted radiation frequncies providing more accurate readings with dense vegetation than NDVI, with the caveat of being marginally more recent and having less historical data. gives values from -1 to 1, with 1 being healthiest and -1 being the least healthy. The EVI has shown a significantly weaker negative correlation than NDVI, strongly suggesting that the NDVI added inaccuracy caused by vertically overlapping plant life is the main source of the higher (albeit still insisgnificant) statstical significance. The p value was 0.767, more than double that of NDVI.",
    "Sahara Surface Wind Speed": "Sahara Surface Wind Speed: The net wind speed as taken 10 metres over the surface of the sahara. The sahara surface wind speed had essenetially no correlation, with the best fitting line having a gradient near zero, and the p value being 0.951.",
    "Sahara Dust Density" : "Sahara Dust Density: The amount of dust per unit volume as given in kg/m³. The dust density over the sahara showed a weak negative correlation with time, though once more there was a lack of statistical significance with a p value of 0.26.",
    "Ratio of Dust Deposition over Dust Emission":"Ratio of Dust Deposition over Dust Emission: The ratio of the dust deposited in the amazon to the dust that travelled over the atlantic. The ratio between sand deposited in the Amazon and sand transferred over the atlantic has shown a weak positive trend, indicating that a greater proportion of sand transferred over the atlantic is reaching the Amazon rainforest, potentially caused by the increase in transatlantic winds. The data is, in spite of all this, statistically insignificant, having a p value of 0.126.",
    "Atlantic Wind Speed 850hPa" : "Atlantic Wind Speed 850hPa: Wind Speed at 850hPa: Wind speed taken over atlantic (850hPa being the rough atmospheric pressure at the points measured). ",
    "Atlantic Dust Density" : "Atlantic Dust Density: The amount of dust per unit volume as given in kg/m³. The dust density over the atlantic showed a slight positive correllation with the progression of time, potentially due to the increased wind speeds allowing a greater number of particles to maintain elevation. Once again there was a strong lack of statistical significance with a p value of 0.408.",
}


var_x = str(var_x_menu.get())

var_detail = CTkLabel(desc_Frame, text = DESCRIPTION[var_x], font = ("Roboto", 18), anchor = "w", justify = "left", wraplength = 600-30)
var_detail.place(x = 15, y = 15)

apply()


# Run the app
app.mainloop()
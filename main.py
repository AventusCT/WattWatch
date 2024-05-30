# UIFlow import
from m5stack import *
from m5stack_ui import *
from uiflow import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x252525)

# -----------------------------------------------------------

# API Verbinding()

# Variabelen
huidigVerbruik = 199
highWatt = 200
weatherGraden = 17
weatherStad = "Deventer"
weatherLastUpdated = "10:05"
weatherKwh = 220

# -----------------------------------------------------------


# Functies

# Centreren van tekst
def centerText(text, y_pos, color, fontsize):
    text_width = lcd.textWidth(text)
    screen_width, screen_height = lcd.screensize()  # Haal de breedte en hoogte van het scherm op
    x_pos = int((screen_width - text_width) / 2)
    Label = M5Label(text, x=x_pos, y=y_pos, color=color, font=fontsize)


# Laat het huidige verbuik zien
def showHome():
  screen.clean_screen()
  if huidigVerbruik > highWatt:
      screen.set_screen_bg_color(0xff6666)
  else:
    screen.set_screen_bg_color(0x009900)
  Label = M5Label("Huidig verbuik", 10, 5, 0xffffff, FONT_MONT_22)

  Line = M5Line(350, 120, 0, 120, 0xffffff, 2)
  wattage_text = str(huidigVerbruik) + ' Watt'
  centerText(wattage_text, 215, 0xffffff, FONT_MONT_14)

btnB.wasPressed(showHome)

# Laat het Apparaatbeheer zien
def showDevices():
  screen.clean_screen()
  screen.set_screen_bg_color(0x252525)
  Label = M5Label("Apparaatbeheer", 10, 5, 0xffffff, FONT_MONT_22)

btnC.wasPressed(showDevices)


# Laat de instellingen zien
def showSettings():
  screen.clean_screen()
  screen.set_screen_bg_color(0x252525)
  
  # Vibration, zodat je weet dat je de instellingen hebt geopend.
  power.setVibrationEnable(True)
  wait(0.2)
  power.setVibrationEnable(False)
  
  Label = M5Label("Instellingen", 10, 5, 0xffffff, FONT_MONT_22)

btnB.pressFor(0.8, showSettings)


# Laat het weerbericht zien
def showWeather():
  screen.clean_screen()
  screen.set_screen_bg_color(0x252525)
  Label = M5Label("Weer", 10, 5, 0xffffff, FONT_MONT_22)
  
  weerBox = M5Line(305, 85, 15, 85, 0xffffff, 90)
  gradenText = str(weatherGraden) + "° C"
  Graden = M5Label(gradenText, 30, 55, 0x000000, FONT_MONT_22)
  infoText = str(weatherStad) + "\nUpdated: " + str(weatherLastUpdated)
  Info = M5Label(infoText, 30, 80, 0x000000, FONT_MONT_14)
  
  zonnepaneelBox = M5Line(305, 185, 15, 185, 0xffffff, 90)
  kwhText = str(weatherKwh) + " kWh"
  KwH = M5Label(kwhText, 190, 155, 0x000000, FONT_MONT_22)
  Info = M5Label("Veel stroom opgwekt,\nmaak er gebruik van!", 130, 180, 0x000000, FONT_MONT_14)

btnA.wasPressed(showWeather)

showHome() # Default action, laat op het begin het homescreen zien
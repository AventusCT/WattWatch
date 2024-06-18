from m5stack import *
from m5stack_ui import *
from uiflow import *

# Imports voor wifi en tijd
import network
import wifiCfg
import time
import urequests
import ujson

# Defaults voor scherm
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x252525)

# Variabelen
huidigVerbruik = 450
highWatt = 200
weatherStad = "Deventer"
weatherKwh = 220

lampAan = True
API_Key = "561bfde85c3849289b7102745242504"

# Functie om te laten zien dat er is verbonden met het internet
def showConnection():
    screen.clean_screen()
    screen.set_screen_bg_color(0x009900)
    Label = M5Label("Wifi Connected", 10, 5, 0xffffff, FONT_MONT_22)

# Verbinden internet
def connectInternet():
    wifiCfg.doConnect('stevenem', 'Steven@2006!')
    if not (wifiCfg.wlan_sta.isconnected()):
        pass
    else:
        showConnection()

# API Verbinding
def weatherAPI():
    global weatherGraden, weatherLastUpdated
    try:
        req = urequests.request(method='GET', 
                                url="http://api.weatherapi.com/v1/current.json?key=" + API_Key + "&q=" + weatherStad + "&aqi=no",
                                headers={})
        data = ujson.loads(req.text)
        full_date_time = data["current"]["last_updated"]
        weatherLastUpdated = full_date_time.split(' ')[1]  # Haal alleen de tijd op
        weatherGraden = data["current"]["temp_c"]
        req.close()
    except Exception as e:
        lcd.print("ERROR: " + str(e), 0, 0, 0x000000)


# Functies

# Centreren van tekst
def centerText(text, y_pos, color, fontsize):
    text_width = lcd.textWidth(text)
    screen_width, screen_height = lcd.screensize()  # Haal de breedte en hoogte van het scherm op
    x_pos = int((screen_width - text_width) / 2)
    Label = M5Label(text, x=x_pos, y=y_pos, color=color, font=fontsize)

# Laat het huidige verbruik zien
def showHome():
    screen.clean_screen()
    if huidigVerbruik > highWatt:
        screen.set_screen_bg_color(0xff6666)
    else:
        screen.set_screen_bg_color(0x009900)
    Label = M5Label("Huidig verbruik", 10, 5, 0xffffff, FONT_MONT_22)

    Line = M5Line(350, 120, 0, 120, 0xffffff, 2)
    wattage_text = str(huidigVerbruik) + ' Watt'
    centerText(wattage_text, 215, 0xffffff, FONT_MONT_14)

btnB.wasPressed(showHome)

# Global variable to track lamp state
lampState = True

def pressed_btn():
    global lampState
    try:
        if lampState:
            lampState = False
            req = urequests.request(method='GET', url="https://app.apilio.com/webhooks/v2/logicblocks/c02faf2e-e3a5-47d1-bad8-1ea510b5e4b6/evaluate?key=28799b2bda8547440d78c37764a1d64325f14886cde1f6b562ea3a05cc4bcaa019b4d54f1012fde4752e38d44754583f17a2ccd0cf0a334cfef66f155afa5879", headers={})
            req.close()
        else:
            lampState = True
            req = urequests.request(method='GET', url="https://app.apilio.com/webhooks/v2/logicblocks/e381fd5d-a240-4e1a-94f4-484975a5f373/evaluate?key=8d60951b35bf1432604be0461819036d9d154f456db95e263cbd1959c1bbbf67b5ace36114e262a2f81acb7b42d84604aa1727d7e090048ebb905e121b81583e", headers={})
            req.close()
    except Exception as e:
        lcd.print("ERROR: " + str(e), 0, 0, 0x000000)

# Laat het Apparaatbeheer zien
def showDevices():
    screen.clean_screen()
    screen.set_screen_bg_color(0x252525)
    Label = M5Label("Apparaatbeheer", 10, 5, 0xffffff, FONT_MONT_22)
    
    apparaatBox = M5Line(110, 100, 15, 100, 0xffffff, 120)
    lampImg = M5Img("res/spots.png", x=35, y=54, parent=None)
    lamp_aan_uit = M5Btn(text='Switch', x=30, y=125, w=70, h=30, bg_c=0xFFFFFF, text_c=0x000000, font=FONT_MONT_14, parent=None)
    
    lamp_aan_uit.pressed(pressed_btn)

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
    settingBox = M5Line(305, 130, 15, 130, 0xffffff, 180)
    
    Volume = M5Label("Volume                                   >", 30, 55, 0x000000, FONT_MONT_18)
    Geluiden = M5Label("Geluiden                                 >", 30, 95, 0x000000, FONT_MONT_18)
    Helderheid = M5Label("Helderheid                             >", 30, 135, 0x000000, FONT_MONT_18)
    Themakleuren = M5Label("Themakleuren                       >", 30, 175, 0x000000, FONT_MONT_18)




btnB.pressFor(0.8, showSettings)

# Laat het weerbericht zien
def showWeather():
    screen.clean_screen()
    screen.set_screen_bg_color(0x252525)
    Label = M5Label("Weer", 10, 5, 0xffffff, FONT_MONT_22)
    
    weerBox = M5Line(305, 85, 15, 85, 0xffffff, 90)
    zonImg = M5Img("res/sun.png", x=230, y=54, parent=None)
    gradenText = str(weatherGraden) + "° C"
    Graden = M5Label(gradenText, 30, 55, 0x000000, FONT_MONT_22)
    infoText = str(weatherStad) + "\nUpdated: " + str(weatherLastUpdated)
    Info = M5Label(infoText, 30, 80, 0x000000, FONT_MONT_14)
    
    zonnepaneelBox = M5Line(305, 185, 15, 185, 0xffffff, 90)
    zonnepaneelImg = M5Img("res/zonnepaneel.png", x=30, y=154, parent=None)
    kwhText = str(weatherKwh) + " kWh"
    KwH = M5Label(kwhText, 190, 155, 0x000000, FONT_MONT_22)
    Info = M5Label("Veel stroom opgewekt,\nmaak er gebruik van!", 130, 180, 0x000000, FONT_MONT_14)

btnA.wasPressed(showWeather)

connectInternet()
weatherAPI()
showHome()  # Default action, laat op het begin het homescreen zien
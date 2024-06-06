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
huidigVerbruik = 199
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
            req = urequests.request(method='GET', url="https://app.apilio.com/webhooks/v2/logicblocks/8884b255-7fd1-4abc-afae-9b9762b7767c/evaluate?key=3dde524ed29c6358f8f296239ffb4cd1ee212fa31bf24a62836d62b8a00411eb4c9dc6bd4bed9c0218d37de6478a6ae3afb0ba0029f4916d69a133f106667aef", headers={})
            req.close()
        else:
            lampState = True
            req = urequests.request(method='GET', url="https://app.apilio.com/webhooks/v2/logicblocks/229b92b4-e26e-4c93-a738-84b9d30646e7/evaluate?key=1ac4bf2035c93978d39fe1fd66822c57666e2cdd4c041b77cdcbce362af4ff541bba8b81253626d248eefc79d8def8db2d77c737e0969ac11662bac8344ee9cb", headers={})
            req.close()
    except Exception as e:
        lcd.print("ERROR: " + str(e), 0, 0, 0x000000)

# Laat het Apparaatbeheer zien
def showDevices():
    screen.clean_screen()
    screen.set_screen_bg_color(0x252525)
    Label = M5Label("Apparaatbeheer", 10, 5, 0xffffff, FONT_MONT_22)
    
    apparaatBox = M5Line(110, 100, 15, 100, 0xffffff, 120)
    lampImg = M5Img("res/lamp.png", x=35, y=54, parent=None)
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

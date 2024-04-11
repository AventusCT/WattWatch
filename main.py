from m5stack import *
from m5stack_ui import *
from uiflow import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x252525)


# Laat de home pagina zien
def showHome():
  lcd.clear()
  lcd.print('Huidig Verbruik', 10, 5, 0xffffff)

# Laat de weerpagina zien
def showWeather():
  lcd.clear()
  lcd.print('Weer', 10, 5, 0xffffff)

# Laat her apparaatbeheer zien
def showDevices():
  lcd.clear()
  lcd.print('Apparaatbeheer', 10, 5, 0xffffff)

# Laat de instellingen menu zien
def showSettings():
  lcd.clear()
  lcd.print('Instellingen', 10, 5, 0xffffff)


btnA.wasPressed(showWeather) # Linkerknopje: weerpagina
btnB.wasPressed(showHome) # Middelste knopje: homepagina
btnC.wasPressed(showDevices) # Rechterknopje: apparaatbeheer
btnB.pressFor(0.8, showSettings) # Middelste knopje ingedrukt houden: instellingen

showHome() # Begin met het tonen van het homescreen
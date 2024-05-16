from m5stack import *
from m5stack_ui import *
from uiflow import *

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x252525)


huidigVerbruik = 1000000
highWatt = 200

def centerText(text, y_pos, color):
  text_width = lcd.textWidth(text)
  screen_width = 320
  x_pos = int((screen_width - text_width) / 2)
  lcd.print(text, x_pos, y_pos, color)


# Describe this function...
def showHome():
  global huidigVerbruik, highWatt
  lcd.clear()
  if huidigVerbruik > highWatt:
    lcd.fill(0xff6666)
  else:
    lcd.fill(0x009900)
  lcd.print('Huidig Verbruik', 10, 5, 0xffffff)
  lcd.line(350, 120, 0, 120, 0xffffff)
  wattage_text = str(huidigVerbruik) + ' Watt'
  centerText(wattage_text, 220, 0xffffff)


# Describe this function...
def showDevices():
  global huidigVerbruik, highWatt
  lcd.clear()
  lcd.print('Apparaatbeheer', 10, 5, 0xffffff)

# Describe this function...
def showSettings():
  global huidigVerbruik, highWatt
  lcd.clear()
  lcd.print('Instellingen', 10, 5, 0xffffff)
  lcd.qrcode('Test', x=0, y=0, width=220, version=6)


# Describe this function...
def showWeather():
  global huidigVerbruik, highWatt
  lcd.clear()
  lcd.print('Weer', 10, 5, 0xffffff)


def buttonB_pressFor():
  power.setVibrationEnable(True)
  wait(0.2)
  power.setVibrationEnable(False)
  global huidigVerbruik, highWatt
  showSettings()
  pass
btnB.pressFor(0.8, buttonB_pressFor)

def buttonA_wasPressed():
  global huidigVerbruik, highWatt
  showWeather()
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonC_wasPressed():
  global huidigVerbruik, highWatt
  showDevices()
  pass
btnC.wasPressed(buttonC_wasPressed)

def buttonB_wasPressed():
  global huidigVerbruik, highWatt
  showHome()
  pass
btnB.wasPressed(buttonB_wasPressed)


showHome()
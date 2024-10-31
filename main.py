#!/usr/bin/env python
#-- coding: utf-8 --

from RPLCD.i2c import CharLCD
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time

# Définition des broches LED
LED_RED = 11   # Correspond à GPIO17 en mode BCM
LED_GREEN = 13 # Correspond à GPIO27 en mode BCM
BUZZER = 37 # Correspond à GPIO19 en mode BCM

DEFAULT_MESSAGE= "Attente badge..."

GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board) il faut noter les numéros de pin
GPIO.setwarnings(False) #On désactive les messages d'alerte
GPIO.setup(BUZZER,GPIO.OUT)

# Configuration de l'écran LCD
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)


# Fonction pour l'affichage sur l'écran LCD
def display_message(line1, line2=""):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string(line1[:16])  # Limite à 16 caractères
    if line2:
        lcd.cursor_pos = (1, 0)
        lcd.write_string(line2[:16])  # Limite à 16 caractères


#Définit la fonction permettant d'allumer une led
def turn_led_on (led) :
    GPIO.setup(led, GPIO.OUT) #Active le contrôle du GPIO
    GPIO.output(led, GPIO.HIGH) #Allume la led
    time.sleep(5)
    GPIO.output(led, GPIO.LOW) #Eteind la led
    display_message(DEFAULT_MESSAGE) #Re-affiche le message par défaut


#Définit la fonction permettant d'éteindre une led
def turn_led_off (led) :
    GPIO.setup(led, GPIO.OUT) #Active le contrôle du GPIO
    GPIO.output(led, GPIO.LOW) #Eteind la led

#Définit la fonction permettant d'allumer la rouge et éteindre la verte
def turn_red_on () :
    turn_led_off(LED_GREEN) #Eteind la led verte
    turn_led_on(LED_RED) #Allume la led rouge

#Définit la fonction permettant d'allumer la verte et éteindre la rouge
def turn_green_on () :
    turn_led_off(LED_RED) #Eteind la led rouge
    turn_led_on(LED_GREEN) #Allume la led verte

def play_sound () :
    GPIO.output(BUZZER, GPIO.HIGH)

def stop_sound () :
    GPIO.output(BUZZER, GPIO.LOW)


# Définir les UID des badges valides
valid_uids = {974975851054}

# Initialiser le lecteur RFID
reader = SimpleMFRC522()

try:
    print("En attente d'un badge RFID...")
    display_message(DEFAULT_MESSAGE)

    while True:
        # Lire l'UID du badge
        id, text = reader.read()

        # Vérifier si l'UID est dans la liste des UIDs valides
        if id in valid_uids:
            print(f"Badge valide détecté ! UID : {id}")
            display_message("Badge valide",f"UID: {id}")
            turn_green_on()
        else:
            print(f"Badge invalide détecté. UID : {id}")
            display_message("Badge invalide",f"UID: {id}")
            play_sound()
            turn_red_on()
            stop_sound()

        # Délai pour éviter les multiples lectures successives
        time.sleep(1)

except KeyboardInterrupt:
    print("Arrêt du programme.")

finally:
    GPIO.cleanup()
    lcd.close(clear=True)

# RFID-LCD  
  
 [![Raspberri Pi RFID LCD](https://img-storage-files.s3.eu-west-1.amazonaws.com/Capture+d%E2%80%99e%CC%81cran+2024-10-31+a%CC%80+17.31.45.png)](https://youtu.be/SFu8QFPjPXc "Raspberri Pi RFID LCD")

## Table of Contents  
  
1. [Matériel requis](#matériel-requis)  
2. [Branchements des broches GPIO](#branchements-des-broches-gpio)  
2.1 [Connexion de l'écran LCD](#connexion-de-lécran-lcd)   
2.2 [Connexion du lecteur RFID (RC522)](#connexion-du-lecteur-rfid-rc522)  
2.3 [Connexion des diodes, résistance et buzzer](#connexion-des-diodes-résistance-et-buzzer)  
3. [Activer les interfaces I2C et SPI](#activer-les-interfaces-i2c-et-spi)  
3.1 [Activer l'interface I2C](#activer-linterface-i2c)  
3.2 [Activer de l'interface SPI](#activer-linterface-spi)  
4. [Préparation de l'environnement de développement sur le Raspberry Pi](#préparation-de-lenvironnement-de-développement-sur-le-raspberry-pi)  
4.1 [Configuration d'un répertoire pour les scripts Python et Environnement](#configuration-dun-répertoire-pour-les-scripts-python-et-environnement)  
4.2 [Créer un environnement virtuel Python](#créer-un-environnement-virtuel-python)  
4.3 [Installation des bibliothèques requises dans l'environnement virtuel.](#installation-des-bibliothèques-requises-dans-lenvironnement-virtuel)  
5. [Le code Python](#le-code-python)  
6. [Exécution du projet](#exécution-du-projet)   
7. [Installation rapide](#installation-rapide)  
  
### Circuit Design Raspberry PI  
  
![enter image description here](https://img-storage-files.s3.eu-west-1.amazonaws.com/raspberry4.png)  
  
  
![enter image description here](https://img-storage-files.s3.eu-west-1.amazonaws.com/schematic-view.png)  
  
## Matériel requis  
  
- Raspberry Pi 4  
- Lecteur RFID RC522  
- Écran LCD 1602 RGB  
- Diodes rouge et verte  
- Résistance 220  
- Buzzer actif  
  
## Branchements des broches GPIO  
  
#### Connexion de l'écran LCD:  
  
L'écran Waveshare LCD 1602 RGB utilise la communication I2C. Connectez l'écran comme suit:  
| **Raspberry PI** | **16*2 LCD** |   
|--|--|  
| GPIO 2 (SDA) | SDA Pin |   
| GPIO 3 (SCL) | SCL Pin |  
| +5 Volt | VCC |  
| GND | GND |  
  
#### Connexion du lecteur RFID (RC522):  
  
Le module RFID RC522 utilise la communication SPI pour interagir avec le Raspberry Pi. Connectez le lecteur RFID comme suit:  
  
| **Raspberry PI** | **Lecteur RFID** |   
|--|--|  
| GPIO 8 (CEO) | SDA  |   
| GPIO 11 (SCK) | SCK |  
| GPIO 10 (MOSI) | MOSI |  
| GPIO 9 (MISO) | MISO |  
| ❗️Not connected | IRQ |  
| GND | GND |  
| GPIO 25 | RST |  
| +5 Volt | VCC |  
  
#### Connexion des diodes, résistance et buzzer:  
  
Se reporter au schéma.  
  
## Activer les interfaces I2C et SPI  
  
### Activer l'interface I2C  
  
Pour utiliser des appareils I2C, vous devez activer l’interface sur votre Raspberry Pi.   
  
#### Activation de l'I2C sur le Raspberry Pi à l'aide d'une simple commande  
  
En utilisant **raspi-config**, nous pouvons définir l'état du port I2C.   
  
##### Voici comment activer le port I2C :  
```bash  
  sudo raspi-config nonint do_i2c 0  
```  
notez que  **0 signifie vrai ou vrai**  
  
##### Voici comment désactiver le port I2C :  
```bash  
  sudo raspi-config nonint do_i2c 1  
```  
1 signifie "faux" ou désactivé.  
  
##### Pour vérifier si c'est bien activer :  
```bash  
  lsmod | grep i2c  
```  
  
Si l'I2C est activé, vous verrez une liste de modules `i2c`, comme `i2c_bcm2835` et `i2c_dev`.  
  
Utiliser   
  
`sudo apt install -y i2c-tools`  
```bash  
  sudo i2cdetect-y 1  
```  
  
commande dans le terminal pour vérifier l'adresse de l'affichage. Par défaut, I2C apparaîtra à l’adresse 0x27. Assurez-vous de modifier le code dans la bibliothèque ci-dessous si celui-ci est différent.  
  
  
### Activer l'interface SPI  
  
Encore une fois, en utilisant **raspi-config**, nous pouvons définir l'état du port SPI.   
  
##### Voici comment activer le port SPI :  
```bash  
  sudo raspi-config nonint do_spi 0  
```  
notez que  **0 signifie vrai ou vrai**  
  
##### Voici comment désactiver le port SPI :  
```bash  
  sudo raspi-config nonint do_spi 1  
```  
1 signifie "faux" ou désactivé.  
  
##### Pour vérifier si c'est bien activer :  
```bash  
  lsmod | grep spi  
```  
Si le SPI est actif, vous verrez des modules comme `spi_bcm2835`.  
  
  
  
### Préparation de l'environnement de développement sur le Raspberry Pi  
  
**1.** Avant de commencer la programmation, nous devons d'abord [mettre à jour notre Raspberry Pi](https://pimylifeup.com/update-raspbian/) pour s'assurer qu'il exécute la dernière version de tous les logiciels. Exécutez les deux commandes suivantes sur votre Raspberry Pi pour le mettre à jour.  
  
```bash  
  sudo apt update  
  sudo apt upgrade -y  
```  
  
**2.** Maintenant, la dernière chose dont nous avons besoin avant de pouvoir procéder est d'installer `python3-dev`, `python3-pip` et `python3-venv` paquets.  
  
Exécutez simplement la commande suivante sur votre Raspberry Pi pour installer tous les packages requis pour ce guide sur la configuration de votre lecteur RFID.  
  
```bash  
  sudo apt install python3-dev python3-pip python3-venv -y  
```  
  
### Configuration d'un répertoire pour les scripts Python et Environnement  
  
**3.** Notre prochaine étape est de créer un répertoire où nous allons stocker les scripts que nous écrivons ainsi que l'environnement virtuel Python.  
  
Les versions récentes de Raspberry Pi OS nécessitent que les packages installés à l'aide de pip soient stockés dans un environnement virtuel.  
  
Vous pouvez créer ce répertoire en utilisant la commande suivante dans le terminal.  
  
```bash  
  mkdir ~/raspberry-rfid-lcd  
```  
  
**4.** Après avoir créé le répertoire, changez-le en utilisant la commande suivante.  
  
```bash  
  cd ~/raspberry-rfid-lcd  
```  
  
### Créer un environnement virtuel Python  
  
**5.** Maintenant, nous devons utiliser Python pour générer un environnement virtuel dans un répertoire appelé “`env`“.  
  
Nous devons utiliser cet environnement virtuel chaque fois que nous voulons exécuter nos scripts et installer d'autres paquets Python.  
  
```bash  
  python3 -m venv env  
```  
  
**6.** Une fois que Python a fini de générer l'environnement virtuel, utilisez la commande ci-dessous pour commencer à l'utiliser.  
  
Une fois que nous utilisons l'environnement virtuel, les paquets Python que nous installons à l'aide de pip seront conservés dans cet environnement, pas dans l'environnement global.  
  
```bash  
  source ~/raspberry-rfid-lcd/env/bin/activate  
```  
  
Après avoir exécuté la commande ci-dessus, vous devriez voir que votre ligne de terminal commence par “`(env)`“.  
  
### Installation des bibliothèques requises dans l'environnement virtuel.  
  
**7.** Pour faire fonctionner notre project, nous auront besoins des librairies suivante, **RPi.GPIO**, **spidev**, **MFRC522**, **RPLCD** et enfin **smbus2**. Avant d'installer les différentes bibliothèques, revenons sur chacune d'elle et son utilité :  
  
- La bibliothèque **RPi.GPIO** est une librairie Python conçue pour contrôler les broches GPIO (General Purpose Input/Output) des Raspberry Pi. Elle permet de configurer les broches en entrée ou sortie, de lire et écrire des valeurs numériques (0 ou 1), et de gérer les interruptions (events) pour réagir aux changements d'état des broches. RPi.GPIO est souvent utilisée pour piloter des composants comme des LED, des boutons, des relais, et d'autres périphériques dans des projets d'automatisation et d'IoT.  
  
- **spidev** est une bibliothèque Python qui fournit une interface pour le protocole SPI (Serial Peripheral Interface) sur les broches GPIO du Raspberry Pi. Elle permet de configurer la fréquence d'horloge, la polarité, le nombre de bits et le mode SPI, puis d'envoyer et recevoir des données sous forme de bits. Utilisée pour communiquer avec divers périphériques compatibles SPI comme les capteurs, les écrans et les modules RFID, spidev simplifie l'échange de données en duplex intégral, idéal pour les projets IoT ou d'électronique embarquée.  
  
- **MFRC522** est une bibliothèque Python destinée à interagir avec le module RFID RC522, un lecteur de cartes et tags RFID fonctionnant à 13,56 MHz. Elle permet de configurer le lecteur, détecter les tags à proximité, lire et écrire des données sur les tags compatibles MIFARE, et gérer l'authentification de blocs mémoire. La bibliothèque est couramment utilisée sur Raspberry Pi pour des projets nécessitant une identification par RFID, comme des systèmes de contrôle d'accès ou des caisses intelligentes.  
  
- **RPLCD** est une bibliothèque Python facilitant le contrôle d’écrans LCD compatibles HD44780 via les protocoles GPIO, I2C ou SPI sur Raspberry Pi. Elle simplifie l'affichage de texte et la gestion des fonctionnalités de l'écran (défilement, curseur, nettoyage). RPLCD est idéale pour afficher des informations dynamiques ou des messages dans des projets d’interface utilisateur pour l’IoT et l’électronique embarquée.  
  
- **smbus2** est une bibliothèque Python qui fournit une interface simplifiée pour communiquer avec des périphériques I2C en utilisant le protocole SMBus (System Management Bus) sur les broches GPIO des Raspberry Pi et autres cartes. Elle permet de lire et d’écrire des données facilement depuis et vers des capteurs, des afficheurs, et divers modules I2C, tout en étant compatible avec la bibliothèque standard `smbus`. Souvent utilisée pour les projets de capteurs en électronique, smbus2 offre des fonctionnalités pratiques comme les transferts de données en blocs et le support de répétitions pour une communication fiable.  
  
**8.** Maintenant, nous pouvons installer les bibliothèques nécessaires au fonctionnement du lecteur RFID et de l'écran LCD.  
  
```bash  
  pip install RPi.GPIO spidev mfrc522 RPLCD smbus2  
```  
  
## Le code Python  
  
**9.** Créer un fichier `main.py` dans le répertoire `raspberry-rfid-lcd` puis copiez/coller le code ci-dessous :  
  
```python  
#!/usr/bin/env python    
#-- coding: utf-8 --    
    
from RPLCD.i2c import CharLCD    
from mfrc522 import SimpleMFRC522    
import RPi.GPIO as GPIO    
import time    
    
# Définition des broches LED    
LED_RED = 11 # Correspond à GPIO17 en mode BCM    
LED_GREEN = 13 # Correspond à GPIO27 en mode BCM    
BUZZER = 37 # Correspond à GPIO19 en mode BCM    
    
DEFAULT_MESSAGE= "Attente badge..."    
  
# Définir les UID des badges valides ici    
valid_uids = {badge_valide_1, badge_valide_x}    
    
GPIO.setmode(GPIO.BOARD) #Définit le mode de numérotation (Board) il faut noter les numéros de pin    
GPIO.setwarnings(False) #On désactive les messages d'alerte    
GPIO.setup(BUZZER,GPIO.OUT)    
    
# Configuration de l'écran LCD    
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)    
    
    
# Fonction pour l'affichage sur l'écran LCD    
def display_message(line1, line2=""):    
  lcd.clear()    
  lcd.cursor_pos = (0, 0)    
  lcd.write_string(line1[:16]) # Limite à 16 caractères    
  if line2:    
  lcd.cursor_pos = (1, 0)    
  lcd.write_string(line2[:16]) # Limite à 16 caractères    
    
    
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
```  
  
## Exécution du projet  
    
- **Connectez les Composants**: Assurez-vous que votre lecteur RFID RC522, votre écran LCD 1602 RGB et les autres composants sont correctement connectés au Raspberry Pi.  
- **Exécutez le script**: Exécutez le script avec Python :  
  
```bash  
python main.py  
```  
  
  Vous pouvez retrouver le projet complet en suivant le lien suivant: 
  
  
  
## Installation rapide  
  
- Installer git  
```bash
sudo apt install git  
```
- Cloner le repository github sur le raspberry:

```bash
  git clone https://github.com/Xipotera/raspberry-rfid-lcd
  cd raspberry-rfid-lcd
```

- Exécuter le script d'installation automatique en utilisant `sudo`:

```bash
  sudo ./install.sh  
```
⚠️ Pendant l'installation, faites attention aux messages concernant l'utilisation de « python » et « python3 ».

- À la fin du script d'installation, vous serez invité à redémarrer le RPi pour appliquer les modifications notament sur l'activation des interfaces EC2 et SPI.

- Après le redémarrage, activons l'environnement virtuel :
```bash
  source ~/raspberry-rfid-lcd/env/bin/activate
```

puis :
```bash  
  ./raspberry-rfid-lcd/main.py  
 ```  
  ou
  
```bash  
  python ~/raspberry-rfid-lcd/main.py  
 ```  
  ou 
  
```bash  
  python3 ~/raspberry-rfid-lcd/main.py  
 ```  


[top :arrow_up:](#table-of-contents)
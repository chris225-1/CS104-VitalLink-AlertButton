import os
import time
import requests
import RPi.GPIO as GPIO

BOT_TOKEN = "8771794213:AAEQmW5oA0EPzz1dQAFxj7r4ht8lEPhgEHo"    
CHAT_ID = "8874172754"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram_alert(message):
    try:
        response = requests.post(
            TELEGRAM_URL,
            json={"chat_id": CHAT_ID, "text": message},
            timeout=10,
        )
        if response.ok:
            print("Telegram alert sent.")
        else:
            print("Telegram error:", response.status_code, response.text)
    except requests.RequestException as e:
        print("Could not reach Telegram:", e)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("Alert button monitoring system is now active. Press Ctrl+C to stop.")

button_pressed = False
try:
    while True:
        if GPIO.input(7) == GPIO.HIGH and not button_pressed:
            print("Someone pressed the alert button!")
            send_telegram_alert("Someone pressed the alert button!")
            button_pressed = True
        elif GPIO.input(7) == GPIO.LOW:
            button_pressed = False
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nMonitoring stopped.")
    GPIO.cleanup()

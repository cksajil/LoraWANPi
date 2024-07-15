"""
Example for using the Shield Fox LoRa with Raspberry Pi and LoRaWAN
 
Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Lucas Maziero for Fox IoT (lucasmaziero@foxiot.com.br) (Adapted)
"""

import time
import busio
from digitalio import DigitalInOut
from random import randint
import board

# Import Adafruit TinyLoRa
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa

# TinyLoRa Configuration
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.D25)
irq = DigitalInOut(board.D23)
rst = DigitalInOut(board.D17)

# TTN Device Address, 4 Bytes, MSB
devaddr = bytearray([0xFC, 0x00, 0x96, 0x41])
# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray(
    [
        0x68,
        0x9F,
        0xAE,
        0x57,
        0xCF,
        0x18,
        0xF8,
        0x1B,
        0xD4,
        0xE4,
        0x50,
        0x6C,
        0x1E,
        0x62,
        0xDF,
        0xB1,
    ]
)

# TTN Application Key, 16 Bytes, MSB
app = bytearray(
    [
        0xE8,
        0x94,
        0xF7,
        0x6F,
        0xCF,
        0xBE,
        0xEC,
        0xB1,
        0x99,
        0x83,
        0x3C,
        0x06,
        0x1A,
        0x7A,
        0x54,
        0x21,
    ]
)

# Initialize ThingsNetwork configuration
ttn_config = TTN(devaddr, nwkey, app, country="IN")
# Initialize lora object
lora = TinyLoRa(spi, cs, irq, rst, ttn_config, 0)

# Select spreading factor
lora.set_datarate("SF12BW125")
# 2-byte array to store sensor data
data_pkt = bytearray(2)
# time to delay periodic packet sends (in seconds)
data_pkt_delay = 5.0


def send_pi_data_periodic():
    send_pi_data(3.14)


def send_pi_data(data, ch_first=0, ch_last=7):
    # Encode float as int
    data = int(data * 100)
    # Encode payload as bytes
    data_pkt[0] = (data >> 8) & 0xFF
    data_pkt[1] = data & 0xFF
    # Select random channel
    channel = randint(ch_first, ch_last)
    lora.set_channel(channel)

    print(f"Sending data on channel: {channel}")
    print(f"Data to send: {data_pkt}")

    # Send data packet
    lora.send_data(data_pkt, len(data_pkt), lora.frame_counter, timeout=5)
    lora.frame_counter += 1

    # Retrieve debug information
    freq = lora._frequencies

    print("Data sent!")
    print(f"Counter: {lora.frame_counter}")
    print(f"Frequency: {freq} Hz")
    time.sleep(0.5)


send_pi_data_periodic()

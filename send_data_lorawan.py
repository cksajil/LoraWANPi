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
devaddr = bytearray([0xFC, 0x00, 0x96, 0xCC])
# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray(
    [
        0x6A,
        0x9D,
        0x80,
        0x15,
        0x0E,
        0x4E,
        0xD6,
        0xDA,
        0xDA,
        0x2B,
        0x2C,
        0xFD,
        0x82,
        0x2C,
        0x63,
        0x78,
    ]
)

# TTN Application Key, 16 Bytes, MSB
app = bytearray(
    [
        0x36,
        0x19,
        0x82,
        0x23,
        0x07,
        0x29,
        0x08,
        0xDA,
        0x7A,
        0x6C,
        0x09,
        0x77,
        0x11,
        0x81,
        0xA2,
        0x1C,
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
# Time to delay periodic packet sends (in seconds)
data_pkt_delay = 10.0


def send_pi_data_periodic():
    while True:
        send_pi_data(3.14)
        time.sleep(data_pkt_delay)


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
    lora.send_data(data_pkt, len(data_pkt), lora.frame_counter, timeout=30)
    lora.frame_counter += 1

    # Retrieve debug information
    # freq = lora._frequencies

    print("Data sent!")
    print(f"Counter: {lora.frame_counter}")
    # print(f"Frequency: {freq} Hz")


send_pi_data_periodic()

# Receiving in gateway

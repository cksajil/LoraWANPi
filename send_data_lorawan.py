import time
import busio
from digitalio import DigitalInOut, Direction
from random import randint
import board

# Import Adafruit TinyLoRa
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa

# TinyLoRa Configuration
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = DigitalInOut(board.D25)
irq = DigitalInOut(board.D23)
rst = DigitalInOut(board.D17)

# Configure LEDs
led1 = DigitalInOut(board.D27)
led1.direction = Direction.OUTPUT
led2 = DigitalInOut(board.D22)
led2.direction = Direction.OUTPUT

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
data_pkt_delay = 3.0


def send_pi_data_periodic():
    try:
        while True:
            # led1.value = True  # Turn on LED 1 when device is active
            send_pi_data(1)
            time.sleep(data_pkt_delay)
            # led1.value = False  # Turn off LED 1 when not sending data
    except KeyboardInterrupt:
        print("Periodic data sending interrupted by user")


def send_pi_data(data, ch_first=0, ch_last=2):
    # Encode float as int
    data = int(data)
    # Encode payload as bytes
    data_pkt[0] = (data >> 8) & 0xFF
    data_pkt[1] = data & 0xFF
    # Select random channel
    channel = randint(ch_first, ch_last)
    lora.set_channel(channel)

    print(f"Sending data on channel: {channel}")
    print(f"Data to send: {data_pkt}")

    led2.value = True  # Turn on LED 2 when data is being transmitted

    # Send data packet
    lora.send_data(data_pkt, len(data_pkt), lora.frame_counter, timeout=8)
    lora.frame_counter += 1

    led2.value = False  # Turn off LED 2 after data is sent

    # Retrieve debug information
    # freq = lora._frequencies

    print("Data sent!")
    print(f"Counter: {lora.frame_counter}")
    # print(f"Frequency: {freq} Hz")


send_pi_data_periodic()

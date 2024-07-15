# Library for [Shield LoRaWAN Raspberry Pi](https://github.com/lucasmaziero/lmic-rpi-fox/blob/master/Shield_Lora_Foxiot.pdf) (developed by [Fox IoT](http://foxiot.com.br/)) 

This library provides an interface between hardware and software, consisting of a LoRa chip [RFM95](http://www.hoperf.com/upload/rf/RFM95_96_97_98W.pdf) 
operating at a frequency of 915 MHz and three indicator LEDs, one green indicating power on and two red general purpose ones that can be configured to indicate some type of system status. 

Note: The construction of this library was based on [lmic_pi](https://github.com/dragino/lmic_pi) with some adaptations to be 
compatible with the LoRaWAN network of the [Federal University of Santa Maria](https://www.ufsm.br/). 

## First steps before downloading the library 

- Format the SD card with [SD Memory Card Formatter](https://www.sdcard.org/downloads/formatter_4/) 
- Install the Raspbian operating system on the Raspberry Pi, which can be installed via [NOOBS](https://www.raspberrypi.org/downloads/noobs/) 
- Enable the SPI interface in preferences => Raspberrry pi configuration => interfaces 

## Installing the WiringPi library 

The [WiringPi](https://github.com/WiringPi/WiringPi) library provides the Raspberry Pi GPIO interface 


- Clone the repository 

  $ git clone https://github.com/WiringPi/WiringPi.git 

- Access the wiringPi folder 

  $ cd wiringPi 

- Build the lib 

  $ ./build 

## Installing the library [lmic-rpi-fox](https://github.com/lucasmaziero/lmic-rpi-fox.git) 

- Clone the repository 

  $ git clone https://github.com/lucasmaziero/lmic-rpi-fox.git 

- Access the lmic-rpi-fox folder 

  $ cd lmic-rpi-fox/examples/ttn-abp-send 

- Make the project (remembering that any changes made to the code later must be executed with the "make" command) 

  $ make 

- Running the program 

  $ ./ttn-abp-send 

## Hardware mapping 

The complete WiringPi pin mapping can be seen [here](https://github.com/lucasmaziero/lmic-rpi-fox/blob/master/Raspberry%20Pi%20GPIO%20Pins.png) 

WiringPi 0 == Reset 
  
WiringPi 4 == DIO0 

WiringPi 5 == DIO1 

WiringPi 1 == DIO2 (Not used) 
  
WiringPi 12 == MOSI 
  
WiringPi 13 == MISO 
  
WiringPi 14 == SCK 

WiringPi 6 == SS 

WiringPi 2 == LED1 

WiringPi 3 == LED2 
  
GND == GND 
  
3.3V == +3.3V   

## License

Content is licensed under the MIT License. See [License File](LICENSE) for more information.
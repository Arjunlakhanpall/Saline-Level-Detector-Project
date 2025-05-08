# Raspberry Pi Python code for saline level detector using MCP3008 ADC
import spidev
import time
import RPi.GPIO as GPIO

# GPIO setup for LED
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# SPI setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Read from MCP3008 ADC
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# Convert ADC value to salinity percentage (calibrate as needed)
def convert_to_salinity(adc_value):
    # Example: Map ADC 0-1023 to 0-100% salinity
    # Adjust based on calibration with known saline solutions
    max_adc = 1023
    salinity = (adc_value / max_adc) * 100
    return salinity

try:
    while True:
        saline_value = read_adc(0) # Read from channel 0 (probe connected)
        salinity_percent = convert_to_salinity(saline_value)
        
        print(f"ADC Value: {saline_value}, Salinity: {salinity_percent:.2f}%")
        
        # Indicate high salinity with LED
        if saline_value > 500: # Adjust threshold based on calibration
            GPIO.output(LED_PIN, GPIO.HIGH)
            print("High Salinity Detected!")
        else:
            GPIO.output(LED_PIN, GPIO.LOW)
        
        time.sleep(1) # Delay for readability

except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup()
    spi.close()
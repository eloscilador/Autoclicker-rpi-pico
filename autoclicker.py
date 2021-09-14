import time
import usb_hid
import board
import digitalio
import pwmio
from adafruit_hid.mouse import Mouse

# Init mouse
m = Mouse(usb_hid.devices)

# Init button
button = digitalio.DigitalInOut(board.GP19)
button.switch_to_input(pull=digitalio.Pull.DOWN)

# Reset button
buttonReset = digitalio.DigitalInOut(board.GP18)
buttonReset.switch_to_input(pull=digitalio.Pull.DOWN)

# Leds
led1 = pwmio.PWMOut(board.GP12, frequency=1000, duty_cycle=0)
led2 = pwmio.PWMOut(board.GP13, frequency=1000, duty_cycle=0)
led3 = pwmio.PWMOut(board.GP14, frequency=1000, duty_cycle=0)
led4 = pwmio.PWMOut(board.GP15, frequency=1000, duty_cycle=0)

# Six seconds between each click
duty_max = 6000

##############################################
# Autclick
def start():
    while buttonReset.value == False:
        for i in range(100):
            # PWM LED up and down
            if i < 50:
                led1.duty_cycle = int(i * 2 * duty_max / 100)  
                led2.duty_cycle = int(i * 2 * duty_max / 100)  
                led3.duty_cycle = int(i * 2 * duty_max / 100)  
            else:
                led1.duty_cycle = duty_max - int((i - 50) * 2 * duty_max / 100)
                led2.duty_cycle = duty_max - int((i - 50) * 2 * duty_max / 100)
                led3.duty_cycle = duty_max - int((i - 50) * 2 * duty_max / 100)
            time.sleep(0.05)
        
        # Click the left mouse button.
        m.click(Mouse.LEFT_BUTTON)
        
        # On Leds
        led1.duty_cycle = 0
        led2.duty_cycle = 0
        led3.duty_cycle = 0
    
    # Exit loop and go to main
    main()        
        
        
##############################################
# Main Function
def main():
    m.release_all()
    led4.duty_cycle = 5000
    
    if button.value == True:
        led4.duty_cycle = 0
        start()
        
    time.sleep(0.1)

while True:
    main()
    

#
# from gpiozero import LED, Button, PWMLED
#
# # setup LEDs
# led_1 = LED(33)
# led_2 = LED(35)
# led_complex = PWMLED(37)
# # setup Button
# button_1 = Button(31)
#
# # turn lights off
# led_1.off()
# led_2.off()
# led_complex.value = 0
#
#
# def check_button():
#     if button_1.is_pressed:
#         print("Button 1 pressed")
#         led_1.on()
#         led_2.on()
#         led_complex.value = 1
#     else:
#         print("Button 1 not pressed")
#         led_1.off()
#         led_2.off()
#         led_complex.value = 0
#
#
# while True:
#     check_button()

from gpiozero import PWMLED, Button

# setup PWM LEDs for RGB imitation
led_red = PWMLED(33)
led_green = PWMLED(35)
led_blue = PWMLED(37)
# setup Button
button_1 = Button(31)

def check_button():
    if button_1.is_pressed:
        print("Button 1 pressed")
        led_red.value = 1
        led_green.value = 0.5  # You can change this value for color mixing
        led_blue.value = 0.2   # You can change this value for color mixing
    else:
        print("Button 1 not pressed")
        led_red.value = 0
        led_green.value = 0
        led_blue.value = 0

while True:
    check_button()

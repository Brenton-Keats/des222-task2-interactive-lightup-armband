def on_button_pressed_a():
    global max_brightness, colour_index
    max_brightness = 1
    colour_index += 1
    if colour_index >= len(colour_modes):
        colour_index = 0
    resetTimer()
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global max_brightness, light_index
    max_brightness = 1
    light_index += 1
    if light_index >= len(light_modes):
        light_index = 0
    resetTimer()
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_gesture_shake():
    resetTimer()
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

def resetTimer():
    global last_shake
    last_shake = input.running_time()
def plotBrightness(brightness: number):
    basic.clear_screen()
    index = 0
    while index <= Math.floor(brightness / 10):
        led.plot(index % 5, Math.floor(index / 5))
        index += 1
current_light_mode = ""
current_colour = 0
max_brightness = 0
colour_index = 0
colour_modes: List[number] = []
light_index = 0
light_modes: List[str] = []
last_shake = 0
strip = neopixel.create(DigitalPin.P2, 30, NeoPixelMode.RGB)
active = True
tickrate = 20
last_shake = input.running_time()
off_timer = 10000 * 1000
light_modes = ["SOLID", "FLASH", "BREATH", "RAINBOW"]
light_index = 0
colour_modes = [neopixel.colors(NeoPixelColors.WHITE),
    neopixel.colors(NeoPixelColors.RED),
    neopixel.colors(NeoPixelColors.BLUE),
    neopixel.colors(NeoPixelColors.GREEN),
    neopixel.colors(NeoPixelColors.ORANGE),
    neopixel.colors(NeoPixelColors.PURPLE)]
colour_index = 0
max_brightness = 1

def on_forever():
    global current_colour, current_light_mode
    if active:
        current_colour = colour_modes[colour_index]
        current_light_mode = light_modes[light_index]
        if current_light_mode == "RAINBOW":
            for index2 in range(361):
                if not (active) or light_modes[light_index] != "RAINBOW":
                    break
                strip.show_rainbow(index2 + 1, 360 + index2)
                basic.pause(tickrate)
        elif current_light_mode == "SOLID":
            strip.show_color(current_colour)
        elif current_light_mode == "FLASH":
            strip.show_color(current_colour)
            basic.pause(200)
            strip.show_color(neopixel.colors(NeoPixelColors.BLACK))
            basic.pause(150)
        elif current_light_mode == "BREATH":
            index3 = 0
            while index3 <= max_brightness:
                if not (active) or light_modes[light_index] != "BREATH":
                    break
                strip.set_brightness(max_brightness - index3)
                strip.show_color(current_colour)
                basic.pause(10)
                index3 += 1
            index4 = 0
            while index4 <= max_brightness:
                if not (active) or light_modes[light_index] != "BREATH":
                    break
                if index4 > max_brightness:
                    break
                strip.set_brightness(min(index4, max_brightness))
                strip.show_color(current_colour)
                basic.pause(10)
                index4 += 1
        basic.pause(tickrate)
basic.forever(on_forever)

def on_in_background():
    global active
    while True:
        if input.running_time() - last_shake > off_timer:
            active = False
            strip.clear()
            strip.show()
        else:
            active = True
        basic.pause(tickrate)
control.in_background(on_in_background)

# Limits power consumption of the Neopixel strip

def on_in_background2():
    global max_brightness
    while True:
        if strip.power() >= 600:
            max_brightness += -1
        elif strip.power() <= 500:
            max_brightness += 1
        max_brightness = Math.constrain(max_brightness, 0, 255)
        strip.set_brightness(max_brightness)
        plotBrightness(max_brightness)
        basic.pause(4)
control.in_background(on_in_background2)

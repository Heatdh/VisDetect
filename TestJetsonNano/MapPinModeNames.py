import Jetson.GPIO as GPIO

board_to_tegra = {
k: list(GPIO.gpio_pin_data.get_data()[-1]['TEGRA_SOC'].keys())[i] for i, k in enumerate(GPIO.gpio_pin_data.get_data()[-1]['BOARD'])}

for k, v in board_to_tegra.items():
    print('board #:', k, 'tegra:', v)
gpio_engine = None

left_taptic_p_pin = 16
left_taptic_p_pwm = None
left_taptic_n_pin = 19
left_taptic_n_pwm = None

right_taptic_p_pin = 20
right_taptic_p_pwm = None
right_taptic_n_pin = 26
right_taptic_n_pwm = None

target_left_freq = 0
target_right_freq = 0

target_left_amp = 0
target_right_amp = 0


def shutdown():
    pass


def init():
    global gpio_engine
    global left_taptic_p_pwm
    global left_taptic_n_pwm
    global right_taptic_p_pwm
    global right_taptic_n_pwm
    if gpio_engine is None:
        print("very fucked: there is no gpio_engine lol")
        raise OSError
    # left_taptic_p_pwm = gpio_engine.set_pwm(left_taptic_p_pin, 100, "left_p_pwm")
    # left_taptic_n_pwm = gpio_engine.set_pwm(left_taptic_n_pin, 100, "left_n_pwm")
    # right_taptic_p_pwm = gpio_engine.set_pwm(right_taptic_p_pin, 100, "right_p_pwm")
    # right_taptic_n_pwm = gpio_engine.set_pwm(right_taptic_n_pin, 100, "right_n_pwm")
    pass

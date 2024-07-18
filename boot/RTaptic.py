gpio_engine = None

line_left_p = None
line_left_n = None
line_right_p = None
line_right_n = None

pwm_left_p = None
pwm_left_n = None
pwm_right_p = None
pwm_right_n = None

pin_left_p = 16
pin_left_n = 19
pin_right_p = 20
pin_right_n = 26

target_left_freq = 0
target_right_freq = 0

target_left_amp = 0
target_right_amp = 0


def shutdown():
    pass


def init():
    global gpio_engine
    global line_left_p
    global line_left_n
    global line_right_p
    global line_right_n
    global pwm_left_p
    global pwm_left_n
    global pwm_right_p
    global pwm_right_n
    if gpio_engine is None:
        print("very fucked: there is no gpio_engine lol")
        raise OSError
    line_left_p = gpio_engine.set_output(pin_left_p, "taptic_left_p")
    line_left_n = gpio_engine.set_output(pin_left_n, "taptic_left_n")
    line_right_p = gpio_engine.set_output(pin_right_p, "taptic_right_p")
    line_right_n = gpio_engine.set_output(pin_right_n, "taptic_right_n")

    pwm_left_p = gpio_engine.create_pwm(line_left_p, 100, "taptic_left_p")
    pwm_left_n = gpio_engine.create_pwm(line_left_n, 100, "taptic_left_n")
    pwm_right_p = gpio_engine.create_pwm(line_right_p, 100, "taptic_right_p")
    pwm_right_n = gpio_engine.create_pwm(line_right_n, 100, "taptic_right_n")

    # debug
    # pwm_left_p.change_duty_rate(0.5)
    # pwm_left_n.change_duty_rate(0.2)
    # pwm_right_p.change_duty_rate(0.8)
    # pwm_right_n.change_duty_rate(0.5)
    # pwm_right_n.change_freq(1)

    pass

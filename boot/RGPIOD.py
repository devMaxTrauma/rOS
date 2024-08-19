try:
    import gpiod
except ImportError:
    raise ImportError("gpiod not found. Please install it using 'pip install gpiod'.")
try:
    import time
except ImportError:
    raise ImportError("time not found. Please install it using 'pip install time'.")
try:
    import threading
except ImportError:
    raise ImportError("threading not found. Please install it using 'pip install threading'.")

chip = gpiod.Chip("gpiochip4")

lines = []
pwms = {}


class PWM:
    line = None
    freq = 0
    duty_rate = 0.0
    name = ""
    pwm_run = True
    pwm_thread = None

    def __init__(self, line, freq, duty_rate, name):
        self.line = line
        self.freq = freq
        self.duty_rate = duty_rate
        self.name = name
        self.period = 1 / freq
        self.t_on = self.period * duty_rate
        self.t_off = self.period - self.t_on
        self.pwm_thread = threading.Thread(target=self.pwm_routine).start()

    def pwm_routine(self):
        while self.pwm_run: self.pwm_tick()

    def pwm_tick(self):
        self.line.set_value(1)
        time.sleep(self.t_on)
        self.line.set_value(0)
        time.sleep(self.t_off)

    def pwm_stop(self):
        self.pwm_run = False

    def change_duty_rate(self, duty_rate):  # 0.0 to 1.0
        self.duty_rate = duty_rate
        self.t_on = self.period * duty_rate
        self.t_off = self.period - self.t_on

    def change_freq(self, freq):  # Hz
        self.freq = freq
        self.period = 1 / freq
        self.t_on = self.period * self.duty_rate
        self.t_off = self.period - self.t_on

    def pwm_restart(self):
        self.pwm_run = False
        if self.pwm_thread is not None: self.pwm_thread.join()
        self.pwm_thread = threading.Thread(target=self.pwm_routine)
        self.pwm_thread.start()


def set_output(pin, name, original_state=False):
    line = chip.get_line(pin)
    line.request(consumer=name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[original_state])
    lines.append(line)
    return line


def set_input(pin, name):
    line = chip.get_line(pin)
    line.request(consumer=name, type=gpiod.LINE_REQ_DIR_IN)
    lines.append(line)
    return line


def output_write(line, value):
    line.set_value(value)


def input_read(line):
    return line.get_value()


def create_pwm(line, freq, name):
    pwm = PWM(line, freq, 0, name)
    pwms[name] = pwm
    return pwm


def get_pwm(name):
    return pwms[name]


def shutdown():
    for pwm in pwms.values():
        pwm.pwm_stop()
    for line in lines:
        line.release()
    chip.close()

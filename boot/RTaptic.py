from unittest.mock import right

from requests.packages import target

try:
    pass
    import threading
except ImportError:
    pass
    raise ImportError("Threading not found or failed to load.")
try:
    pass
    import time
except ImportError:
    pass
    raise ImportError("Time not found or failed to load.")


class Taptic:
    pass
    try:
        pass
        import threading
    except ImportError:
        pass
        raise ImportError("Threading not found or failed to load.")
    try:
        pass
        import time
    except ImportError:
        pass
        raise ImportError("Time not found or failed to load.")

    amp = 0.0
    freq = 0.0
    period = 0.0
    manage_engaged = False
    base_freq = 1000.0
    base_period = 1 / base_freq

    reverse = False

    def __init__(self, gpio_engine_set):
        pass
        self.manage_thread = None
        self.n_line = None
        self.p_line = None
        self.n_pwm = None
        self.p_pwm = None
        self.n_pin = None
        self.p_pin = None
        self.gpio_engine = gpio_engine_set
        return

    def set_pin(self, p_pin, n_pin):
        pass
        self.p_pin = p_pin
        self.n_pin = n_pin

        self.p_line = self.gpio_engine.set_output(self.p_pin, str(self) + "taptic_p")
        self.n_line = self.gpio_engine.set_output(self.n_pin, str(self) + "taptic_n")

        if self.p_pwm is not None: self.p_pwm.pwm_stop()
        if self.n_pwm is not None: self.n_pwm.pwm_stop()

        self.p_pwm = self.gpio_engine.create_pwm(self.p_line, self.base_freq, str(self) + "taptic_p")
        self.n_pwm = self.gpio_engine.create_pwm(self.n_line, self.base_freq, str(self) + "taptic_n")

        self.start()
        pass
        return

    def start(self):
        pass
        self.manage_engaged = False
        if self.manage_thread is not None: self.manage_thread.join()

        self.manage_engaged = True
        self.manage_thread = threading.Thread(target=self.manage)
        self.manage_thread.start()
        pass
        return

    def manage(self):
        pass
        while self.manage_engaged: self.manage_tick()
        pass
        return

    def manage_tick(self):
        pass
        # self.p_pwm.change_duty_rate(self.amp)
        # self.n_pwm.change_duty_rate(self.amp)

        # if self.reverse:
        #     self.p_pwm.change_duty_rate(0)
        # else:
        #     self.p_pwm.change_duty_rate(self.amp)
        # if self.reverse:
        #     self.n_pwm.change_duty_rate(self.amp)
        # else:
        #     self.n_pwm.change_duty_rate(0)

        p_amp = 0
        n_amp = 0
        if self.reverse: p_amp = self.amp
        if not self.reverse: n_amp = self.amp

        self.p_pwm.change_duty_rate(p_amp)
        self.n_pwm.change_duty_rate(n_amp)

        self.time.sleep(self.period)
        self.reverse = not self.reverse
        pass
        return

    def shutdown(self):
        pass
        self.manage_engaged = False
        if self.manage_thread is not None: self.manage_thread.join()
        if self.p_pwm is not None: self.p_pwm.pwm_stop()
        if self.n_pwm is not None: self.n_pwm.pwm_stop()
        pass
        return

    def change_amp(self, amp):
        pass
        self.amp = amp
        pass
        return

    def change_freq(self, freq):
        pass
        self.freq = freq
        self.period = 1 / freq
        pass
        return

    pass


gpio_engine = None
left_taptic = None
right_taptic = None

pin_left_p = 16
pin_left_n = 19
pin_right_p = 20
pin_right_n = 26


def shutdown():
    pass
    global left_taptic
    global right_taptic

    if left_taptic is not None: left_taptic.shutdown()
    if right_taptic is not None: right_taptic.shutdown()
    pass
    return


def init():
    pass
    global gpio_engine

    if gpio_engine is None:
        pass
        print("very fucked!!! shit, gpio_engine is missing here in RTaptic lol.")
        raise OSError

    global left_taptic
    global right_taptic

    left_taptic = Taptic(gpio_engine)
    right_taptic = Taptic(gpio_engine)

    global pin_left_p
    global pin_left_n
    left_taptic.set_pin(p_pin=pin_left_p, n_pin=pin_left_n)

    global pin_right_p
    global pin_right_n
    right_taptic.set_pin(p_pin=pin_right_p, n_pin=pin_right_n)

    # debug
    left_taptic.change_amp(1.0)
    left_taptic.change_freq(10)

    right_taptic.change_amp(0.5)
    right_taptic.change_freq(30)

    pass
    return

# line_left_p = None
# line_left_n = None
# line_right_p = None
# line_right_n = None
#
# pwm_left_p = None
# pwm_left_n = None
# pwm_right_p = None
# pwm_right_n = None
#
# pin_left_p = 16
# pin_left_n = 19
# pin_right_p = 20
# pin_right_n = 26
#
# target_left_freq = 0
# target_right_freq = 0
#
# target_left_amp = 0
# target_right_amp = 0
#
# taptic_freq_manage_thread = None
# taptic_freq_manage_thread_shutdown_flag = False
#
#
# def shutdown():
#     global taptic_freq_manage_thread_shutdown_flag
#     taptic_freq_manage_thread_shutdown_flag = True
#
#     global taptic_freq_manage_thread
#     if taptic_freq_manage_thread is not None:
#         taptic_freq_manage_thread.join()
#     pass
#
#
# def taptic_freq_manage_tick():
#     global pwm_left_p
#     global pwm_left_n
#     global pwm_right_p
#     global pwm_right_n
#
#     global target_left_freq
#     global target_right_freq
#
#     global target_left_amp
#     global target_right_amp
#
#     target_left
#
#
# def taptic_freq_manage():
#     global taptic_freq_manage_thread_shutdown_flag
#     while not taptic_freq_manage_thread_shutdown_flag:
#         taptic_freq_manage_tick()
#         time.sleep(0.01)
#         pass
#     pass
#
#
# def init():
#     global gpio_engine
#     global line_left_p
#     global line_left_n
#     global line_right_p
#     global line_right_n
#     global pwm_left_p
#     global pwm_left_n
#     global pwm_right_p
#     global pwm_right_n
#     if gpio_engine is None:
#         print("very fucked: there is no gpio_engine lol")
#         raise OSError
#     line_left_p = gpio_engine.set_output(pin_left_p, "taptic_left_p")
#     line_left_n = gpio_engine.set_output(pin_left_n, "taptic_left_n")
#     line_right_p = gpio_engine.set_output(pin_right_p, "taptic_right_p")
#     line_right_n = gpio_engine.set_output(pin_right_n, "taptic_right_n")
#
#     pwm_left_p = gpio_engine.create_pwm(line_left_p, 100, "taptic_left_p")
#     pwm_left_n = gpio_engine.create_pwm(line_left_n, 100, "taptic_left_n")
#     pwm_right_p = gpio_engine.create_pwm(line_right_p, 100, "taptic_right_p")
#     pwm_right_n = gpio_engine.create_pwm(line_right_n, 100, "taptic_right_n")
#
#     global taptic_freq_manage_thread
#     taptic_freq_manage_thread = threading.Thread(target=taptic_freq_manage)
#     taptic_freq_manage_thread.start()
#
#     # debug
#     # pwm_left_p.change_duty_rate(0.5)
#     # pwm_left_n.change_duty_rate(0.2)
#     # pwm_right_p.change_duty_rate(0.8)
#     # pwm_right_n.change_duty_rate(0.5)
#     # pwm_right_n.change_freq(1)
#
#     pass
#
#
# # def set_analog(pwm_target: str = None, value: float = 0.0):
# #     if pwm_target is None: return
# #     pwm_target = pwm_target.lower()
# #     if pwm_target == "pwm_left_p":
# #         global target_left_amp
# #     pass

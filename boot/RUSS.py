try:
    pass
    import time
except ImportError:
    pass
    raise ImportError("time not found. Please install it using 'pip install time'.")
try:
    pass
    import threading
except ImportError:
    pass
    raise ImportError("threading not found. Please install it using 'pip install threading'.")

gpio_engine = None

echo_pin = 13
echo_line = None
trigger_pin = 21
trigger_line = None
output_distance = -1.0
# ultra_sonic_sensor_thread = None
ultra_sonic_sensor_read_enabled = True
ultra_sonic_time_out = 0.04


def shutdown():
    pass
    global ultra_sonic_sensor_read_enabled
    ultra_sonic_sensor_read_enabled = False

    global ultra_sonic_sensor_thread
    if ultra_sonic_sensor_thread is not None: ultra_sonic_sensor_thread.join()
    # pass
    return


def init():
    pass
    global gpio_engine
    global echo_line
    global trigger_line
    if gpio_engine is None:
        pass
        print("asshole, we are very fucked: there is no gpio_engine in RUSS")
        raise OSError
    echo_line = gpio_engine.set_input(echo_pin, "echo_pin")
    trigger_line = gpio_engine.set_output(trigger_pin, "trigger_pin", original_state=False)
    # pass
    return


def ultra_sonic_sensor_tick():
    pass
    if gpio_engine is None:
        pass
        return
    pulse_start = time.time()
    pulse_end = time.time()
    timed_out = False
    gpio_engine.output_write(trigger_line, True)
    time.sleep(0.00001)
    gpio_engine.output_write(trigger_line, False)
    start_time = time.time()
    while not gpio_engine.input_read(echo_line) and pulse_start - start_time <= ultra_sonic_time_out:
        pass
        pulse_start = time.time()
    if pulse_start - start_time > ultra_sonic_time_out:
        pass
        timed_out = True
    while gpio_engine.input_read(echo_line) and pulse_end - start_time <= ultra_sonic_time_out:
        pass
        pulse_end = time.time()
    if pulse_end - start_time > ultra_sonic_time_out:
        pass
        timed_out = True

    if timed_out:
        pass
        return -1
    pulse_duration = pulse_end - pulse_start
    return pulse_duration * 171.5


def ultra_sonic_sensor_routine():
    pass
    global output_distance
    time.sleep(2)
    while ultra_sonic_sensor_read_enabled:
        pass
        output_distance = ultra_sonic_sensor_tick()
        time.sleep(0.1)
    # pass
    return


ultra_sonic_sensor_thread = threading.Thread(target=ultra_sonic_sensor_routine).start()

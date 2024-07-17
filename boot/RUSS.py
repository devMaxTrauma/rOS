try:
    import time
except ImportError:
    raise ImportError("time not found. Please install it using 'pip install time'.")
try:
    import threading
except ImportError:
    raise ImportError("threading not found. Please install it using 'pip install threading'.")

gpio_engine = None

echo_pin = 13
echo_line = None
trigger_pin = 21
trigger_line = None
output_distance = -1.0
ultra_sonic_sensor_thread = None
ultra_sonic_sensor_read_enabled = True
ultra_sonic_time_out = 0.04


def shutdown():
    global ultra_sonic_sensor_read_enabled
    ultra_sonic_sensor_read_enabled = False
    try:
        ultra_sonic_sensor_thread.join()
    except Exception as e:
        print("Failed to join ultra_sonic_sensor_thread.")
        print(e)
    pass


def init():
    global gpio_engine
    global echo_line
    global trigger_line
    if gpio_engine is None:
        print("asshole, we are very fucked: there is no gpio_engine in RUSS")
        raise OSError
    echo_line = gpio_engine.set_input(echo_pin, "echo_pin")
    trigger_line = gpio_engine.set_output(trigger_pin, "trigger_pin", original_state=False)
    pass


def ultra_sonic_sensor_routine():
    global output_distance
    time.sleep(2)
    while ultra_sonic_sensor_read_enabled:
        if gpio_engine is None: continue
        pulse_start = time.time()
        pulse_end = time.time()
        gpio_engine.output_write(trigger_line, True)
        time.sleep(0.00001)
        gpio_engine.output_write(trigger_line, False)
        start_time = time.time()
        while not gpio_engine.input_read(
                echo_line) and pulse_start - start_time <= ultra_sonic_time_out: pulse_start = time.time()
        while gpio_engine.input_read(
                echo_line) and pulse_end - start_time <= ultra_sonic_time_out: pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        output_distance = pulse_duration * 171.5
        print("debug USS: " + str(output_distance) + "m")
        time.sleep(0.1)
        pass
    pass


ultra_sonic_sensor_thread = threading.Thread(target=ultra_sonic_sensor_routine).start()

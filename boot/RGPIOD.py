try:
    import gpiod
except ImportError:
    raise ImportError("gpiod not found. Please install it using 'pip install gpiod'.")


chip = gpiod.Chip("gpiochip0")

lines = []


def set_output(pin, name, original_state=False):
    line = chip.get_line(pin)
    config = gpiod.line_request()
    config.consumer = name
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT
    line.request(config)
    line.set_value(original_state)
    lines.append(line)
    return line


def set_input(pin, name):
    line = chip.get_line(pin)
    config = gpiod.line_request()
    config.consumer = name
    config.request_type = gpiod.line_request.DIRECTION_INPUT
    line.request(config)
    lines.append(line)
    return line


def output_write(line, value):
    line.set_value(value)


def input_read(line):
    return line.get_value()


def shutdown():
    for line in lines:
        line.release()
    chip.close()

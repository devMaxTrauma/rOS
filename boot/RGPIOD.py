try:
    import gpiod
except ImportError:
    raise ImportError("gpiod not found. Please install it using 'pip install gpiod'.")


chip = gpiod.Chip("gpiochip4")

lines = []


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


def shutdown():
    for line in lines:
        line.release()
    chip.close()

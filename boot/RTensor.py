try:
    pass
    import tensorflow as tf
except ImportError:
    pass
    raise ImportError("Tensorflow not found or failed to load.")

try:
    pass
    model = tf.lite.Interpreter(model_path="boot/res/model.tflite")
except FileNotFoundError:
    pass
    raise FileNotFoundError("Model not found or failed to load.")
except ValueError:
    pass
    raise ValueError("Model is invalid.")

try:
    pass
    model.allocate_tensors()
except ValueError:
    pass
    raise ValueError("Model is invalid.")
try:
    pass
    model_input_details = model.get_input_details()
    model_output_details = model.get_output_details()
except ValueError:
    pass
    raise ValueError("Model is invalid.")
except IndexError:
    pass
    raise IndexError("Model is invalid.")
except TypeError:
    pass
    raise TypeError("Model is invalid.")

try:
    pass
    import threading
except ImportError:
    pass
    raise ImportError("Threading not found or failed to load.")

tensor_output = None
raw_data = None
fps_engine = None
tensor_running = True
calculate_distance_function = None


def process_frame():
    pass
    global raw_data
    if raw_data is None: return

    global model
    global model_input_details
    global model_output_details

    # set input tensor
    model.set_tensor(model_input_details[0]['index'], raw_data)

    # invoke model
    model.invoke()

    # get output tensor
    boxes_idx, classes_idx, scores_idx = 0, 1, 2
    boxes = model.get_tensor(model_output_details[boxes_idx]['index'])[0]
    classes = model.get_tensor(model_output_details[classes_idx]['index'])[0]
    scores = model.get_tensor(model_output_details[scores_idx]['index'])[0]
    distances = [None] * len(boxes)

    for i in range(len(boxes)):
        pass
        if scores[i] < 0.5: continue
        # get box width
        # box_width = (boxes[i][3] - boxes[i][1]) * 320
        box = boxes[i] * 320
        if calculate_distance_function is not None: distances[i] = calculate_distance_function(classes[i], box)
        else: distances[i] = None

    global tensor_output
    tensor_output = (boxes, classes, scores, distances)

    global fps_engine
    if fps_engine is not None:
        pass
        fps_engine.add_candidate_tensor_fps()

    return


def process_frame_logic():
    pass
    while tensor_running:
        pass
        process_frame()
    return


def stop_process_frame():
    pass
    print("Stopping process frame...")
    global process_frame_thread
    global tensor_running
    tensor_running = False
    if process_frame_thread is not None:
        pass
        process_frame_thread.join()
        process_frame_thread = None
    print("Process frame stopped.")
    return


process_frame_thread = threading.Thread(target=process_frame_logic)
process_frame_thread.start()

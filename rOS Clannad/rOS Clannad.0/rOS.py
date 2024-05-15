import time

from rCore import rKernel

rKernel = rKernel.Kernel()
prev_time = time.time()
max_fps = 0
fps_history = []

video = rKernel.cv.VideoCapture(0)

rKernel.cv.namedWindow("Camera", rKernel.cv.WINDOW_NORMAL)
rKernel.cv.resizeWindow("Camera", 1920, 1080)

input_details = rKernel.model.get_input_details()
output_details = rKernel.model.get_output_details()

while True:
    frame_success, frame = video.read()
    if not frame_success:
        break

    # INPUT:
    # image data: ByteBuffer sized Height x Width x 3, where Height = 320 and Width = 320 with values in [0, 255]
    # OUTPUT:
    # this model outputs to detection_boxes, detection_classes, detection_scores, num_detections. the max number of output detections are 25.
    # detection_boxed: bounding box for each detection.
    # detection_classes: class of each detection.
    # detection_scores: confidence score of each detection.
    # num_detections: total number of detections.

    # INPUT: A three-channel image of variable size - the model does NOT support batching. The input tensor is a tf.uint8 tensor with shape [1, height, width, 3] with values in [0, 255].
    # OUTPUT: The output dictionary contains:

    # num_detections: a tf.int tensor with only one value, the number of detections [N].
    # detection_boxes: a tf.float32 tensor of shape [N, 4] containing bounding box coordinates in the following order: [ymin, xmin, ymax, xmax].
    # detection_classes: a tf.int tensor of shape [N] containing detection class index from the label file.
    # detection_scores: a tf.float32 tensor of shape [N] containing detection scores.

    frame = rKernel.cv.flip(frame, 1)

    if rKernel.rKeyEngine.get_key("tensorflow enabled").value:
        copy_frame = frame.copy()
        copy_frame = rKernel.cv.resize(copy_frame, (320, 320))
        copy_frame = rKernel.cv.cvtColor(copy_frame, rKernel.cv.COLOR_BGR2RGB)

        input_data = rKernel.np.expand_dims(copy_frame, axis=0)

        rKernel.model.set_tensor(input_details[0]['index'], input_data)
        rKernel.model.invoke()

        boxes_idx, classes_idx, scores_idx = 0, 1, 2
        boxes = rKernel.model.get_tensor(output_details[boxes_idx]['index'])[0]
        classes = rKernel.model.get_tensor(output_details[classes_idx]['index'])[0]
        scores = rKernel.model.get_tensor(output_details[scores_idx]['index'])[0]

        for i in range(len(scores)):
            if scores[i] > 0.5:
                # strach detection box
                box = boxes[i] * [320, 320, 320, 320]
                # frame resoultion is 1920*1080
                # copy_frame resoultion is 320*320
                # so, we need to scale the box
                box = box * [6, 6, 6, 6]
                # draw box
                rKernel.cv.rectangle(frame, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), (0, 255, 0), 2)
                # draw text
                rKernel.cv.putText(frame, str(int(classes[i])), (int(box[1]), int(box[0])), rKernel.cv.FONT_HERSHEY_SIMPLEX,
                                   1, (0, 255, 0), 2)
    # fps
    curr_time = time.time()
    exec_time = curr_time - prev_time
    prev_time = curr_time
    fps = 1.0 / exec_time
    fps_history.append(fps)
    if len(fps_history) > 100:
        fps_history.pop(0)
    avg_fps = sum(fps_history) / len(fps_history)
    if fps > max_fps:
        max_fps = fps
    rKernel.cv.putText(frame, "FPS: " + str(int(fps)), (10, 30), rKernel.cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    rKernel.cv.putText(frame, "Max FPS: " + str(int(max_fps)), (10, 60), rKernel.cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                       2)
    rKernel.cv.putText(frame, "Avg FPS: " + str(int(avg_fps)), (10, 90), rKernel.cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                          2)

    rKernel.cv.imshow("Camera", frame)
    if rKernel.cv.waitKey(1) & 0xFF == ord('q'):
        break

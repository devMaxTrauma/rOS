import numpy as np

import RKernel

rk = RKernel.RKernel()

# resize window 360 360
rk.cv.namedWindow("ROS", rk.cv.WINDOW_NORMAL)
rk.cv.resizeWindow("ROS", 640, 480)


boot_start_time = rk.time.time()
while rk.time.time() - boot_start_time < 5:
    rk.cv.imshow("ROS", rk.splash_screen)
    rk.cv.waitKey(1)

if rk.key_engine.get_key("CameraDevice").get("value") == "macbook pro":
    camera = rk.cv.VideoCapture(0)
elif rk.key_engine.get_key("CameraDevice").get("value") == "iphone":
    camera = rk.cv.VideoCapture(1)
else:
    print("warning! Invalid camera device. Using default device.")
    camera = rk.cv.VideoCapture(0)

last_update_time = rk.time.time()
while True:
    capture_success, frame = camera.read()
    if not capture_success:
        break

    new_frame = rk.cv.resize(frame, (640, 480))

    if rk.key_engine.get_key("ROSModelActive").get("value"):
        processed_data = rk.process_frame(frame)
        # get processed data
        boxes_idx, classes_idx, scores_idx = 0, 1, 2
        outputs = rk.model.get_tensor(rk.model_output_details[0]['index'])[0]

        boxes = []
        confidences = []
        classes = []
        class_probs = []

        if rk.key_engine.get_key("ROSMindDisplayWay").get("value") == "outlined box":
            for output in outputs:
                box_confidence = output[4]
                if box_confidence <0.5:
                    continue
                class_ = output[5:].argmax(axis=0)
                class_prob = output[5:][class_]
                if class_prob < 0.5:
                    continue
                cx, cy, w, h = output[:4] * np.array([640, 480, 640, 480])
                x = round(cx - w / 2)
                y = round(cy - h / 2)
                w = round(w)
                h = round(h)

                boxes.append([x, y, w, h])
                confidences.append(float(box_confidence))
                classes.append(class_)
                class_probs.append(class_prob)

                rk.cv.rectangle(new_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # rk.cv.putText(new_frame, f"{rk.key_engine.get_key('ROSClasses').get('value')[class_]} {class_prob:.2f}", (x, y - 10), rk.cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


        elif rk.key_engine.get_key("ROSMindDisplayWay").get("value") == "filled box":
            for output in outputs:
                box_confidence = output[4]
                if box_confidence <0.5:
                    continue
                class_ = output[5:].argmax(axis=0)
                class_prob = output[5:][class_]
                if class_prob < 0.5:
                    continue
                cx, cy, w, h = output[:4] * np.array([640, 480, 640, 480])
                x = round(cx - w / 2)
                y = round(cy - h / 2)
                w = round(w)
                h = round(h)

                boxes.append([x, y, w, h])
                confidences.append(float(box_confidence))
                classes.append(class_)
                class_probs.append(class_prob)

                rk.cv.rectangle(new_frame, (x, y), (x + w, y + h), (0, 255, 0), -1)
                # rk.cv.putText(new_frame, f"{rk.key_engine.get_key('ROSClasses').get('value')[class_]} {class_prob:.2f}", (x, y - 10), rk.cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    update_time = rk.time.time()
    fps = 1 / (update_time - last_update_time)
    last_update_time = update_time

    if rk.key_engine.get_key("ROSDisplayFPSEnable").get("value"):
        rk.cv.putText(new_frame, f"FPS: {round(fps, 1)}", (10, 30), rk.cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


    rk.cv.imshow("ROS", new_frame)

    if rk.cv.waitKey(1) & 0xFF == ord('q'):
        break

rk.shutdown()

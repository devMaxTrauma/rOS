print("ROS is booting up...")
try:
    import boot.RKernel as kernel
except ImportError as ie:
    print("RKernel not found or failed to load.")
    print(ie)
    exit(11)

print("ROS booted up.")

import time

debug_start_time = time.time()

while True:
    frame = kernel.get_frame()
    kernel.raw_screen = frame
    kernel.set_tensor_input()
    kernel.render_tensor_and_etc()
    kernel.tick_screen()
    if kernel.cv.waitKey(1) & 0xFF == 27:
        break

    if time.time() - debug_start_time > 3:
        kernel.notification_engine.add_notification("hard_warning.png", "3 seconds passed.", ".")
        # kernel.notification_engine.add_notification("warning.png", "3 seconds passed1.")
        debug_start_time = time.time()

kernel.shutdown()

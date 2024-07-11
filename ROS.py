print("ROS is booting up...")
try:
    import boot.RKernel as kernel
except ImportError as ie:
    print("RKernel not found or failed to load.")
    print(ie)
    exit(11)

print("ROS booted up.")

camera = kernel.get_camera()

while True:
    frame = kernel.get_frame(camera)
    kernel.raw_screen = frame
    kernel.set_tensor_input()
    kernel.render_tensor_and_etc()
    kernel.tick_screen()
    if kernel.cv.waitKey(1) & 0xFF == 27:
        break

kernel.shutdown()

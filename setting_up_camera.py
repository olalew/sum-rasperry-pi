import arducam_mipicamera as arducam
import v4l2
import ctypes
import time

def set_controls(camera):
    try:
        camera.software_auto_exposure(enable = False)
        camera.software_auto_white_balance(enable = True)
        camera.set_control(v4l2.V4L2_CID_EXPOSURE, 10) # default 0
        camera.set_control(v4l2.V4L2_CID_FOCUS_ABSOLUTE, 10) # default 0 test values
        camera.manual_set_awb_compensation(0,0) # change value here experiment
    except Exception as e:
        print(e)

def callback(data):
    buff = arducam.buffer(data)
    file = buff.userdata
    buff.as_array.tofile(file)
    return 0

def capture_image(camera):
    frame = camera.capture(encoding='jpeg')
    fmt = camera.get_resolution()
    frame.as_array.tofile("{}x{}.jpg".format(fmt[0], fmt[1]))

def record_video(camera, duration=10):
    file = open("test.h264", "wb")
    file_obj = ctypes.py_object(file)
    camera.set_video_callback(callback, file_obj)
    time.sleep(duration)
    camera.set_video_callback(None, None)
    file.close()

if __name__ == "__main__":
    try:
        camera = arducam.mipi_camera()
        camera.init_camera()
        camera.set_resolution(640,480)
        camera.start_preview(fullscreen=False, window=(0, 0, 640,480))
        set_controls(camera)

        # Capture image and video after setting controls
        capture_image(camera)
        record_video(camera, 10)  # records for 10 seconds

        camera.stop_preview()
        camera.close_camera()
    except Exception as e:
        print(e)

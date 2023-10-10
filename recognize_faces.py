import arducam_mipicamera as arducam
import v4l2
import time
import cv2


def align_down(size, align):
    return (size & ~((align) - 1))


def align_up(size, align):
    return align_down(size + align - 1, align)


def set_controls(camera):
    try:
        camera.software_auto_exposure(enable=False)
        camera.software_auto_white_balance(enable=True)
        camera.set_control(v4l2.V4L2_CID_EXPOSURE, 0)
        camera.set_control(v4l2.V4L2_CID_FOCUS_ABSOLUTE, 0)
        camera.manual_set_awb_compensation(0, 0)
    except Exception as e:
        print(e)


# Load the face classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

# Load the replacement image and resize it to a standard face size (for simplicity)
replacement_img = cv2.imread("smiley.png")
replacement_img = cv2.resize(replacement_img, (100, 100))  # Adjust this size as per your needs

camera = arducam.mipi_camera()
camera.init_camera()
fmt = camera.set_resolution(1920, 1080)
print("Current resolution is {}".format(fmt))
set_controls(camera)

started = True
while started:
    frame = camera.capture(encoding='i420')
    height = int(align_up(fmt[1], 16))
    width = int(align_up(fmt[0], 32))
    image = frame.as_array.reshape(int(height * 1.5), width)
    image = cv2.cvtColor(image, cv2.COLOR_YUV2BGR_I420)

    image = cv2.resize(image, (640, 360))

    # Detect faces
    faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

    # For each detected face, replace that region with the replacement image
    for (x, y, w, h) in faces:
        resized_replacement = cv2.resize(replacement_img, (w, h))
        image[y:y + h, x:x + w] = resized_replacement

    cv2.imshow("Faces", image)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        started = False

camera.close_camera()

# TODO: Use better logger to file.
# TODO: Allow config file
# TODO: Allow changing camera text
# TODO: Add audio recording
# TODO: Allow changing saved files directory

import cv2
import datetime
import time

# consts
CAMERA0_ID = 0
CAMERA0_TOP_L_TEXT = "LICENSE: NMBRPLT"
CAMERA0_BOT_L_TEXT = "___CURRENT_TIME___"


def LogInfo(message: str):
    print("[INFO]   ", message)


def LogError(message: str):
    print("[ERR_]   ", message)


LogInfo("Starting CPCS...")

LogInfo("Saving time of start...")
current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime('%Y%m%d-%H%M%S')

# print local time
LogInfo("Time of start: {times}".format(times=time.ctime()))

# check how many cams are on device


def check_camera(index):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        LogInfo(f"Camera {index}: Not available")
        return False
    else:
        LogInfo(f"Camera {index}: Available")
        cap.release()
        return True


def check_all_cameras():
    LogInfo("Checking available cameras on device...")
    index = 0
    while True:
        if not check_camera(index):
            break
        index += 1


# check_all_cameras()


# print text that will be on video
LogInfo("Text on camera 0 (Top left): {text}".format(text=CAMERA0_TOP_L_TEXT))
LogInfo("Text on camera 0 (Bottom left): {text}".format(text=CAMERA0_BOT_L_TEXT))

# initiate cameras, mics any other shit we have
cv2cam0 = cv2.VideoCapture(CAMERA0_ID)

if not cv2cam0.isOpened():
    LogError("Could not open camera or video stream: Camera No: {cno}".format(cno=CAMERA0_ID))
    exit(1)

# Define the video writer properties
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('{datetimeformat}.avi'.format(datetimeformat=formatted_datetime), fourcc, 20.0, (640, 480))

LogInfo("Started recording! Time: {times}".format(times=time.ctime()))

# start program loop
while True:
    # read from camera0
    ret, frame = cv2cam0.read()

    # if frame = fucky wucky
    if not ret:
        LogError("Could not read latest frame! Time: {times}".format(times=time.ctime()))

    # add text to frames
    top_left_coord = (10, 30)  # Coordinates at the top left
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_size = cv2.getTextSize(CAMERA0_TOP_L_TEXT, font, font_scale, font_thickness)[0]
    cv2.putText(frame, CAMERA0_TOP_L_TEXT, top_left_coord, font, font_scale, (255, 255, 255), font_thickness,
                cv2.LINE_AA)

    if CAMERA0_BOT_L_TEXT == "___CURRENT_TIME___":
        bottom_left_coord = (10, frame.shape[0] - 10)  # Coordinates at the bottom left
        cv2.putText(frame, time.ctime(), bottom_left_coord, font, font_scale, (255, 255, 255), font_thickness,
                    cv2.LINE_AA)
    else:
        bottom_left_coord = (10, frame.shape[0] - 10)  # Coordinates at the bottom left
        cv2.putText(frame, CAMERA0_BOT_L_TEXT, bottom_left_coord, font, font_scale, (255, 255, 255), font_thickness,
                    cv2.LINE_AA)

    # save to file
    out.write(frame)

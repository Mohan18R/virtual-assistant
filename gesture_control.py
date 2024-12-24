import cv2
import mediapipe as mp
import numpy as np
import time
import math            
import pyautogui
from filterpy.kalman import KalmanFilter
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Initialize mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2)
mp_drawing = mp.solutions.drawing_utils

# Get screen size and initialize cursor control variables
screen_width, screen_height = pyautogui.size()
prev_x, prev_y = 0, 0

# Initialize audio utilities for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

last_volume_change = 0
last_action_time = 0

# Kalman Filter for Cursor Smoothing
kf = KalmanFilter(dim_x=4, dim_z=2)
kf.x = np.array([0., 0., 0., 0.])  # initial state (x, y, dx, dy)
kf.F = np.array([[1, 0, 1, 0],    # state transition matrix
                 [0, 1, 0, 1],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1]])
kf.H = np.array([[1, 0, 0, 0],    # measurement function
                 [0, 1, 0, 0]])
kf.P *= 1000.0                    # covariance matrix
kf.R = np.array([[10, 0], [0, 10]])  # measurement noise
kf.Q = np.eye(4) * 0.01           # process noise

# Function to draw green skeleton
def draw_green_skeleton(image, hand_landmarks):
    mp_drawing.draw_landmarks(
        image,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),  # Green Lines
        mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)  # Green Dots
    )

# Function to get hand landmarks and draw skeleton
def hand_landmarks(image):
    results = hands.process(image)
    landmark_list = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_green_skeleton(image, hand_landmarks)  # Draw green skeleton
            landmark_list.append(
                [(int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])) 
                 for landmark in hand_landmarks.landmark]
            )
    return landmark_list

# Function to get finger status (up/down)
def get_finger_status(landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    return [int(landmarks[tip_ids[0]][0] > landmarks[tip_ids[0] - 1][0])] + \
           [int(landmarks[tip_id][1] < landmarks[tip_id - 2][1]) for tip_id in tip_ids[1:]]

def perform_actions(finger_status, current_time, frame):
    global last_action_time
    action_text = ""

    if current_time - last_action_time < 0.2:  # Prevent multiple actions within a short time
        return frame

    # Detect gestures and perform actions
    if all(finger_status):  # All fingers up
        action_text = "All Fingers Up (Space Pressed)"
        pyautogui.press('space')  # Perform Space Key Press
    elif finger_status == [0, 1, 0, 0, 1]:  # 'Right' gesture
        action_text = "Right Arrow"
        pyautogui.press('right')  # Perform Right Arrow Key Press
    elif finger_status == [0, 1, 1, 0, 1]:  # 'Left' gesture
        action_text = "Left Arrow"
        pyautogui.press('left')  # Perform Left Arrow Key Press
    elif finger_status == [0, 1, 1, 1, 1]:  # 'Up' gesture
        action_text = "Up Arrow"
        pyautogui.press('up')  # Perform Up Arrow Key Press
    elif finger_status == [0, 1, 1, 1, 0]:  # 'Down' gesture
        action_text = "Down Arrow"
        pyautogui.press('down')  # Perform Down Arrow Key Press
    elif finger_status == [0, 1, 1, 0, 0]:  # 'Screenshot' gesture
        action_text = "Screenshot Taken"
        pyautogui.screenshot('screenshot.png')  # Take Screenshot

    # Display the action text on the webcam frame
    if action_text:
        cv2.putText(frame, action_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        last_action_time = current_time  # Update the last action time

    return frame


# Function for cursor control with Kalman Filter
def cursor_control(index_finger):
    global prev_x, prev_y
    x1, y1 = index_finger
    screen_x = np.interp(x1, (75, 1205), (0, screen_width))
    screen_y = np.interp(y1, (75, 645), (0, screen_height))

    # Update Kalman Filter
    kf.predict()
    kf.update([screen_x, screen_y])
    smoothed_x, smoothed_y = kf.x[0], kf.x[1]

    pyautogui.moveTo(screen_width - smoothed_x, smoothed_y)

# Main Loop
def start_gesture_control():
    cv2.namedWindow("Hand Gesture Control")
    running = True
    frame_count = 0

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB, process landmarks, and convert back to BGR
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        landmarks = hand_landmarks(frame_rgb)
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        current_time = time.time()

        if landmarks:
            # Volume control
            if len(landmarks) >= 2:
                distance = math.hypot(*(np.array(landmarks[0][20]) - np.array(landmarks[1][20])))
                if (current_time - last_volume_change) > 0.1:
                    vol = np.interp(distance, [50, 300], [minVol, maxVol])
                    volume.SetMasterVolumeLevel(vol, None)
                    last_volume_change = current_time

            # Perform gestures and cursor control
            if landmarks[0]:
                finger_status = get_finger_status(landmarks[0])
                perform_actions(finger_status, current_time,frame)

                # Cursor control (index finger up)
                if finger_status[1] == 1 and finger_status[2] == 0:
                    cursor_control(landmarks[0][8])

                # Left click for thumb
                if finger_status[1] == 0 and finger_status[0] == 1:
                    pyautogui.click()
                    time.sleep(0.2)

        # Display the updated frame
        cv2.imshow("Hand Gesture Control", frame)
        frame_count += 1

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Program terminated.")

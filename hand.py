import cv2
import mediapipe as mp
import pyautogui
import math

click  = False
new_pos = False
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.0

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

    while cap.isOpened():

        success, image = cap.read()
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape

        if results.multi_hand_landmarks:
          for hand_landmarks in results.multi_hand_landmarks:
            pointer_tip = hand_landmarks.landmark[8]
            middle_tip = hand_landmarks.landmark[12]
            thumb_tip = hand_landmarks.landmark[4]

            a = (middle_tip.x, middle_tip.y, middle_tip.z * 0)
            b = (thumb_tip.x, thumb_tip.y, thumb_tip.z * 0)
            dist = math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2) + pow(a[2] - b[2], 2))
            if dist < 0.1:
                click = True
            else:
                click = False
            index_locations.append((pointer_tip.x, pointer_tip.y))
            mp_drawing.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            new_pos = True
            target = [index_locations[-1][0] * pyautogui.size()[0], index_locations[-1][1] * pyautogui.size()[1]]
            pyautogui.move((target[0] - pyautogui.position()[0]) * 0.1, (target[1] - pyautogui.position()[1]) * 0.1)
            if click == True:
                pyautogui.mouseDown()
            else:
                pyautogui.mouseUp()
        cv2.imshow('hand', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break
cap.release()
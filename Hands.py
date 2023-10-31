import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def get_distance(hand_landmarks, index):
  """Return the Euclidean distance of the fingertip to the wrist."""
  coord_index = hand_landmarks.landmark[index]
  coord_wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
  return ((coord_index.x - coord_wrist.x)**2 \
        + (coord_index.y - coord_wrist.y)**2 \
        + (coord_index.z - coord_wrist.z)**2)**0.5


# Input from web camera
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      # Draw the detected hand landmarks onto the camera image.
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
      
        # Calculate the distance of each finger tip to the wrist.
        distances = [get_distance(hand_landmarks, tip_idx)
                     for tip_idx in [mp_hands.HandLandmark.INDEX_FINGER_TIP,
                                     mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                                     mp_hands.HandLandmark.RING_FINGER_TIP,
                                     mp_hands.HandLandmark.PINKY_TIP,
                                     mp_hands.HandLandmark.THUMB_TIP]]
        # Draw the distances as rectangles that grow as a function of the respective distance.
        # FIXME: Obviously, this is just hacked together for a demo and should be generalized.
        colors = [(128, 0, 128), (0, 220, 220), (0, 255, 0), (255, 0, 0), (200, 255, 255)]
        cv2.rectangle(image, (0, 0), (int(distances[0]*100), 20), colors[0], -1)
        cv2.rectangle(image, (0, 20), (int(distances[1]*100), 40), colors[1], -1)
        cv2.rectangle(image, (0, 40), (int(distances[2]*100), 60), colors[2], -1)
        cv2.rectangle(image, (0, 60), (int(distances[3]*100), 80), colors[3], -1)
        cv2.rectangle(image, (0, 80), (int(distances[4]*100), 100), colors[4], -1)

    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

import mediapipe as mp
import cv2
import serial

mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

ser = serial.Serial('COM3', 9600) 

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
         
            mouth_landmarks = face_landmarks.landmark[60:68]
           
            smile_score = (mouth_landmarks[3].y + mouth_landmarks[2].y - mouth_landmarks[0].y - mouth_landmarks[1].y) / 2
            
            if smile_score > 0.2:
               
                ser.write(b'1')
            else:
          
                ser.write(b'0')
    mp_drawing.draw_landmarks(frame, face_landmarks)
    cv2.imshow('Face Mesh', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

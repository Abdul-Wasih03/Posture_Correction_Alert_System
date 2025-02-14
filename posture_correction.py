import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import threading  # To play beep sound without blocking

# Initialize Mediapipe Pose Model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    """Calculate angle between three points using cosine rule"""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    ba = a - b
    bc = c - b
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(cosine_angle))
    
    return angle

# Function to play beep without stopping execution
def play_beep():
    import beepy
    threading.Thread(target=lambda: beepy.beep(sound="ping"), daemon=True).start()

# Streamlit UI
st.title("🧍‍♂️ Posture Correction Alert System ⚠️")
st.write("Monitor your posture in real-time and get alerts if you're slouching!")

# Start Webcam Button
start_webcam = st.button("Start Webcam")

if start_webcam:
    cap = cv2.VideoCapture(0)
    slouching_start = None
    slouching_threshold = 5  # Seconds before triggering alert
    slouching_alert = False  # Track if alert has been triggered

    stframe = st.empty()  # Placeholder for video feed

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect Pose
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Get key points
            ear = [landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x, 
                   landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].y]
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, 
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            # Calculate Posture Angle (Ear-Shoulder-Hip)
            posture_angle = calculate_angle(ear, shoulder, hip)

            # Set default color to green
            color = (0, 255, 0)  # Green

            # Check for slouching
            if posture_angle < 155:  # Adjusted threshold (was too high)
                color = (0, 0, 255)  # Red
                if slouching_start is None:
                    slouching_start = time.time()
                elif time.time() - slouching_start > slouching_threshold:
                    cv2.putText(frame, "Don't Lean! Sit Straight!", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
                    if not slouching_alert:
                        play_beep()  # Play beep sound in a separate thread
                        slouching_alert = True  # Prevent multiple alerts
            else:
                slouching_start = None  # Reset timer if posture is good
                slouching_alert = False  # Reset alert flag

            # Draw Pose Landmarks
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Show Posture Angle in Green or Red
            cv2.putText(frame, f"Angle: {int(posture_angle)}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

        # Convert to RGB for Streamlit display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    cap.release()

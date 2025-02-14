import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time

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

# Streamlit UI
st.title("🧍‍♂️ Posture Correction Alert System ⚠️")
st.write("Monitor your posture in real-time and get alerts if you're slouching!")

# Start Webcam Button
start_webcam = st.button("Start Webcam")

if start_webcam:
    cap = cv2.VideoCapture(0)
    slouching_start = None
    slouching_threshold = 5  # Seconds before triggering alert

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
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, 
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, 
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, 
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            # Calculate Back Angle
            back_angle = calculate_angle(shoulder, hip, knee)

            # Check for slouching
            if back_angle < 150:  # Slouching threshold
                if slouching_start is None:
                    slouching_start = time.time()
                elif time.time() - slouching_start > slouching_threshold:
                    cv2.putText(frame, "Sit Straight!", (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            else:
                slouching_start = None  # Reset timer if posture is good

            # Draw Pose Landmarks
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Show Back Angle
            cv2.putText(frame, f"Angle: {int(back_angle)}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Convert to RGB for Streamlit display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    cap.release()

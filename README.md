# Posture Correction Alert System  

This is a real-time AI-powered posture monitoring application that detects slouching using Mediapipe Pose and OpenCV. It provides immediate feedback via visual alerts and a beep sound when poor posture is detected. The app is built using Streamlit and designed for easy deployment.  

## 🚀 Features  
- 📷 Uses **webcam** to track posture in real-time.  
- 🎯 Detects **Ear-Shoulder-Hip angle** to determine slouching.  
- ✅ **Green angle**: Good posture.  
- ❌ **Red angle + Beep Sound + Warning Message**: Bad posture.  
- 🔊 Beep sound alert triggers if slouching persists for **5 seconds**.  
- 🖥️ **Streamlit-based UI** for seamless experience.  

---

## 📊 Posture Detection  
The system calculates the **angle between the Ear, Shoulder, and Hip**:  
- **Angle ≥ 175°** → **Good posture** (✅ Green)  
- **Angle < 155°** → **Bad posture** (❌ Red + Beep + "Sit Straight!")  

---

## 💂️ Project Structure  
```bash  
|-- posture_correction.py   # Main application script  
|-- requirements.txt        # Dependencies  
|-- README.md               # Project documentation  
```  

---

## 📌 Requirements  
Install the required Python libraries:  
```bash  
pip install -r requirements.txt  
```  

---

## 🏃‍♂️ How to Run Locally  
### Clone this repository:  
```bash  
git clone https://github.com/Abdul-Wasih03/Posture_Correction_Alert_System.git  
cd posture-correction  
```  

### Run the Streamlit app:  
```bash  
streamlit run posture_correction.py  
```  

---

## 🌍 Deployment  
The app is deployed on **Streamlit Community Cloud**.  
📎 **Access it here:** [Deployed Link]([https://share.streamlit.io/](https://posturecorrectionalertsystem.streamlit.app/))  

---

## 🎯 How the Model Works  
- Uses **Mediapipe Pose** to detect body landmarks.  
- Calculates **posture angle** from keypoints.  
- If angle **drops below 155°**, an **alert is triggered**.  
- Displays **real-time feedback** directly on the webcam feed.  

---


## 🔍 Acknowledgments  
- **Mediapipe** - Pose Estimation  
- **OpenCV** - Computer Vision Processing  
- **Streamlit** - Web Application Framework  

---

## 📝 License  
This project is licensed under the **MIT License**. See the LICENSE file for details.  
```


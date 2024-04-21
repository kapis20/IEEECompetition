import cv2
import numpy as np
import mediapipe as mp

#function for calculating angles
def find_angle(p1, p2, p3):
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    
    vector_a = p1 - p2
    vector_b = p3 - p2

    theta = np.arccos((np.dot(vector_a,vector_b)) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b)))
            
    degree = 180 / np.pi * theta

    return int(degree)


#set details for the visual
scale = 1.8
colours = {"mint": (137,180,62),
           "cyan": (255, 255, 0),
           "red": (33,33, 217),
           "orange": (0,102, 255),
           "white": (255,255,255),
           "teal": (200,90,56)}



#drawing utilities for visualising the poses
mp_drawing = mp.solutions.drawing_utils
#import pose estimation model (one of the solutions in media pipe)
mp_pose = mp.solutions.pose


#setting up the video feed with results displayed
#could be any camera connected to the machine. The number here represents the device. 
cap = cv2.VideoCapture(1)   

#set up a mediapipe instance. .Pose means accesing the pose estimation model
with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence=0.5) as pose: #entire line will be accesible via variable pose
    while cap.isOpened():
        ret,frame = cap.read() #ret can be ignored, frame is the image from the camera

        
        width  = int((cap.get(3))*scale) #width of webcam scaled 
        height = int((cap.get(4))*scale)  #height of webcam scaled 

        #details for message box
        m_box1 = {"start": (int(width*0.01), int(height*0.02)),
                  "end": (int(width*0.40), int(height*0.07)),
                  "text": (int(width*0.015), int(height*0.05))}
        m_box2 = {"start": (int(width*0.01), int(height*0.09)),
                  "end": (int(width*0.40), int(height*0.14)),
                  "text": (int(width*0.015), int(height*0.12))}
        

        #reclour image to make sure its in the format of rgb instead of bgr when we feed it to mediapipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        #make detection by accesing the pose model. The detection will be stored in results
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #cv2 wants bgr format
        image = cv2.resize(image, (width,height))
     

        
        #angle for knee
        try:
            landmarks = results.pose_landmarks.landmark
            hip = [landmarks[23].x, landmarks[23].y]
            knee = [landmarks[25].x, landmarks[25].y]
            ankle = [landmarks[27].x, landmarks[27].y]
            
            angle_k = find_angle(hip, knee, ankle)

            #location to print
            knee_loc = [x - 0.03 for x in knee]
            
            if (angle_k > 95):
                print(angle_k)
                cv2.rectangle(image, m_box1["start"], m_box1["end"], colours["orange"], -1)
                cv2.putText(image, str("Bend your knees more to squat deeper"), m_box1["text"], cv2.FONT_HERSHEY_SIMPLEX, 0.7, colours["white"], 1, cv2.LINE_AA)
                cv2.putText(image, str(angle_k), tuple(np.multiply(knee_loc, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, colours["red"], 2, cv2.LINE_AA)
            else:
                cv2.putText(image, str(angle_k), tuple(np.multiply(knee_loc, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, colours["mint"], 2, cv2.LINE_AA)

        except:
            pass

        #angle for back
        try:
            landmarks = results.pose_landmarks.landmark
            shoulder = [landmarks[11].x, landmarks[11].y]
            hip = [landmarks[23].x, landmarks[23].y]
            verticle = [landmarks[23].x, 0]
            
            angle_b = find_angle(shoulder, hip, verticle)

            #location to print
            hip_loc = [x - 0.03 for x in hip]

            if (angle_b < 25):
                print(angle_k)
                cv2.rectangle(image, m_box2["start"], m_box2["end"], colours["orange"], -1)
                cv2.putText(image, str("Bend your back forward more"), m_box2["text"], cv2.FONT_HERSHEY_SIMPLEX, 0.7, colours["white"], 1, cv2.LINE_AA)
                cv2.putText(image, str(angle_b), tuple(np.multiply(hip_loc, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, colours["red"], 2, cv2.LINE_AA)
            else:
                cv2.putText(image, str(angle_b), tuple(np.multiply(hip_loc, [width, height]).astype(int)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, colours["mint"], 2, cv2.LINE_AA)
            
            #print(angle)
        except:
            pass

        

        #draw the detection (landmarks and connections between them) into the image
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec (color=colours["teal"], thickness=13, circle_radius=7), #landmark
                                  mp_drawing.DrawingSpec (color=colours["white"], thickness=1, circle_radius=2)) #connection
        
        
        cv2.imshow("MediaPipe Feed", image)  #imshow gives a popup on screen and shows the image
    
        if cv2.waitKey(10) & 0xFF == ord('q'):  #feed stops when we hit q.
            break
    
    cap.release()
    cv2.destroyAllWindows()





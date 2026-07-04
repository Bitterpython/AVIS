from ultralytics import YOLO
import cv2

# ----------------------------
# Setup
# ----------------------------

model = YOLO("yolov8n.pt")

VIDEO_PATH = "C:/Programming/Vogelschreck/video1.mp4"
cap = cv2.VideoCapture(VIDEO_PATH)

BIRD_CLASS_ID = 14

CONF_THRESHOLD = 0.3

bird_counter = 0
DETECTION_THRESHOLD = 8   # wie viele Frames am Stück Vogel da sein muss

alarm_triggered = False
cooldown = 0
COOLDOWN_FRAMES = 0

# ----------------------------
# Loop
# ----------------------------

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (900, 500))

    frame_proc = cv2.GaussianBlur(frame, (3, 3), 0)

    results = model(frame_proc)[0]

    bird_detected_this_frame = False

    # ----------------------------
    # YOLO Detection
    # ----------------------------

    for box in results.boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        if cls == BIRD_CLASS_ID and conf > CONF_THRESHOLD:
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            bird_detected_this_frame = True

            # Visualisierung
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

            cv2.putText(frame,
                        f"Bird {conf:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2)

            print(f"Vogel-Mittelpunkt: {cx}, {cy}")

    if bird_detected_this_frame:
        bird_counter += 1
    else:
        bird_counter = 0

    stable_bird = bird_counter >= DETECTION_THRESHOLD

    if cooldown > 0:
        cooldown -= 1

    # ----------------------------
    # ALARM LOGIK
    # ----------------------------

    if stable_bird and cooldown == 0: #and not alarm_triggered
        alarm_triggered = True
        cooldown = COOLDOWN_FRAMES

        print("VOGEL STABIL ERKANNT -> WASSER / PIEP WÜRDE AUSLÖSEN")

    if not stable_bird:
        alarm_triggered = False

    # ----------------------------
    # Debug Anzeige
    # ----------------------------

    cv2.putText(frame,
                f"Counter: {bird_counter} | Stable: {stable_bird}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2)

    cv2.imshow("Vogel-Erkennung stabil", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
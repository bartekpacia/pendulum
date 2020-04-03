import cv2
import time
print(f"using OpenCV v{cv2.__version__}")

capture = cv2.VideoCapture("film3.mp4")

ret, frame1 = capture.read()
ret, frame2 = capture.read()

time_start = time.time()
prev_time = None
time_labels = []

prev_moving = False
while capture.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, None, iterations=1)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    cv2.putText(frame1, f"T", org=(600, 400),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color=(255, 0, 0), thickness=3)

    big_moving_things = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 2000:
            continue
        else:
            big_moving_things += 1
            cv2.rectangle(frame1, pt1=(x, y), pt2=(x + w, y + h),
                          color=(0, 255, 0), thickness=2)

    if big_moving_things > 0:
        color = (0, 255, 0)
        msg = "JEST RUCH"
        prev_moving = True
    else:
        color = (0, 0, 255)
        msg = "NIE MA RUCHU"
        if prev_moving:
            prev_time = "- -"
            time_labels.append(
                f"{round(time.time() - time_start, 2)}, diff: {prev_time}")
        prev_moving = False

    label_y = 60
    for label in time_labels:

        label_y += 30
        cv2.putText(frame1, label, org=(10, label_y),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=color, thickness=3)

    cv2.putText(frame1, msg, org=(10, 20),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                color=color, thickness=3)

    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = capture.read()

    if cv2.waitKey(40) == 27:
        break


cv2.destroyAllWindows()
capture.release()

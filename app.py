import cv2
print(f"using OpenCV v{cv2.__version__}")

capture = cv2.VideoCapture("film.mp4")

ret, frame1 = capture.read()
ret, frame2 = capture.read()

while capture.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, None, iterations=3)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame1, contours, -1, color=(0, 255, 0), thickness=2)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = capture.read()

    if cv2.waitKey(40) == 27:
        break


cv2.destroyAllWindows()
capture.release()

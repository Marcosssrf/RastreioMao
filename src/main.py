import cv2


def main():

    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Erro :(")
            break
        cv2.imshow("Webcam!", frame)
        # pressionar Q sai do loop
        # ord transforma o caractere em um int
        if cv2.waitKey(1) == ord("q"):
            break
    capture.release()
    cv2.destroyAllWindows()


main()

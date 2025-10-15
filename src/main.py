import cv2
import pyautogui
from hand_tracking import capture_hands, drawing_options


def main():

    screen_width, screen_height = pyautogui.size()
    capture = cv2.VideoCapture(0)
    x1 = y1 = x2 = y2 = 0

    while True:
        # Le a imagem e inverte e converte para RGB
        ret, frame = capture.read()
        image_height, image_width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Reconhce as maos
        output_hands = capture_hands.process(rgb_frame)
        all_hands = output_hands.multi_hand_landmarks

        # Se encontrar uma mao desenha os pontos
        if all_hands:
            for hand in all_hands:
                drawing_options.draw_landmarks(frame, hand)
                one_hand_landmarks = hand.landmark

                for id, lm in enumerate(one_hand_landmarks):
                    x = int(lm.x * image_width)
                    y = int(lm.y * image_height)
                    # print(x, y)

                    # Dedo indicador = id 8 usa para mover o mouse
                    if id == 8:
                        mouse_x = int(screen_width / image_width * x)
                        mouse_y = int(screen_height / image_height * y)
                        cv2.circle(frame, (x, y), 10, (0, 255, 255))
                        pyautogui.moveTo(mouse_x, mouse_y)
                        x1, y1 = x, y  # Guarda a posicao do indicador

                    # Dedo polegar = id 4 usa para clicar
                    if id == 4:
                        x2, y2 = x, y  # Guarda a posicao do polegar
                        cv2.circle(frame, (x, y), 10, (0, 255, 255))

                # Calcula a distancia entre o indicador e o polegar
                distance = y2 - y1
                print(distance)
                if distance < 40:
                    pyautogui.click()
                    print("clicou")
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

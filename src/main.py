import cv2
import pyautogui
from hand_tracking import capture_hands, drawing_options
import time


def main():

    screen_width, screen_height = pyautogui.size()
    capture = cv2.VideoCapture(0)

    # Coordenadas dos dedos
    # x1, y1 = Indicador (8)
    # x2, y2 = Polegar (4)
    x1 = y1 = x2 = y2 = 0

    positions_x = []
    positions_y = []
    smooth_factor = 5

    # Constantes de Tempo para Gestos
    drag_threshold_time = 0.4  # Tempo segurando para ativar o arrastar
    double_click_window = 0.4  # Tempo máximo entre o 1º soltar e o 2º clicar
    click_threshold = 40  # Distância vertical para considerar clique

    # Variáveis de Estado
    is_pinching = False  # Está atualmente pinçando?
    is_dragging = False  # Está no modo arrastar?
    pinch_start_time = 0  # Quando o pinçar começou?
    last_click_release_time = 0  # Quando o último clique foi solto?

    while True:
        # Le a imagem
        ret, frame = capture.read()
        if not ret:
            print("Erro :(")
            break

        # Inverte e converte para RGB
        image_height, image_width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Reconhce as maos
        output_hands = capture_hands.process(rgb_frame)
        all_hands = output_hands.multi_hand_landmarks

        # Reseta as coordenadas dos dedos a cada frame
        x1 = y1 = x2 = y2 = 0

        if all_hands:
            for hand in all_hands:
                drawing_options.draw_landmarks(frame, hand)
                one_hand_landmarks = hand.landmark

                for id, lm in enumerate(one_hand_landmarks):
                    x = int(lm.x * image_width)
                    y = int(lm.y * image_height)

                    if id == 8:
                        mouse_x = int(screen_width / image_width * x)
                        mouse_y = int(screen_height / image_height * y)
                        cv2.circle(frame, (x, y), 10, (0, 255, 255))

                        positions_x.append(mouse_x)
                        positions_y.append(mouse_y)

                        if len(positions_x) > smooth_factor:
                            positions_x.pop(0)
                            positions_y.pop(0)

                        if positions_x:
                            avg_x = int(sum(positions_x) / len(positions_x))
                            avg_y = int(sum(positions_y) / len(positions_y))
                            pyautogui.moveTo(avg_x, avg_y)

                        x1, y1 = x, y  # Guarda a posicao do indicador

                    if id == 4:
                        x2, y2 = x, y
                        cv2.circle(frame, (x, y), 10, (0, 255, 255))

                # Só executa se ambos os dedos foram detectados
                if y1 > 0 and y2 > 0:
                    distance = y2 - y1
                    current_time = time.time()

                    is_pinch_active_now = distance < click_threshold

                    # Usuário esta pinçando
                    if is_pinch_active_now:
                        if not is_pinching:

                            is_pinching = True
                            pinch_start_time = current_time

                            if (
                                current_time - last_click_release_time
                            ) < double_click_window:
                                pyautogui.doubleClick()
                                print("Clique Duplo")
                                last_click_release_time = (
                                    0  # Reseta o timer p/ evitar triplo clique
                                )
                                is_dragging = True  # Trava o clique para não soltar
                            else:
                                # É um clique normal
                                pyautogui.mouseDown()
                                print("Mouse Down (Iniciando clique/arraste)")
                                is_dragging = False

                        else:
                            # Usuário continua segurando o pinçar
                            if (
                                current_time - pinch_start_time
                            ) > drag_threshold_time and not is_dragging:
                                is_dragging = True  # Ativa o modo arrastar
                                print("Arrastar Ativado")

                    # Usuário não está pinçando
                    else:
                        if is_pinching:
                            is_pinching = False

                            if is_dragging:
                                # Soltou o modo arrastar
                                pyautogui.mouseUp()
                                print("Soltou o Arraste")
                            else:
                                # Foi um clique simples (segurou < drag_threshold_time)
                                pyautogui.mouseUp()
                                print("Clique Simples")
                                last_click_release_time = (
                                    current_time  # Salva a hora que soltou
                                )

        cv2.imshow("Webcam!", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    capture.release()
    cv2.destroyAllWindows()


main()

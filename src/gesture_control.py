import time


class GestureController:

    # Processa as coordenadas dos dedos e determina qual gesto está sendo feito.
    # Mantém o estado (ex: está arrastando? quando foi o último clique?).

    def __init__(self, click_threshold=40, drag_threshold_time=0.4, click_delay=0.5):
        # Constantes
        self.click_threshold = click_threshold
        self.drag_threshold_time = drag_threshold_time
        self.click_delay = click_delay

        # Variáveis de Estado
        self.is_pinching = False
        self.is_dragging = False
        self.pinch_start_time = 0
        self.last_action_time = 0

        # Coordenadas dos dedos
        self.x1 = self.y1 = 0  # Indicador (8)
        self.x2 = self.y2 = 0  # Polegar (4)
        self.x3 = self.y3 = 0  # Dedo Médio (12)

    def reset_finger_coords(self):
        # Reseta as coordenadas antes de processar um novo frame
        self.x1 = self.y1 = self.x2 = self.y2 = self.x3 = self.y3 = 0

    def update_finger_coords(self, hand_landmarks, image_width, image_height):
        # Atualiza as coordenadas dos dedos com base nos landmarks
        self.reset_finger_coords()

        for id, lm in enumerate(hand_landmarks):
            x = int(lm.x * image_width)
            y = int(lm.y * image_height)

            if id == 8:  # Indicador
                self.x1, self.y1 = x, y
            elif id == 4:  # Polegar
                self.x2, self.y2 = x, y
            elif id == 12:  # Dedo Médio
                self.x3, self.y3 = x, y

        # Retorna a posição do indicador para o main.py
        return (self.x1, self.y1)

    def process_gestures(self):

        # Analisa as coordenadas dos dedos e retorna a ação a ser executada.

        action = "NONE"  # Ação padrão

        # Só executa se os dedos principais (Indicador e Polegar) foram detectados
        if self.y1 > 0 and self.y2 > 0:

            dist_indicador = self.y2 - self.y1
            dist_medio = self.y2 - self.y3
            current_time = time.time()

            is_pinch_2_dedos = dist_indicador < self.click_threshold
            is_pinch_3_dedos = (
                is_pinch_2_dedos and self.y3 > 0 and (dist_medio < self.click_threshold)
            )

            # 1. Lógica de Clique Duplo (3 dedos)
            if is_pinch_3_dedos:
                if current_time - self.last_action_time > self.click_delay:
                    action = "DOUBLE_CLICK"
                    self.last_action_time = current_time

                # Reseta o estado do clique simples/arraste
                self.is_pinching = False
                self.is_dragging = False

            # 2. Lógica de Clique Simples / Arrastar (2 dedos)
            elif is_pinch_2_dedos:
                if not self.is_pinching:
                    # Usuário acabou de pinçar (2 dedos)
                    self.is_pinching = True
                    self.pinch_start_time = current_time
                    action = "MOUSE_DOWN"
                    self.is_dragging = False
                else:
                    # Usuário continua segurando (2 dedos)
                    if (
                        current_time - self.pinch_start_time
                    ) > self.drag_threshold_time and not self.is_dragging:
                        self.is_dragging = True
                        print("Arrastar Ativado")

            # 3. Usuário não está pinçando
            else:
                if self.is_pinching:
                    # Usuário acabou de soltar
                    self.is_pinching = False
                    action = "MOUSE_UP"

                    if self.is_dragging:
                        print("Soltou o Arraste")
                        self.is_dragging = False
                    else:
                        print("Clique Simples")

                    self.last_action_time = current_time

        return action

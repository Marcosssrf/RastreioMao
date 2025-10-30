import tkinter as tk
import threading
import cv2
import hand_tracking
from mouse_controller import MouseController
from gesture_control import GestureController
from utils import get_screen_dimensions


class HandTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Mão")
        self.root.geometry("300x150")

        self.running = False  # Flag para controlar o loop da câmera
        self.tracking_thread = None

        self.btn_start = tk.Button(
            self.root,
            text="Iniciar Controle",
            command=self.start_tracking,
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
        )
        self.btn_start.pack(pady=20, fill=tk.X, padx=30)

        self.btn_stop = tk.Button(
            self.root,
            text="Parar Controle",
            command=self.stop_tracking,
            font=("Arial", 14),
            bg="#f44336",
            fg="white",
            state="disabled",
        )
        self.btn_stop.pack(pady=10, fill=tk.X, padx=30)

        # Garante que a thread pare ao fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_tracking(self):
        # Inicia a câmera e o rastreamento em uma nova thread
        if self.running:
            return  # Já está rodando

        print("Iniciando controle...")
        self.running = True

        # Inicia a lógica da câmera em uma thread separada
        self.tracking_thread = threading.Thread(target=self.run_hand_tracking)
        self.tracking_thread.start()

        # Atualiza os botões
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")

    def stop_tracking(self):
        # Sinaliza para a thread de rastreamento parar
        print("Parando controle...")
        self.running = False  # O loop 'while self.running' na thread vai parar

    def on_tracking_stopped(self):
        # Chamado pela thread quando ela termina a limpeza.
        print("Controle finalizado.")
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")

    def on_closing(self):
        # Chamado ao fechar a janela do Tkinter
        if self.running:
            self.stop_tracking()  # Garante que a thread pare
        self.root.destroy()

    def run_hand_tracking(self):

        # Configuração Inicial
        screen_width, screen_height = get_screen_dimensions()

        try:
            capture = cv2.VideoCapture(0)
            if not capture.isOpened():
                print("Erro: Não foi possível abrir a câmera.")
                self.running = False
        except Exception as e:
            print(f"Erro ao iniciar a câmera: {e}")
            self.running = False
            self.root.after(0, self.on_tracking_stopped)
            return

        # Inicializa os controladores
        mouse = MouseController(smooth_factor=5)
        gesture = GestureController()

        # Loop Principal
        while self.running:
            ret, frame = capture.read()
            if not ret:
                print("Erro :(")
                break

            image_height, image_width, _ = frame.shape
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Processa a mão
            output_hands = hand_tracking.capture_hands.process(rgb_frame)
            all_hands = output_hands.multi_hand_landmarks

            if all_hands:
                for hand in all_hands:
                    hand_tracking.drawing_options.draw_landmarks(frame, hand)

                    indicator_x, indicator_y = gesture.update_finger_coords(
                        hand.landmark, image_width, image_height
                    )

                    if indicator_x > 0:
                        mouse_x = int(screen_width / image_width * indicator_x)
                        mouse_y = int(screen_height / image_height * indicator_y)
                        mouse.move_mouse(mouse_x, mouse_y)

                    action = gesture.process_gestures()

                    if action != "NONE":
                        mouse.perform_action(action)

            # Mostra a imagem da webcam
            cv2.imshow("Webcam!", frame)

            if cv2.waitKey(1) == 27:  # (ESC)
                break

        print("Limpando recursos...")
        capture.release()
        cv2.destroyAllWindows()
        self.root.after(0, self.on_tracking_stopped)

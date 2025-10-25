import cv2
import pyautogui
import tkinter as tk
from datetime import datetime
import threading  # NOVO: Módulo para rodar a webcam em segundo plano
# NOTE: Certifique-se de que o arquivo 'hand_tracking.py' está no mesmo diretório
from hand_tracking import capture_hands, drawing_options

# VARIÁVEL DE CONTROLE GLOBAL
running = False


# --- FUNÇÃO DE LOG ---
def log(text_widget, *args):
    """
    Inserts a simple, timestamped message into the Text widget.
    """
    # ... (A função log permanece a mesma) ...
    action_message = ' '.join(map(str, args))
    timestamp = datetime.now().strftime("[%H:%M:%S]")
    full_message = f"{timestamp}: {action_message}\n"

    text_widget.config(state="normal")
    text_widget.insert("end", full_message)
    text_widget.see("end")
    text_widget.config(state="disabled")


# --- FUNÇÃO DE ENCERRAMENTO ---
def quit_program(root_window, log_text_widget):
    """
    Função chamada pelo botão SAIR.
    """
    global running

    # 1. Sinaliza a função main() para parar
    if running:
        running = False
        log(log_text_widget, "Sinal de parada enviado. Encerrando...")

    # 2. Fecha a janela Tkinter
    root_window.destroy()


# --- FUNÇÃO PRINCIPAL (EXECUTADA EM THREAD) ---
def main():
    global running

    if running:
        log(log_text, "Aviso: O rastreamento já está em execução.")
        return

    # Inicia o rastreamento
    running = True
    log(log_text, "Iniciando captura de mão...")

    # ... (O restante da sua lógica de webcam e processamento permanece a mesma) ...
    screen_width, screen_height = pyautogui.size()
    capture = cv2.VideoCapture(0)
    x1 = y1 = x2 = y2 = 0

    if not capture.isOpened():
        log(log_text, "ERRO: Não foi possível acessar a webcam!")
        running = False
        return

    while running:
        ret, frame = capture.read()

        if not ret:
            log(log_text, "ERRO: Falha na leitura do frame.")
            break

        image_height, image_width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        output_hands = capture_hands.process(rgb_frame)
        all_hands = output_hands.multi_hand_landmarks

        if all_hands:
            for hand in all_hands:
                drawing_options.draw_landmarks(frame, hand)
                one_hand_landmarks = hand.landmark

                for id, lm in enumerate(one_hand_landmarks):
                    x = int(lm.x * image_width)
                    y = int(lm.y * image_height)

                    if id == 8:  # Dedo indicador para mover o mouse
                        mouse_x = int(screen_width / image_width * x)
                        mouse_y = int(screen_height / image_height * y)
                        cv2.circle(frame, (x, y), 10, (0, 255, 255))
                        pyautogui.moveTo(mouse_x, mouse_y)
                        x1, y1 = x, y

                    if id == 4:  # Dedo polegar para clicar
                        x2, y2 = x, y
                        cv2.circle(frame, (x, y), 10, (0, 255, 255))

                distance = y2 - y1

                if distance < 40:
                    pyautogui.click()
                    log(log_text, "AÇÃO: Clicou!")

        cv2.imshow("Webcam!", frame)

        if cv2.waitKey(1) == ord("q"):
            log(log_text, "Interrupção por 'Q'.")
            break

    # LIMPEZA APÓS O LOOP
    running = False
    capture.release()
    cv2.destroyAllWindows()
    log(log_text, "Webcam encerrada.")


# --- FUNÇÃO ENVOLTÓRIO PARA THREADING ---
def start_main_thread():
    """Cria e inicia a função main em um novo thread."""
    if not running:
        # Cria um novo thread que executará a função main()
        thread = threading.Thread(target=main)
        # Define o thread como 'daemon' para que ele seja forçado a terminar quando o programa principal fechar
        thread.daemon = True
        thread.start()
        log(log_text, "Thread de rastreamento iniciado.")
    else:
        log(log_text, "Aviso: O rastreamento já está em execução.")


# --- TKINTER SETUP ---
root = tk.Tk()
root.title("Mouse Mão")

# --- FRAME A (TOPO) - Botões ---
frame_A = tk.Frame(root, bg='lightcoral', padx=10, pady=10)
frame_A.pack(side="top", fill="x")

tk.Label(frame_A, text="Projeto Rastreio de Mão \n Este projeto permite controlar o cursor do mouse utilizando o movimento da mão capturado pela webcam." , bg='lightcoral').pack(side="top", padx=25, pady=15 )
tk.Label(frame_A, text="Controles:", bg='lightcoral').pack(side="left", padx=5)

# --- FRAME LOG (ABAIXO) ---
frame_log = tk.Frame(root)
frame_log.pack(pady=10, padx=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(frame_log)
scrollbar.pack(side="right", fill="y")

log_text = tk.Text(
    frame_log,
    wrap="word",
    yscrollcommand=scrollbar.set,
    height=15,
    width=60,
    fg="black"
)
log_text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=log_text.yview)

# --- BOTÕES ---
# O botão 'Iniciar' agora chama a função que inicia o thread
tk.Button(frame_A, text="Iniciar Mouse (Webcam)", command=start_main_thread).pack(side="left", padx=5)

# Botão de Saída
tk.Button(
    frame_A,
    text="Sair do Programa",
    command=lambda: quit_program(root, log_text),
    bg="red",
    fg="white"
).pack(side="left", padx=15)

# Mensagem de inicialização do Tkinter
log(log_text, "Interface carregada. Clique em 'Iniciar'.")

root.mainloop()
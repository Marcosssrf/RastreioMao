import pyautogui


class MouseController:

    # Controla todas as ações do mouse, incluindo a suavização de movimento

    def __init__(self, smooth_factor=5):
        self.smooth_factor = smooth_factor
        self.positions_x = []
        self.positions_y = []

    def move_mouse(self, mouse_x, mouse_y):
        # Suaviza o movimento do mouse usando média móvel e o move
        self.positions_x.append(mouse_x)
        self.positions_y.append(mouse_y)

        if len(self.positions_x) > self.smooth_factor:
            self.positions_x.pop(0)
            self.positions_y.pop(0)

        if self.positions_x:
            avg_x = int(sum(self.positions_x) / len(self.positions_x))
            avg_y = int(sum(self.positions_y) / len(self.positions_y))
            pyautogui.moveTo(avg_x, avg_y)

    def perform_action(self, action):
        # Executa uma ação de clique com base no gesto
        if action == "MOUSE_DOWN":
            pyautogui.mouseDown()
            print("Mouse Down (Iniciando clique/arraste)")
        elif action == "MOUSE_UP":
            pyautogui.mouseUp()
        elif action == "DOUBLE_CLICK":
            pyautogui.doubleClick()
            pyautogui.mouseUp()  # Garante que o clique seja solto
            print("Clique Duplo (3 dedos)")

import pyautogui


def get_screen_dimensions():
    # Retorna a largura e altura da tela
    screen_width, screen_height = pyautogui.size()
    return screen_width, screen_height

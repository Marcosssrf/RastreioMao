import tkinter as tk
from app_gui import HandTrackingApp


def main():

    # Cria a janela raiz do Tkinter e inicia a aplicação.

    root = tk.Tk()
    app = HandTrackingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

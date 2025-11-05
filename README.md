🖐️ Controle de Mão — Hand Tracking App

Este projeto permite controlar o cursor do mouse usando movimentos das mãos capturados pela webcam, com base em visão computacional e reconhecimento de gestos em tempo real. A interface foi construída com Tkinter, e o rastreamento utiliza OpenCV e MediaPipe (via módulo hand_tracking).

🔧 Funcionalidades

Captura de vídeo em tempo real via webcam. Rastreamento da mão utilizando o módulo hand_tracking. Controle do mouse conforme a posição dos dedos. Reconhecimento de gestos (clicar, arrastar, rolar, etc.) através do módulo gesture_control. Interface gráfica simples e funcional (Tkinter). Execução em thread separada, permitindo iniciar e parar o controle sem travar a interface.

🗂️ Estrutura do Projeto
```
hand_tracking_app/
│
├── hand_tracking.py         # Módulo responsável por detectar e desenhar landmarks da mão
├── gesture_control.py       # Lógica de reconhecimento de gestos e ações do mouse
├── mouse_controller.py      # Controlador de movimentos e cliques do mouse
├── utils.py                 # Funções auxiliares, como captura de dimensões da tela
├── main.py                  # Arquivo principal com a interface Tkinter e controle de execução
└── README.md
```
Pré-requisitos

Antes de executar o projeto, é necessário instalar as dependências:

pip install opencv-python mediapipe pyautogui

Como Executar

Clone o repositório:

git clone https://github.com/Marcosssrf/RastreioMao.git



Acesse a pasta do projeto:

cd hand-tracking-app


Execute o aplicativo:

python main.py

Funcionamento

Ao clicar em “Iniciar Controle”, o sistema abre a webcam e começa a rastrear a mão. A posição do dedo indicador é convertida em coordenadas na tela e usada para mover o mouse. Gestos detectados pelo GestureController são convertidos em ações do mouse, como clique ou arraste. Ao clicar em “Parar Controle”, a captura é encerrada com segurança e os recursos são liberados.

⚙️ Estrutura de Execução

O main.py cria a interface gráfica e controla o fluxo da aplicação: inicia a thread de captura e rastreamento (run_hand_tracking), monitora o estado dos botões “Iniciar” e “Parar”, e finaliza a execução liberando os recursos ao fechar a janela.

🆙 Possíveis Melhorias

Adicionar calibração automática para diferentes distâncias da câmera. Implementar um modo de configuração de gestos personalizados. Adicionar suporte a múltiplas mãos ou gestos complexos. Criar logs de uso ou estatísticas de movimento.

Licença

Este projeto é de uso livre para fins educacionais e de pesquisa. Desenvolvido para demonstrar aplicações práticas de visão computacional e interação natural com o computador.



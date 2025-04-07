import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import time

# Configurações da janela
LARGURA_JANELA = 400
ALTURA_JANELA = 600

# Configurações do pássaro
pos_x_passaro = 50
pos_y_passaro = ALTURA_JANELA // 2
velocidade_passaro = 0
GRAVIDADE = 0.5
FORCA_PULO = -10

# Configurações do cano
LARGURA_CANO = 50
ESPACO_CANO = 150
pos_x_cano = LARGURA_JANELA
altura_cano = random.randint(100, ALTURA_JANELA - ESPACO_CANO - 100)

# Estados do jogo
ESTADO_JOGANDO = "jogando"
ESTADO_PAUSADO = "pausado"
estado_jogo = ESTADO_JOGANDO

# Inicialização do GLFW e FreeGLUT
if not glfw.init():
    raise Exception("Falha ao inicializar o GLFW")

janela = glfw.create_window(LARGURA_JANELA, ALTURA_JANELA, "Flappy Donkey", None, None)

if not janela:
    glfw.terminate()
    raise Exception("Falha ao criar a janela GLFW")

glfw.make_context_current(janela)
glfw.swap_interval(1)
glutInit()

# Função para desenhar retângulos (pássaro e canos)
def desenhar_retangulo(x, y, largura, altura, cor):
    glColor3f(*cor)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + largura, y)
    glVertex2f(x + largura, y + altura)
    glVertex2f(x, y + altura)
    glEnd()

# Função para desenhar texto na tela usando FreeGLUT
def desenhar_texto(mensagem, x, y, cor):
    glColor3f(*cor)
    glRasterPos2f(x, y)
    for char in mensagem:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Define o sistema de coordenadas da janela
glOrtho(0, LARGURA_JANELA, ALTURA_JANELA, 0, -1, 1)

# Loop principal do jogo
ultimo_tempo = time.time()
em_execucao = True
while not glfw.window_should_close(janela) and em_execucao:
    glfw.poll_events()  # Processa eventos de teclado e janelas

    # Estado pausado: aguarda a tecla para reiniciar ou encerrar
    if estado_jogo == ESTADO_PAUSADO:
        glClear(GL_COLOR_BUFFER_BIT)
        desenhar_texto("Voce morreu!", 120, 250, (1, 0, 0))  # Mensagem de morte
        desenhar_texto("Tentar novamente? Espaco", 80, 300, (1, 1, 1))  # Instruções
        desenhar_texto("Para sair, pressione ESC", 80, 350, (1, 1, 1))  # Sair
        glfw.swap_buffers(janela)
        if glfw.get_key(janela, glfw.KEY_SPACE) == glfw.PRESS:  # Reinicia ao pressionar espaço
            estado_jogo = ESTADO_JOGANDO
            pos_y_passaro = ALTURA_JANELA // 2
            velocidade_passaro = 0
            pos_x_cano = LARGURA_JANELA
            altura_cano = random.randint(100, ALTURA_JANELA - ESPACO_CANO - 100)
        elif glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:  # Fecha ao pressionar ESC
            em_execucao = False
        continue  # Pula o restante do loop para aguardar interação do usuário

    # Detecta pulo do pássaro
    if glfw.get_key(janela, glfw.KEY_SPACE) == glfw.PRESS:
        velocidade_passaro = FORCA_PULO

    # Atualiza a física do jogo
    velocidade_passaro += GRAVIDADE
    pos_y_passaro += velocidade_passaro

    # Movimenta os canos e reposiciona-os quando saem da tela
    pos_x_cano -= 3
    if pos_x_cano < -LARGURA_CANO:
        pos_x_cano = LARGURA_JANELA
        altura_cano = random.randint(100, ALTURA_JANELA - ESPACO_CANO - 100)

    # Detecta colisões com canos ou com as bordas da janela
    if (pos_x_passaro + 30 > pos_x_cano and pos_x_passaro < pos_x_cano + LARGURA_CANO and
        (pos_y_passaro < altura_cano or pos_y_passaro + 30 > altura_cano + ESPACO_CANO)) or pos_y_passaro < 0 or pos_y_passaro + 30 > ALTURA_JANELA:
        estado_jogo = ESTADO_PAUSADO  # Pausa o jogo ao morrer

    # Desenha os elementos na tela
    glClear(GL_COLOR_BUFFER_BIT)
    desenhar_retangulo(pos_x_cano, 0, LARGURA_CANO, altura_cano, (0, 1, 0))  # Cano superior
    desenhar_retangulo(pos_x_cano, altura_cano + ESPACO_CANO, LARGURA_CANO, ALTURA_JANELA - (altura_cano + ESPACO_CANO), (0, 1, 0))  # Cano inferior
    desenhar_retangulo(pos_x_passaro, pos_y_passaro, 30, 30, (1, 1, 1))  # Pássaro

    glfw.swap_buffers(janela)
    time.sleep(1 / 60)  # Mantém a taxa de atualização em 60 FPS

# Finaliza o GLFW ao encerrar o jogo
glfw.terminate()

# importando pygame e outras bibliotecas e funções
import pygame
from pygame.locals import *
from sys import exit
import os
import math
import random

# localizando onde estão as spritsheets
diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagens')
diretorio_sons = os.path.join(diretorio_principal, 'sons')

#iniciando pygame
pygame.init()

#sons
som_agachar = pygame.mixer.Sound(os.path.join(diretorio_sons,'agachar.wav'))
som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons,'pulo.wav'))


#musica de fundo 
#musica_fundo = pygame.mixer.music.load(os.path.join(diretorio_sons, 'musica_fundo.mp3'))
#pygame.mixer.music.play(-1)
# Criando a tela e suas configurações

altura_tela = 692
largura_tela = 1366
dimensoes_tela = (largura_tela, altura_tela)
tela = pygame.display.set_mode(dimensoes_tela)
pygame.display.set_caption('Recin RUN!')

# Criando a sprite do jogador
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'sprite-sheet-tuba.png')).convert_alpha()

# Criando a sprite do jogador abaixando
tuba_agachando = pygame.image.load(os.path.join(diretorio_imagens, 'sprite-sheet-tuba-agachado.png')).convert_alpha()

# Criando os Coletaveis Positivos
boloderolo = pygame.image.load(os.path.join(diretorio_imagens, 'coletaveis', 'boloderolo_animacao.png'))
caldodecana = pygame.image.load(os.path.join(diretorio_imagens, 'coletaveis', 'caldodecana_animacao.png'))
cuscuz = pygame.image.load(os.path.join(diretorio_imagens, 'coletaveis', 'cuscuz_animacao.png'))

# Criando os Coletáveis Negativos
cuscuz_paulista = pygame.image.load(os.path.join(diretorio_imagens, 'coletaveis', 'cuscuzpaulista_animacao.png'))
pitu = pygame.image.load(os.path.join(diretorio_imagens, 'coletaveis', 'pitu_animacao.png'))
rocambole = pygame.image.load(os.path.join(diretorio_imagens, 'coletaveis', 'rocambole_animacao.png'))

# Criando o cenário de fundo
bg_image = pygame.image.load(os.path.join(diretorio_imagens, 'bg-cenario.png'))
bg_width = bg_image.get_width()

# Função para mostrar a quantidade de vidas na tela e definir a fonte e a cor do texto
text_font = pygame.font.SysFont("Comic Sans MS", 40)
text_color = (202, 18, 4)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    tela.blit(img, (x, y))

# Classe de Coletáveis
class Coletaveis(pygame.sprite.Sprite):

    def __init__(self, imagem):
        pygame.sprite.Sprite.__init__(self)
        self.lista = []
        for i in range(6):
            img = imagem.subsurface((i * 333, 0), (333, 333))
            img = pygame.transform.scale(img, (333 / 3, 333 / 3))
            self.lista.append(img)

        self.index = 0
        self.image = self.lista[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (600, 500)

    def update(self):
        self.index += 0.1
        if self.index >= len(self.lista):
            self.index = 0
        self.image = self.lista[int(self.index)]


class Tuba(pygame.sprite.Sprite):
    VELOC_PULO = 8.5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tuba_agachando = []
        for i in range(3):
            img1 = tuba_agachando.subsurface((i * 300, 0), (300, 300))
            self.tuba_agachando.append(img1)

        self.index_lista1 = 0
        self.image1 = self.tuba_agachando[self.index_lista1]
        self.rect1 = self.image1.get_rect()
        self.rect1.center = (500, 500)

        self.veloc_pulo = self.VELOC_PULO
        self.imagens_tuba = []
        for i in range(3):
            img = sprite_sheet.subsurface((i * 300, 0), (300, 300))
            self.imagens_tuba.append(img)

        self.index_lista = 0
        self.image = self.imagens_tuba[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (500, 500)
        self.pulo = False
        self.posicao_y_inicial = 350

        self.esta_agachado = False
    
    # metodo para quando ele está aguachado
    def agachar(self):
        self.esta_agachado = True

    # metodo de quando ele levanta
    def levantar(self):
        self.esta_agachado = False

    def pular(self):
        self.pulo = True

    def update(self):
        if self.pulo:
            self.rect.y -= self.veloc_pulo * 4
            self.veloc_pulo -= 0.8
        if self.veloc_pulo < -self.VELOC_PULO:
            self.pulo = False
            self.veloc_pulo = self.VELOC_PULO
            self.rect.y = self.posicao_y_inicial

        #lógica de animação de agachamento
        if self.esta_agachado:
            self.index_lista1 += 0.40
            if self.index_lista1 >= len(self.tuba_agachando):
                self.index_lista1 = 0
            self.image = self.tuba_agachando[int(self.index_lista1)]
        else:
            self.index_lista += 0.40
            if self.index_lista >= len(self.imagens_tuba):
                self.index_lista = 0
            self.image = self.imagens_tuba[int(self.index_lista)]


def main():
    # Looping do jogo
    sprites_player = pygame.sprite.Group()
    jogador = Tuba()
    sprites_player.add(jogador)
    bolo_de_rolo = Coletaveis(boloderolo)
    sprites_player.add(bolo_de_rolo)

    run = True
    relogio = pygame.time.Clock()
    scroll = 0
    tiles = math.ceil(largura_tela / bg_width) + 1
    n_ponte = 0
    ponte_final = 10
    vidas = 3

    while run: #loop principal
        relogio.tick(30)

        for event in pygame.event.get():  # Para fechar a janela do jogo
            if event.type == QUIT:
                run = False
                pygame.quit()
                exit()

        # Desenhando o cenário
        for i in range(0, tiles):
            tela.blit(bg_image, (i * bg_width + scroll, 0))

        # Scroll background
        scroll -= 10

        # Reset scroll
        if abs(scroll) > bg_width:
            scroll = 0
            n_ponte += 1  # Contando quantas pontes se passaram
            print(n_ponte)

        if n_ponte <= ponte_final:
            # Desenhando o personagem na tela e atualizando a animação
            sprites_player.draw(tela)
            sprites_player.update()

            # Configurando o pulo
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                jogador.pular()
                som_pulo.play()

            if keys_pressed[pygame.K_s]:
                jogador.agachar()
                som_agachar.play()

            else:
                jogador.levantar()

            # Desenhando a UI
            draw_text(str(vidas), text_font, text_color, 1120, 20)
            coracao_vidas = pygame.image.load(os.path.join(diretorio_imagens, 'coracao-vidas.png')).convert_alpha()
            tela.blit(coracao_vidas, (largura_tela - 195 * 1.2, 0))

            # Posicionando a linha de chegada
            if n_ponte == ponte_final:
                linha_chegada = pygame.image.load(os.path.join(diretorio_imagens, 'linha-chegada.png')).convert_alpha()
                tela.blit(linha_chegada, (largura_tela + scroll, 500))

        # Cutscene final
        elif n_ponte > ponte_final:
            win_img = pygame.image.load(os.path.join(diretorio_imagens, 'venceu.png'))
            tela.blit(win_img, (0, 0))

        pygame.display.flip()


main()

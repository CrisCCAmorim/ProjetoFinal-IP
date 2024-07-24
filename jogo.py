import pygame
from pygame.locals import *
from sys import exit
import os
import math

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,'imagens')
diretorio_sons = os.path.join(diretorio_principal,'sons')

pygame.init()

# criando a tela
altura_tela = 692
largura_tela = 1366
dimensoes_tela=(largura_tela,altura_tela)
tela = pygame.display.set_mode(dimensoes_tela)


pygame.display.set_caption('Eu <3 o Recife')

# Criando a sprite do jogador
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens,'sprite-sheet-tuba.png')).convert_alpha()

class Tuba(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_tuba = []
        for i in range(3):
            img = sprite_sheet.subsurface((i*300,0),(300,300))
            self.imagens_tuba.append(img)

        self.index_lista = 0
        self.image = self.imagens_tuba[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (500,500)

    def update(self):
        self.index_lista += 0.25
        if self.index_lista >2:
            self.index_lista=0
        self.image = self.imagens_tuba[int(self.index_lista)]


sprites_player = pygame.sprite.Group()
tuba = Tuba()
sprites_player.add(tuba)

# Criando o cenário de fundo
bg_image = pygame.image.load(os.path.join(diretorio_imagens,'bg-cenario.png'))
bg_width = bg_image.get_width()

# definindo variáveis do jogo
scroll = 0
tiles = math.ceil(largura_tela/bg_width) + 1
n_ponte = 0

# Relógio
relogio = pygame.time.Clock()

# looping do jogo
run = True
while run:
    relogio.tick(30)
    
    for event in pygame.event.get():        # para fechar a janela do jogo
        if event.type == QUIT:
            run = False
            pygame.quit()
            exit()
    
    # desenhando o cenário
    for i in range(0, tiles):
        tela.blit(bg_image,(i*bg_width + scroll,0))
    
    # scroll background
    scroll -= 10

    # reset scroll
    if abs(scroll) > bg_width:
        scroll = 0
        if n_ponte<5:
            n_ponte +=1     # contando quantas pontes se passaram
        print(n_ponte)

    # posicionando a linha de chagada
    if n_ponte==5:
        linha_chegada = pygame.image.load(os.path.join(diretorio_imagens,'linha-de-chegada.png')).convert_alpha()
        tela.blit(linha_chegada,(largura_tela + scroll, 500))

    # desenhando o personagem na tela e atualizando a animação
    sprites_player.draw(tela)
    sprites_player.update()


    pygame.display.flip()
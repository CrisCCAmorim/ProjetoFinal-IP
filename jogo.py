import pygame
from pygame.locals import *
from sys import exit
import os
import math

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal,'imagens')
diretorio_sons = os.path.join(diretorio_principal,'sons')

pygame.init()

# Criando a tela
altura_tela = 692
largura_tela = 1366
dimensoes_tela=(largura_tela,altura_tela)
tela = pygame.display.set_mode(dimensoes_tela)
pygame.display.set_caption('Eu <3 o Recife')

# Criando a sprite do jogador
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens,'sprite-sheet-tuba.png')).convert_alpha()

# Criando o cenário de fundo
bg_image = pygame.image.load(os.path.join(diretorio_imagens,'bg-cenario.png'))
bg_width = bg_image.get_width()

# Função para mostrar a quantidade de vidas na tela
text_font = pygame.font.SysFont("Comic Sans MS",40)
text_color = (202,18,4)
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    tela.blit(img, (x,y))


class Tuba(pygame.sprite.Sprite):
    VELOC_PULO = 8.5
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.veloc_pulo = self.VELOC_PULO
        self.imagens_tuba = []
        for i in range(3):
            img = sprite_sheet.subsurface((i*300,0),(300,300))
            self.imagens_tuba.append(img)

        self.index_lista = 0
        self.image = self.imagens_tuba[self.index_lista]
        self.rect = self.image.get_rect()
        self.rect.center = (500,500)
        self.pulo = False
        self.posicao_y_inicial = 350

    def pular(self):
        self.pulo = True

    def update(self):
        if self.pulo == True:
            self.rect.y -= self.veloc_pulo * 4
            self.veloc_pulo -= 0.8 
        if self.veloc_pulo < - self.VELOC_PULO:
            self.pulo = False
            self.veloc_pulo = self.VELOC_PULO
            self.rect.y = self.posicao_y_inicial

        self.index_lista += 0.40
        if self.index_lista >2:
            self.index_lista=0
        self.image = self.imagens_tuba[int(self.index_lista)]


def main():
    # looping do jogo
    sprites_player = pygame.sprite.Group()
    jogador = Tuba()
    sprites_player.add(jogador)
    run = True
    relogio = pygame.time.Clock()
    scroll = 0
    tiles = math.ceil(largura_tela/bg_width) + 1
    n_ponte = 0
    ponte_final=5
    vidas = 3
    
        
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
            n_ponte +=1     # contando quantas pontes se passaram
            print(n_ponte)

        if n_ponte<=ponte_final:
                # desenhando o personagem na tela e atualizando a animação
                sprites_player.draw(tela)
                sprites_player.update()

                # configurando o pulo 
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_SPACE]:
                    jogador.pular()

                # desenhando a UI
                draw_text(str(vidas),text_font,text_color,1120,20)
                coracao_vidas = pygame.image.load(os.path.join(diretorio_imagens,'coracao-vidas.png')).convert_alpha()
                tela.blit(coracao_vidas,(largura_tela-195*1.2,0))

                # posicionando a linha de chagada
                if n_ponte==ponte_final:
                    linha_chegada = pygame.image.load(os.path.join(diretorio_imagens,'linha-chegada.png')).convert_alpha()
                    tela.blit(linha_chegada,(largura_tela + scroll, 500))

        # cutscene final
        elif n_ponte>ponte_final:
            win_img = pygame.image.load(os.path.join(diretorio_imagens,'venceu.png'))
            tela.blit(win_img,(0,0))
            

        pygame.display.flip()
        
main()
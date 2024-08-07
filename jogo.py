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

#musica de fundo 
musica_fundo = pygame.mixer.music.load(os.path.join(diretorio_sons, 'musica_fundo.mp3'))
pygame.mixer.music.set_volume(0.25)
#pygame.mixer.music.play(-1)
som_vitoria = pygame.mixer.Sound(os.path.join(diretorio_sons,'success-fanfare-trumpets-6185(1).wav'))
som_derrota  = pygame.mixer.Sound(os.path.join(diretorio_sons, 'game over - sound effect.mp3'))

#Criando a tela e suas configurações
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
text_font = pygame.font.SysFont('freesansbold.ttf', 40)
text_color_life = (202, 18, 4)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    tela.blit(img, (x, y))

# Variáveis para controlar a adição de coletáveis
tempo_para_adicionar_coletaveis = 5  # Tempo em segundos para adicionar um novo coletável
tempo_ultimo_coletavel = 0  # Tempo do último coletável adicionado

# Lista para armazenar coletáveis ativos
coletaveis_ativos = pygame.sprite.Group()

# Função para gerar coletáveis aleatóriamente
def adicionar_coletavel():

    if len(coletaveis_ativos) > 2:
        return

    imagens_coletaveis = [cuscuz, cuscuz_paulista, pitu]
    tipos_coletaveis = ["cuscuz", "cuscuz_paulista", "pitu"]
    index = random.randint(0, len(imagens_coletaveis) - 1)
    imagem = imagens_coletaveis[index]
    tipo = tipos_coletaveis[index]
    novo_coletavel = Coletaveis(imagem, tipo)
    nova_posicao_x = random.randint(largura_tela, largura_tela + 200)  # Fora da tela à direita
    nova_posicao_y = random.randint(250, 500)  # Dentro dos limites da tela
    novo_coletavel.rect.topleft = (nova_posicao_x, nova_posicao_y)
    coletaveis_ativos.add(novo_coletavel)

# Classe de Coletáveis
class Coletaveis(pygame.sprite.Sprite):

    def __init__(self, imagem, tipo):
        pygame.sprite.Sprite.__init__(self)
        self.lista = []
        self.index = 0 
        self.taxa_quadros = 0.2
        self.time = 0
        self.tipo = tipo

        for i in range(6):
            img = imagem.subsurface((i * 100, 0), (100, 100))
            img = pygame.transform.scale(img, (100 * 1, 100 * 1))
            self.lista.append(img)

        self.image = self.lista[self.index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.topleft = (600, 450)

    def update(self, delta_time):
        self.time += delta_time
        if self.time >= self.taxa_quadros:
            self.time = 0
            self.index += 1
            if self.index >= len(self.lista):
                self.index = 0
            self.image = self.lista[int(self.index)]
        if self.rect.topright[0] < 0:
            self.rect.x = largura_tela
        self.rect.x -= 10

# Classe do jogador
class Tuba(pygame.sprite.Sprite):
    VELOC_PULO = 8.5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #sons e seus determinados volumes
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons,'pulo.wav'))
        self.som_pulo.set_volume(0.45)
        self.som_buff = pygame.mixer.Sound(os.path.join(diretorio_sons,'coletar.wav'))
        self.som_debuff = pygame.mixer.Sound(os.path.join(diretorio_sons, 'coleta_ruim2.wav'))
        self.som_agachar = pygame.mixer.Sound(os.path.join(diretorio_sons,'agachar.wav'))
        self.som_agachar.set_volume(1)

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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (500, 500)
        self.pulo = False
        self.posicao_y_inicial = 350

        self.esta_agachado = False
    
    # metodo para quando ele está agachado
    def agachar(self):
        self.esta_agachado = True
        self.som_agachar.stop()
        self.som_agachar.play()

    # metodo de quando ele levanta
    def levantar(self):
        self.esta_agachado = False

    def pular(self):
        self.pulo = True
        self.som_pulo.stop()
        self.som_pulo.play()

    def update(self, delta_time):
        if self.pulo:
            self.rect.y -= self.veloc_pulo * 4 
            self.veloc_pulo -= 0.5
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
    global tempo_ultimo_coletavel

    # Looping do jogo
    sprites_player = pygame.sprite.Group()
    jogador = Tuba()
    sprites_player.add(jogador)
    coletaveis_ativos.add(Coletaveis(pitu, "pitu"))
    
    # Inicialização das variáveis
    run = True
    game_over = False
    relogio = pygame.time.Clock()
    scroll = 0
    tiles = math.ceil(largura_tela / bg_width) + 1
    n_ponte = 0
    ponte_final = 10
    vidas = 3
    som_vitoria_tocado = False
    tempo_ultimo_coletavel = 0
    points = 0
    fonte = pygame.font.Font('freesansbold.ttf', 21)
    qtd_cuscuz = 0
    qtd_pitu = 0
    qtd_cuscuzpaulista = 0

    def score(tela, points): #Score na tela
        points += 1    
        text_score = fonte.render('Score: ' + str(points), True, (0, 0, 0))
        tela.blit(text_score, (15, 10))

    while run:  # loop principal
        delta_time = relogio.tick(30) / 1000.0  # tempo decorrido em segundos

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
            if not game_over:
                n_ponte += 1  # Contando quantas pontes se passaram
                print(n_ponte)

        if n_ponte <= ponte_final:
            # Desenhando o personagem na tela e atualizando a animação
            sprites_player.update(delta_time)
            sprites_player.draw(tela)
            coletaveis_ativos.update(delta_time)
            coletaveis_ativos.draw(tela)

            # Configurando o pulo
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_SPACE]:
                jogador.pular()

            if keys_pressed[pygame.K_s]:
                jogador.agachar()
            else:
                jogador.levantar()

            # adiciona um novo coletavel quando necessário
            tempo_ultimo_coletavel += delta_time
            if tempo_ultimo_coletavel >= tempo_para_adicionar_coletaveis:
                tempo_ultimo_coletavel = 0
                adicionar_coletavel()

            # Checando se houve colisões
            colisoes = pygame.sprite.spritecollide(jogador, coletaveis_ativos, True, pygame.sprite.collide_mask)
            for colisao in colisoes:
                if colisao.tipo == "cuscuz":
                    qtd_cuscuz += 1
                    jogador.som_buff.play()
                    print(f"Cuscuz coletado: {qtd_cuscuz}")
                elif colisao.tipo == "pitu":
                    qtd_pitu += 1
                    jogador.som_debuff.play()
                    print(f"Pitu coletado: {qtd_pitu}")
                elif colisao.tipo == "cuscuz_paulista":
                    qtd_cuscuzpaulista += 1
                    jogador.som_debuff.play()
                    print(f"Cuscuz Paulista coletado: {qtd_cuscuzpaulista}")

            # Desenhando a UI
            score(tela, points)  # score
            points += 1

            draw_text(str(vidas), text_font, text_color_life, 1120, 40)  # quantidade de vidas
            coracao_vidas = pygame.image.load(os.path.join(diretorio_imagens, 'coracao-vidas.png')).convert_alpha()
            tela.blit(coracao_vidas, (largura_tela - 195 * 1.2, 0))

            draw_text(str(qtd_cuscuz), text_font, (0, 0, 0), 250, 20)  # quantidade de cuscuz coletado
            cuscuz_UI = cuscuz.subsurface((100, 0), (100, 100))
            tela.blit(cuscuz_UI, (150, 0))

            draw_text(str(qtd_pitu), text_font, (0, 0, 0), 400, 20)  # quantidade de pitu coletada
            pitu_UI = pitu.subsurface((100, 0), (100, 100))
            tela.blit(pitu_UI, (300, 0))

            draw_text(str(qtd_cuscuzpaulista), text_font, (0, 0, 0), 550, 20)  # quantidade de cuscuz paulista coletado
            cuscuzpaulista_UI = cuscuz_paulista.subsurface((100, 0), (100, 100))
            tela.blit(cuscuzpaulista_UI, (450, 0))

            # Posicionando a linha de chegada
            if n_ponte == ponte_final:
                linha_chegada = pygame.image.load(os.path.join(diretorio_imagens, 'linha-chegada.png')).convert_alpha()
                tela.blit(linha_chegada, (largura_tela + scroll, 500))

            # Cutscene em caso de Game Over
            if game_over:
                game_over_img = pygame.image.load(os.path.join(diretorio_imagens, 'game-over.png'))
                tela.blit(game_over_img, (0, 0))

        # Cutscene final
        elif n_ponte > ponte_final:
            win_img = pygame.image.load(os.path.join(diretorio_imagens, 'venceu.png'))
            tela.blit(win_img, (0, 0))
            pygame.mixer.music.stop()
            if not som_vitoria_tocado:
                som_vitoria.play()
                som_vitoria_tocado = True

        pygame.display.flip()


main()

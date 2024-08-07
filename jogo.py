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
pygame.mixer.music.set_volume(0.30)
pygame.mixer.music.play(-1)
som_vitoria = pygame.mixer.Sound(os.path.join(diretorio_sons,'success-fanfare-trumpets-6185(1).wav'))
som_vitoria.set_volume(0.50)
som_derrota  = pygame.mixer.Sound(os.path.join(diretorio_sons, 'game over - sound effect.mp3'))
som_derrota.set_volume(0.50)

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
cuscuz = pygame.image.load(os.path.join(diretorio_imagens, 'coletaveis', 'cuscuz_animacao.png'))

# Criando os Coletáveis Negativos
cuscuz_paulista = pygame.image.load(os.path.join(diretorio_imagens, 'coletaveis', 'cuscuzpaulista_animacao.png'))
pitu = pygame.image.load(os.path.join(diretorio_imagens, 'coletaveis', 'pitu_animacao.png'))

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

contadores_coletaveis = {"cuscuz": 0, "cuscuz_paulista": 0, "pitu": 0}
min_aparicoes = 2

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
        self.rect.topleft = (600, 450)  # Posição inicial

    def update(self, delta_time):
        self.time += delta_time
        if self.time >= self.taxa_quadros:
            self.time = 0
            self.index += 1
            if self.index >= len(self.lista):
                self.index = 0
            self.image = self.lista[int(self.index)]
        
        # Mover o coletável para a esquerda
        self.rect.x -= 10
        
        # Se o coletável saiu da tela, reinicie a posição
        if self.rect.right < 0:
            self.kill()  # Remove o coletável do grupo


primeiro_coletavel_adicionado = False


def adicionar_coletavel():
    global primeiro_coletavel_adicionado

    if len(coletaveis_ativos) > 2:
        return 

    imagens_coletaveis = [cuscuz, cuscuz_paulista, pitu]
    tipos_coletaveis = ["cuscuz", "cuscuz_paulista", "pitu"]

    # Filtrando os tipos que ainda não atingiram o mínimo de aparições
    tipos_disponiveis = [tipo for tipo in tipos_coletaveis if contadores_coletaveis[tipo] < min_aparicoes]
    if not tipos_disponiveis:
        # Se todos os tipos já atingiram o mínimo, permitimos todos
        tipos_disponiveis = tipos_coletaveis

    index = random.randint(0, len(tipos_disponiveis) - 1)
    tipo = tipos_disponiveis[index]
    imagem = imagens_coletaveis[tipos_coletaveis.index(tipo)]
    novo_coletavel = Coletaveis(imagem, tipo)
    
    # Definindo uma faixa de altura acessível para os coletáveis
    altura_minima = 249 # Ajuste conforme a altura mínima que o jogador pode alcançar
    altura_maxima = 500  # Ajuste conforme a altura máxima que o jogador pode alcançar
    
    nova_posicao_x = random.randint(largura_tela, largura_tela + 200)  # Fora da tela à direita
    nova_posicao_y = random.randint(altura_minima, altura_maxima)  # Dentro dos limites de altura acessível

    # Garantir que o primeiro coletável não apareça muito perto do jogador
    if not primeiro_coletavel_adicionado:
        while nova_posicao_x < 600 + 300 and nova_posicao_x > 500:  # Ajuste 500 + 300 conforme o tamanho do jogador
            nova_posicao_x = random.randint(largura_tela, largura_tela + 200)

    
    novo_coletavel.rect.topleft = (nova_posicao_x, nova_posicao_y)
    coletaveis_ativos.add(novo_coletavel)

    # Incrementa o contador do tipo de coletável adicionado
    contadores_coletaveis[tipo] += 1
    primeiro_coletavel_adicionado = True



# Classe do jogador
class Tuba(pygame.sprite.Sprite):
    VELOC_PULO = 8.5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #sons e seus determinados volumes
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons,'pulo.wav'))
        self.som_pulo.set_volume(0.45)
        self.som_buff = pygame.mixer.Sound(os.path.join(diretorio_sons,'coleta2.wav'))
        self.som_buff.set_volume(0.28)
        self.som_debuff = pygame.mixer.Sound(os.path.join(diretorio_sons, 'coleta_ruim2.wav'))
        self.som_debuff.set_volume(0.28)
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
    global tempo_ultimo_coletavel, primeiro_coletavel_adicionado

    # Looping do jogo
    sprites_player = pygame.sprite.Group()
    jogador = Tuba()
    sprites_player.add(jogador)

    # Adiciona um primeiro coletável longe do jogador
    primeiro_coletavel_adicionado = False
    adicionar_coletavel()  # Garante que o primeiro coletável não esteja muito perto    

    # Inicialização das variáveis
    run = True
    game_over = False
    relogio = pygame.time.Clock()
    scroll = 0
    tiles = math.ceil(largura_tela / bg_width) + 1
    n_ponte = 0
    ponte_final = 90
    vidas = 3
    som_vitoria_tocado = False
    som_derrota_tocado = False
    tempo_ultimo_coletavel = 0
    points = 0
    fonte = pygame.font.Font('freesansbold.ttf', 21)
    qtd_cuscuz = 0
    qtd_pitu = 0
    qtd_cuscuzpaulista = 0
    buff_ativo = False
    debuff_ativo = False
    tempo_ativo = 0

    def score(tela, points): #Score na tela
        if debuff_ativo:
            points += 0
        if buff_ativo:
            points += 2
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
        if buff_ativo:
            debuff_ativo = False
            scroll -= 20
            tempo_ativo += 1
            if tempo_ativo >= 100:
                buff_ativo = False
                tempo_ativo = 0
        else:
            scroll -= 10

        if debuff_ativo:
            buff_ativo = False
            scroll -= 1
            tempo_ativo += 1
            if tempo_ativo >= 100:
                debuff_ativo = False
                tempo_ativo = 0
        else:
            scroll -= 10

        # Reset scroll
        if abs(scroll) > bg_width:
            scroll = 0
            if not game_over:
                n_ponte += 1  # Contando quantas pontes se passaram
                print(f'Numero da ponte: {n_ponte}')

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
                    buff_ativo = True
                    print(f"Cuscuz coletado: {qtd_cuscuz}")
                elif colisao.tipo == "pitu":
                    qtd_pitu += 1
                    jogador.som_debuff.play()
                    debuff_ativo = True
                    print(f"Pitu coletado: {qtd_pitu}")
                elif colisao.tipo == "cuscuz_paulista":
                    qtd_cuscuzpaulista += 1
                    vidas -= 1
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
            if vidas <= 0:
                game_over=True
            

        # Cutscene vitória
        elif n_ponte > ponte_final:
            win_img = pygame.image.load(os.path.join(diretorio_imagens, 'venceu.png'))
            tela.blit(win_img, (0, 0))
            pygame.mixer.music.stop()
            if not som_vitoria_tocado:
                som_vitoria.play()
                som_vitoria_tocado = True

        if game_over:
            game_over_img = pygame.image.load(os.path.join(diretorio_imagens, 'game-over.png'))
            tela.blit(game_over_img, (0, 0))
            pygame.mixer.music.stop()
            if not som_derrota_tocado:
                som_derrota.play()
                som_derrota_tocado = True



        pygame.display.flip()


main()
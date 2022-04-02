import pygame
import os
import random
import neat

ai_jogando =  True
geracao = 0

TELA_LARGURA = 800
TELA_ALTURA = 800

pygame.display.init()
pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))

IMAGENS_NUVEM = [
    pygame.transform.rotozoom(pygame.image.load(os.path.join('imgs', 'nuvem1.png')).convert_alpha(), 0, 0.5),
    pygame.transform.rotozoom(pygame.image.load(os.path.join('imgs', 'nuvem2.png')).convert_alpha(), 0, 0.5),
    pygame.transform.rotozoom(pygame.image.load(os.path.join('imgs', 'nuvem3.png')).convert_alpha(), 0, 0.5),
]
IMAGENS_DASH = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'dash1.png')).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'dash2.png')).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'dash3.png')).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'dash4.png')).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'dash5.png')).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'dash6.png')).convert_alpha()),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'dash7.png')).convert_alpha()),
]

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')).convert_alpha())
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')).convert())
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')).convert())
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

#Sons
pygame.mixer.init()
sfx_pulo = pygame.mixer.Sound(os.path.join('snds', 'sfx_wing.wav'))
sfx_point = pygame.mixer.Sound(os.path.join('snds', 'sfx_point.wav'))
sfx_hit = pygame.mixer.Sound(os.path.join('snds', 'sfx_hit.wav'))
sfx_fart = pygame.mixer.Sound(os.path.join('snds', 'fart.mp3'))

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)


class Passaro:
    IMGS = IMAGENS_PASSARO
    IMGS_DASH = IMAGENS_DASH

    # animações da rotação
    ROTACAO_MAXIMA = 20
    VELOCIDADE_ROTACAO = 10
    TEMPO_ANIMACAO = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.contagem_dash = 0
        self.imagem = self.IMGS[1]
        self.dash = 1
        self.dash_power = 0
        self.imagem_dash = self.IMGS[0]
        self.dash_time = 200
        self.cor_original = (200, 183, 51) # NAO ALTERAR
        self.cor_nova = (100, 0, 0)
        cor1 = pygame.PixelArray(self.IMGS[0])
        cor2 = pygame.PixelArray(self.IMGS[1])
        cor3 = pygame.PixelArray(self.IMGS[2])
        cor1.replace(self.cor_original, self.cor_nova)
        cor2.replace(self.cor_original, self.cor_nova)
        cor3.replace(self.cor_original, self.cor_nova)


    def pular(self):
        self.velocidade = -6
        self.tempo = 0
        self.altura = self.y
        sfx_pulo.play()

    def dasher(self):
        if self.dash_time >= 200:
            if ai_jogando:
                self.dash_power = 100
            else:
                self.dash_power = 50
            self.dash = 0.2
            self.dash_time = 0
            self.contagem_dash = 0
            sfx_fart.play()

    def mover(self):
    # calcular o deslocamento
        self.tempo += 0.5
        deslocamento = self.velocidade * self.tempo + 1 * (self.tempo**2)
    # dash
        if self.dash_time < 200:
            self.dash_time += 1

        if self.dash_power >= 0:
            self.angulo = 0
            self.dash_power -= 1
        else:
            self.dash = 1


        # restringir o deslocamento
        if deslocamento > 12:
            deslocamento = 12
        elif deslocamento < 0:
            deslocamento -= 2.5
        if self.dash == 1:
            self.y += deslocamento

    # angulo do passaro
        if deslocamento < 0 or self.y < (self.altura - 1000):
            if self.angulo < self.ROTACAO_MAXIMA and self.dash_power <= 0:
                self.angulo = self.ROTACAO_MAXIMA

        else:
            if self.angulo > -5 and self.dash_power <= 0:
                self.angulo -= self.VELOCIDADE_ROTACAO


    def desenhar(self, tela):
        # definir a imagem
        self.contagem_imagem += 1
        if self.contagem_imagem < self.TEMPO_ANIMACAO*1*self.dash:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2*self.dash:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3*self.dash:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4*self.dash:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4*self.dash + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        #definir dash
        self.contagem_dash += 1
        if self.contagem_dash < self.TEMPO_ANIMACAO *   1*4:
            self.imagem_dash = self.IMGS_DASH[0]
        elif self.contagem_dash < self.TEMPO_ANIMACAO * 2*4:
            self.imagem_dash = self.IMGS_DASH[1]
        elif self.contagem_dash < self.TEMPO_ANIMACAO * 3*4:
            self.imagem_dash = self.IMGS_DASH[2]
        elif self.contagem_dash < self.TEMPO_ANIMACAO * 4*4:
            self.imagem_dash = self.IMGS_DASH[3]
        elif self.contagem_dash < self.TEMPO_ANIMACAO * 5*4:
            self.imagem_dash = self.IMGS_DASH[4]
        elif self.contagem_dash < self.TEMPO_ANIMACAO * 6*4:
            self.imagem_dash = self.IMGS_DASH[5]
        elif self.contagem_dash < self.TEMPO_ANIMACAO * 7*4:
            self.imagem_dash = self.IMGS_DASH[6]


        # não bater a asa
        if self.angulo < 0:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

        #desenhar dash
        #self.imagem_dash.set_alpha(50)
        pos_centro_imagem_dash = self.imagem_dash.get_rect(topleft=(self.x - 20 - self.contagem_dash*2, self.y + 20)).center
        retangulo_dash = self.imagem_dash.get_rect(center=pos_centro_imagem_dash)
        if self.dash_power >= 0:
            tela.blit(self.imagem_dash, retangulo_dash.topleft)



    def get_mask(self):
       return pygame.mask.from_surface(self.imagem)


class Cano:

    VELOCIDADE = 4


    def __init__(self, x, altura, passou, distancia):
        self.x = x
        self.altura = altura
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = passou
        self.distancia = distancia
        self.definir_altura()
        self.dash = 1
        self.dash_time = 30



    def definir_altura(self):

        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.distancia

    def dasher(self):
        if self.dash_time >= 30:
            self.dash = 4
            self.dash_time = 0

    def mover(self):
        self.x -= self.VELOCIDADE*self.dash
    # dash
        if self.dash_time < 30:
            self.dash_time += 1
            if self.dash > 1:
                self.dash -= 0.1
        else:
            self.dash = 1

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 6
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA
        self.x3 = 2*self.LARGURA
        self.dash = 1
        self.dash_time = 30

    def dasher(self):
        if self.dash_time >= 30:
            self.dash = 4
            self.dash_time = 0

    def mover(self):
        self.x1 -= self.VELOCIDADE*self.dash
        self.x2 -= self.VELOCIDADE*self.dash
        self.x3 -= self.VELOCIDADE*self.dash

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x3 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA
        if self.x3 + self.LARGURA < 0:
            self.x3 = self.x2 + self.LARGURA
    # dash
        if self.dash_time < 30:
            self.dash_time += 1
            if self.dash > 1:
                self.dash -= 0.1
        else:
            self.dash = 1

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))
        tela.blit(self.IMAGEM, (self.x3, self.y))

class Background:

    VELOCIDADE = 0.5
    LARGURA = IMAGEM_BACKGROUND.get_width()
    IMAGEM = IMAGEM_BACKGROUND


    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA
        self.x3 = 2 * self.LARGURA
        self.dash = 1
        self.dash_time = 30

    def dasher(self):
        if self.dash_time >= 30:
            self.dash = 4
            self.dash_time = 0

    def mover(self):
        self.x1 -= self.VELOCIDADE*self.dash
        self.x2 -= self.VELOCIDADE*self.dash
        self.x3 -= self.VELOCIDADE*self.dash

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x3 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA
        if self.x3 + self.LARGURA < 0:
            self.x3 = self.x2 + self.LARGURA

    # dash
        if self.dash_time < 30:
            self.dash_time += 1
            if self.dash > 1:
                self.dash -= 0.1
        else:
            self.dash = 1

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))
        tela.blit(self.IMAGEM, (self.x3, self.y))

class Nuvem:

    VELOCIDADE = 1.5
    IMGS = IMAGENS_NUVEM
    LARGURA = 1000


    def __init__(self, x, y):
        self.y = y
        self.x1 = random.randrange(500, 2500)
        self.n = random.randrange(1, 3)
        self.imagem = self.IMGS[random.randrange(1, 3)]
        self.dash = 1
        self.dash_time = 30
        self.n = random.randrange(0, 20)/10

    def dasher(self):
        if self.dash_time >= 30:
            self.dash = 4
            self.dash_time = 0

    def mover(self):
        self.x1 -= self.VELOCIDADE*self.dash+ self.n
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.LARGURA + 800
            self.y = random.randrange(0, 200)
            self.n = random.randrange(1, 4)
            if self.n == 1:
                self.imagem = self.IMGS[0]
            elif self.n == 2:
                self.imagem = self.IMGS[1]
            elif self.n == 3:
                self.imagem = self.IMGS[2]
        self.imagem.set_alpha(240)
    # dash
        if self.dash_time < 30:
            self.dash_time += 1
            if self.dash > 1:
                self.dash -= 0.1
        else:
            self.dash = 1

    def desenhar(self, tela):

        tela.blit(self.imagem, (self.x1, self.y))




def desenhar_tela(tela, background, passaros, canos, chao, pontos, nuvem1, nuvem2):
    background.desenhar(tela)
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
    texto = FONTE_PONTOS.render(f"{pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))

    if ai_jogando:
        texto = FONTE_PONTOS.render(f"G: {geracao}--{len(passaros)}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    chao.desenhar(tela)
    nuvem1.desenhar(tela)
    nuvem2.desenhar(tela)
    pygame.display.update()


def main(genomas, config): #fitness function
    global geracao
    geracao += 1

    if ai_jogando:
        redes = []
        lista_genomas = []
        passaros = []
        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(300, 350))
    else:

        passaros = [Passaro(300, 350)]
    chao = Chao(730)

    nuvem1 = Nuvem(100, 200)
    nuvem2 = Nuvem(1000, 100)
    background = Background(0)
    canos = [Cano(800, 400, False, 200)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(60)

        # interação
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if not ai_jogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()
                    if evento.key == pygame.K_LCTRL and passaro.dash_time >= 200:
                        for passaro in passaros:
                            passaro.dasher()
                        chao.dasher()
                        background.dasher()
                        nuvem1.dasher()
                        nuvem2.dasher()
                        passaro.dash_time = 0
                        for cano in canos:
                            cano.dasher()

        indice_cano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indice_cano = 1
        else:
            rodando = False
            break


        # mover as coisas
        for i, passaro in enumerate(passaros):
            passaro.mover()
            # aumentar a fitness
            if ai_jogando:
                lista_genomas[i].fitness += 0.1

                output = redes[i].activate((passaro.y,
                                            abs(passaro.y - canos[indice_cano].altura),
                                            abs(passaro.y - canos[indice_cano].pos_base),
                                            abs(passaro.x - canos[indice_cano].x)))

                #-1 e 1 -> se o output for > 0.5 então o passaro pula
                if output[0] > 0:
                 passaro.pular()

                if output[1] > 0:
                 passaro.dasher()

        chao.mover()
        background.mover()
        nuvem1.mover()
        nuvem2.mover()


        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    sfx_hit.play()
                    if ai_jogando:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x + cano.CANO_TOPO.get_width():
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)


        if adicionar_cano:
            pontos += 1
            sfx_point.play()
            cano.altura = random.randrange(50, 500)
            if pontos <= 40:
                distancia = random.randrange(100, 500 - pontos*10)
            elif pontos > 40:
                distancia = 100
            n = random.randrange(1, 4)
            if n == 3:
                if distancia < 200:
                    distancia = 200
                canos.append(Cano(850, cano.altura, True, distancia))
                canos.append(Cano(850 + cano.CANO_TOPO.get_width(), cano.altura, True, distancia))
                canos.append(Cano(850 + cano.CANO_TOPO.get_width() * 2, cano.altura, False, distancia))
            elif n == 2:
                if distancia < 100:
                    distancia = 100
                canos.append(Cano(850+cano.CANO_TOPO.get_width(), cano.altura, True, distancia))
                canos.append(Cano(850 + cano.CANO_TOPO.get_width() * 2, cano.altura, False, distancia))
            elif n == 1:
                if distancia < 100:
                    distancia = 100
                canos.append(Cano(850+cano.CANO_TOPO.get_width()*2, cano.altura, False, distancia))
            if ai_jogando:
                for genoma in lista_genomas:
                    genoma.fitness += 5
        for cano in remover_canos:
            canos.remove(cano)


        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                if ai_jogando:
                    genoma.fitness -= 0.1
                    lista_genomas.pop(i)
                    redes.pop(i)

        desenhar_tela(tela, background, passaros, canos, chao, pontos, nuvem1, nuvem2)

def rodar(caminho_config):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminho_config)
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())


    if ai_jogando:
        populacao.run(main, 50)
    else:
        main(None, None)


if __name__ == '__main__':
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, 'config.txt')
    rodar(caminho_config)
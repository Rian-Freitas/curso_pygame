import pygame
import os
from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE,
                           K_SPACE,
                           K_UP,
                           K_DOWN
                           )
from fundo import Fundo
from elementos import ElementoSprite
import random

nivel = 1

class Jogo:
    def __init__(self, size=(600, 600), fullscreen=False):
        self.elementos = {}
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.fundo = Fundo()
        self.jogador = None
        # self.musica = musica
        self.interval = 0
        self.nivel = 0

        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN

        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('The Corona Shooter')
        self.run = True


    def manutenção(self):
        r = random.randint(0, 100)
        x = random.randint(1, self.screen_size[0])
        if r > (40 * len(self.elementos["virii"])):
            enemy = Virus([0, 0])
            size = enemy.get_size()
            enemy.set_pos([x, 0])
            self.elementos["virii"].add(enemy)

    def muda_nivel(self):
        xp = self.jogador.get_pontos()
        if xp > 10 and self.level == 0:
            self.fundo = Fundo("tile2")
            self.nivel = 1
            self.jogador.set_lives(self.jogador.get_lives() + 3)
        elif xp > 50 and self.level == 1:
            self.fundo = Fundo("tile2")
            self.nivel = 2
            self.jogador.set_lives(self.player.get_lives() + 6)
            
    def troca_musica_fundo(self):
        
        musica = "Fase1.wav"
        musica = os.path.join("sons", musica)
        musica = pygame.mixer.music.load(musica)
        
        if self.nivel == 0:  
            pygame.mixer.init()
            musica = "Fase 1.wav"
            pygame.mixer.music.play(-1)
        elif self.nivel == 1:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
                        
            pygame.mixer.init()
            musica = "Fase 2.wav"
            pygame.mixer.music.play(-1)
        elif self.nivel == 2:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            
            pygame.mixer.init()
            musica = "Fase 3.wav"
            pygame.mixer.music.play(-1)

    def atualiza_elementos(self, dt):
        self.fundo.update(dt)

    def desenha_elementos(self):
        self.fundo.draw(self.screen)
        self.nave.draw(self.screen)
        
        if nivel>0:
            for el in self.elementos['virii']:
                el.draw(self.screen)
        if nivel>1: 
            for el in self.elementos['virii2']:
                el.draw(self.screen)
        if nivel>2:
            for el in self.elementos['virii3']:
                el.draw(self.screen)  

    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False

        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            if key == K_ESCAPE:
                self.run = False
        # ESPAÇO ATIRA
            if key == K_SPACE:
                self.interval = 0
                self.jogador.atira(self.elementos["tiros"])
        #comandos movimento teclas
            if key == K_LEFT:
                self.run.vel_left
            if key == K_RIGHT:
                self.run.vel_right
            if key == K_UP:
                self.run.vel_up
            if key == K_DOWN:
                self.run.vel_down
                

    def loop(self):
        clock = pygame.time.Clock()
        if nivel > 0:
            dt = 4
        else:
            dt = 16
        # desenhar o virus na tela
        #self.elementos['virii'] = [pygame.sprite.RenderPlain(Virus([120, 50]))]
        #self.elementos['virii2'] = [pygame.sprite.RenderPlain(Virus2([500, 70]))]
        #self.elementos['virii3'] = [pygame.sprite.RenderPlain(Virus3([300, 300]))]
        
        # implementar logica de nivel 
           
        if nivel == 1: 
            self.elementos['virii'] = [pygame.sprite.RenderPlain(Virus([120, 50]))]
            pygame.mixer.music.load("Nivel 1.wav")
        if nivel == 2: 
            self.elementos['virii'] = [pygame.sprite.RenderPlain(Virus([120, 50]))]
            self.elementos['virii2'] = [pygame.sprite.RenderPlain(Virus2([500, 70]))]
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Nivel 2.wav")
        if nivel == 3:
            self.elementos['virii'] = [pygame.sprite.RenderPlain(Virus([120, 50]))]
            self.elementos['virii2'] = [pygame.sprite.RenderPlain(Virus2([500, 70]))]
            self.elementos['virii3'] = [pygame.sprite.RenderPlain(Virus3([300, 300]))]
            pygame.mixer.music.stop()
            pygame.mixer.music.load("Nivel 3.wav")

        self.nave = pygame.sprite.RenderPlain(Nave([200, 400], 5))
        while self.run:
            clock.tick(1000 / dt)

            self.trata_eventos()
            self.ação_elemento()
            self.troca_musica_fundo()
            self.manutenção()

            # Atualiza Elementos
            self.atualiza_elementos(dt)

            # Desenhe no back buffer
            self.desenha_elementos()
            pygame.display.flip()

class Nave(ElementoSprite):
    def __init__(self, position, lives=0, speed=[0, 0], image=None, new_size=[83, 248]):
        self.acceleration = [3, 3]
        if not image:
            image = "seringa.png"
        super().__init__(image, position, speed, new_size)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives
        
        #ATIRAR
    def atira(self, lista_de_tiros, image=None):
        s = list(self.get_speed())
        s[1] *= 2
        Tiro(self.get_pos(), s, image, lista_de_tiros)
        pygame.mixer.Sound("Atirar.wav")

#defini o virus 1 com 1 vida
class Virus(Nave):
    def __init__(self, position, lives=1, speed=None, image=None, size=(100, 100)):
        if not image:
            image = "virus1.png"
        super().__init__(position, lives, speed, image, size)
        
#defini o virus 2 com 2 vidas
class Virus2(Nave):
    def __init__(self, position, lives=2, speed=None, image=None, size=(100, 100)):
        if not image:
            image = "virus2.png"
        super().__init__(position, lives, speed, image, size)
        
#defini o virus 3 com 3 vidas
class Virus3(Nave):
    def __init__(self, position, lives=3, speed=None, image=None, size=(100, 100)):
        if not image:
            image = "virus3.png"
        super().__init__(position, lives, speed, image, size)
        
class Jogador(Nave):
 
    def __init__(self, position, lives=10, image=None, new_size=[83, 248]):
    
class Tiro(ElementoSprite):
    def __init__(self, position, speed=None, image=None, list=None):
        if not image:
            image = "tiro.png"
        super().__init__(image, position, speed)
        if list is not None:
            self.add(list)
            
class Player(Nave):
    def __init__(self, position, lives=5, image=None, new_size=[83, 248]):
        if not image:
            image = "seringa.png"
        super().__init__(position, lives, [0, 0], image, new_size)
        self.pontos = 0

    def atualiza(self, dt):
        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

    def get_pos(self):
        return (self.rect.center[0], self.rect.top)
    
    
    @property
    def morto(self):
        return self.get_lives() == 0

    def vel_up(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] - self.acceleration[1]))

    def vel_down(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] + self.acceleration[1]))

class Tiro(ElementoSprite):
    def __init__(self, position, speed=None, image=None, list=None):
        if not image:
            image = "gota.png"
        super().__init__(image, position, speed)
        if list is not None:
            self.add(list)

    def vel_left(self):
        speed = self.get_speed()
        self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def vel_right(self):
        speed = self.get_speed()
        self.set_speed((speed[0] + self.acceleration[0], speed[1]))

if __name__ == '__main__':
    J = Jogo()
    J.loop()

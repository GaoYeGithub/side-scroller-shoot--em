import asyncio
from engine import GameState
from renderer import Renderer, SpriteRegistry
from sprites import Background, Craft, AsteroidWave, FontSprite, PowerUp, GameEvent
from controls import Input
from pygame import Rect
from pygame.event import Event
from random import randint
from sound_manager import SoundManager  

class BaseState(GameState):
    def __init__(self, score: int = 0):
        self.score: int = score
        self.font: FontSprite = FontSprite()

    def on_event(self, e: Event, sound: SoundManager) -> None:
        if e.gtype == GameEvent.CRAFT_SHOOTED:
            sound.play(SoundManager.FIRE)  # Play sound
        elif e.gtype == GameEvent.ENEMY_DESTROYED:
            ''' play sound, increase score '''
            sound.play(SoundManager.EXPLODE)
            self.score += e.points
        elif e.gtype == GameEvent.PLAYER_DESTROYED:
            sound.play(SoundManager.PLAYER_EXPLODE)

    def draw_score(self, renderer: Renderer) -> None:
        word = str(self.score)
        word = word.zfill(8)
        self.font.display(word)
        self.font.draw(renderer)


class LoadState(BaseState):

    def __init__(self, renderer: Renderer):
        super().__init__()
        self.renderer: Renderer = renderer
        self.background: Background = Background()
        self.craft: Craft = Craft(renderer.bb_size)

    async def update(self, time: int, input: Input) -> None:
        await asyncio.sleep(0)

    def draw(self, renderer: Renderer) -> None:
        pass

    def state(self) -> GameState:
        return GetReadyState(self)


class GetReadyState(BaseState):
    def __init__(self, state: GameState, score: int = 0):
        super().__init__(score)
        self.ticks = 0
        self.renderer: Renderer = state.renderer
        self.background: Background = state.background
        self.craft: Craft = Craft(self.renderer.bb_size)

    async def update(self, time: int, input: Input) -> None:
        self.background.update(time)
        self.craft.set_input(input)
        await self.craft.update(time)
        self.ticks += 1
        await asyncio.sleep(0)

    def draw(self, renderer: Renderer) -> None:
        self.background.draw(renderer)
        self.craft.draw(renderer)
        self.renderer.draw(SpriteRegistry.BULLET, Rect(0, 64, 144, 32), Rect(100, 100, 144, 32))
        self.draw_score(renderer)

    def state(self) -> GameState:
        if self.ticks < 60:
            return self
        return PlayState(self, self.score)


class PlayState(BaseState):
    def __init__(self, state: GetReadyState, score: int):
        super().__init__(score)
        self.renderer: Renderer = state.renderer
        self.background: Background = state.background
        self.craft: Craft = state.craft
        self.asteroids: AsteroidWave = AsteroidWave(self.renderer.bb_size)
        self.__dead_tick: int = 0
        self.__powerups: list = []

    async def update(self, time: int, input: Input) -> None:
        self.background.update(time)
        self.craft.set_input(input)
        await self.craft.update(time)
        await self.asteroids.update(time)
        await self.check_collision()
        
        for powerup in self.__powerups:
            powerup.update(time)
            if len(self.__powerups) > 15:
                await asyncio.sleep(0)

    def draw(self, renderer: Renderer) -> None:
        self.background.draw(renderer)
        self.asteroids.draw(renderer)
        self.craft.draw(renderer)
        self.draw_score(renderer)
        [powerup.draw(renderer) for powerup in self.__powerups]

    def state(self) -> GameState:
        if self.craft.is_alive() is False:
            if self.__dead_tick > 60:
                from main_menu import GameOverState
                return GameOverState(self.renderer, self.score)
            self.__dead_tick += 1
        return self

    async def check_collision(self) -> None:
        items = self.asteroids.collide(self.craft)
        for item in items:
            if randint(1, 5) <= 4:
                powerup = PowerUp()
                powerup.rect.center = item.rect.center
                self.__powerups.append(powerup)
                
        for p in self.__powerups[:]:
            if p.collide(self.craft):
                p.destroy()
                self.__powerups.remove(p)
                self.craft.power_up(p.skin)
        
        await asyncio.sleep(0)
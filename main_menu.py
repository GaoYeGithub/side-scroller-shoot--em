from engine import GameState
from renderer import Renderer, SpriteRegistry
from sprites import Background, FontSprite
from controls import Input, State
from pygame import Rect
from pygame.event import Event
from sound_manager import SoundManager

class MainMenuState(GameState):
    def __init__(self, renderer: Renderer):
        super().__init__()
        self.renderer = renderer
        self.background = Background()
        self.font = FontSprite()
        self.ticks = 0
        self.blink_timer = 0
        self.show_start_text = True
        
    async def update(self, time: int, input: Input) -> None:
        self.background.update(time)
        
        self.blink_timer += 1
        if self.blink_timer > 30:
            self.show_start_text = not self.show_start_text
            self.blink_timer = 0
        
        buttons = input.get_buttons()
        if buttons.is_pressed(State.START):
            self.ticks = 1 
            
    def draw(self, renderer: Renderer) -> None:
        self.background.draw(renderer)
        
        self.font.display("SPACE SHOOTER")
        self.draw_text_at_position(renderer, 100, 40)
        
        controls_y = 80
        line_spacing = 18
        
        self.font.display("CONTROLS:")
        self.draw_text_at_position(renderer, 110, controls_y)
        
        self.font.display("ARROW KEYS - MOVE")
        self.draw_text_at_position(renderer, 80, controls_y + line_spacing)
        
        self.font.display("SPACE - SHOOT")
        self.draw_text_at_position(renderer, 100, controls_y + line_spacing * 2)
        
        self.font.display("ENTER - START")
        self.draw_text_at_position(renderer, 105, controls_y + line_spacing * 3)
        
        self.font.display("ESC - QUIT")
        self.draw_text_at_position(renderer, 115, controls_y + line_spacing * 4)
        
        if self.show_start_text:
            self.font.display("PRESS START")
            self.draw_text_at_position(renderer, 105, 200)
    
    def draw_text_at_position(self, renderer: Renderer, x: int, y: int) -> None:
        for i, char in enumerate(self.font.letters):
            if char in self.font.chars:
                n = self.font.chars.index(char)
                src_y = (n // self.font.CHAR_PER_ROW) * self.font.HEIGHT
                src_x = (n % (self.font.CHAR_PER_ROW + 1)) * self.font.WIDTH
                src = Rect(src_x, src_y, self.font.WIDTH, self.font.HEIGHT)
                dest = Rect(x + (i * 8), y, self.font.WIDTH, self.font.HEIGHT)
                renderer.draw(SpriteRegistry.FONTS, src, dest)
    
    def state(self) -> GameState:
        if self.ticks > 0:
            from game import LoadState
            return LoadState(self.renderer)
        return self
    
    def on_event(self, e: Event, sound: SoundManager = None) -> None:
        pass


class GameOverState(GameState):
    def __init__(self, renderer: Renderer, score: int):
        super().__init__()
        self.renderer = renderer
        self.background = Background()
        self.font = FontSprite()
        self.score = score
        self.ticks = 0
        self.blink_timer = 0
        self.show_restart_text = True
        
    async def update(self, time: int, input: Input) -> None:
        self.background.update(time)
        
        self.blink_timer += 1
        if self.blink_timer > 30:
            self.show_restart_text = not self.show_restart_text
            self.blink_timer = 0
        
        buttons = input.get_buttons()
        if buttons.is_pressed(State.START):
            self.ticks = 1
            
    def draw(self, renderer: Renderer) -> None:
        self.background.draw(renderer)
        
        self.font.display("GAME OVER")
        self.draw_text_at_position(renderer, 110, 80)
        
        score_text = f"SCORE: {str(self.score).zfill(8)}"
        self.font.display(score_text)
        self.draw_text_at_position(renderer, 80, 120)
        
        if self.show_restart_text:
            self.font.display("PRESS START TO CONTINUE")
            self.draw_text_at_position(renderer, 55, 160)
    
    def draw_text_at_position(self, renderer: Renderer, x: int, y: int) -> None:
        for i, char in enumerate(self.font.letters):
            if char in self.font.chars:
                n = self.font.chars.index(char)
                src_y = (n // self.font.CHAR_PER_ROW) * self.font.HEIGHT
                src_x = (n % (self.font.CHAR_PER_ROW + 1)) * self.font.WIDTH
                src = Rect(src_x, src_y, self.font.WIDTH, self.font.HEIGHT)
                dest = Rect(x + (i * 8), y, self.font.WIDTH, self.font.HEIGHT)
                renderer.draw(SpriteRegistry.FONTS, src, dest)
    
    def state(self) -> GameState:
        if self.ticks > 0:
            return MainMenuState(self.renderer)
        return self
    
    def on_event(self, e: Event, sound: SoundManager = None) -> None:
        pass

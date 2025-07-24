import asyncio
from engine import Engine
from renderer import SdlRenderer, SpriteRegistry
from main_menu import MainMenuState

async def main():
    renderer = SdlRenderer(320, 240, 800, 600)
    engine: Engine = Engine(renderer)
    
    renderer.register_image(SpriteRegistry.BACKGROUND, "assets/background.png")
    renderer.register_image(SpriteRegistry.CRAFT, "assets/pxplayer.png")
    renderer.register_image(SpriteRegistry.BULLET, "assets/bullets.png")
    renderer.register_image(SpriteRegistry.ASTEROID, "assets/level1_sprites.png")
    renderer.register_image(SpriteRegistry.EXPLOSION, "assets/explosion.png")
    renderer.register_image(SpriteRegistry.FONTS, "assets/font.png")
    renderer.register_image(SpriteRegistry.POWERUP, "assets/power-up.png")
    
    await engine.run(MainMenuState(renderer))

if __name__ == "__main__":
    asyncio.run(main())

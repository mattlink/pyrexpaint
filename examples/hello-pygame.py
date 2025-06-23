import pygame
import pyrexpaint
import sys
import os

def main():
    # Load the .xp file using pyrexpaint
    try:
        image_layers = pyrexpaint.load("hello.xp")
        layer = image_layers[0]  # Use the first layer
    except FileNotFoundError:
        print("Error: hello.xp file not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading .xp file: {e}")
        sys.exit(1)

    # Initialize pygame
    pygame.init()
    
    # Set up display
    TILE_SIZE = 12  # Size of each character in pixels
    SCREEN_WIDTH = layer.width * TILE_SIZE
    SCREEN_HEIGHT = layer.height * TILE_SIZE
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PyREXPaint - Pygame Example")
    
    # Set up font for rendering characters
    try:
        # Try to use a monospace font
        font = pygame.font.Font(pygame.font.get_default_font(), TILE_SIZE)
    except:
        font = pygame.font.Font(None, TILE_SIZE)
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Clear screen with black background
        screen.fill((0, 0, 0))
        
        # Render each tile from the .xp file
        for y in range(layer.height):
            for x in range(layer.width):
                # Calculate tile position in the tiles array
                tile_index = x + y * layer.width
                
                if tile_index < len(layer.tiles):
                    tile = layer.tiles[tile_index]
                    
                    # Decode the character from cp437 encoding
                    try:
                        char = tile.ascii_code.decode("cp437")
                        char = char.replace(chr(0), " ")  # Replace null characters with spaces
                    except:
                        char = " "
                    
                    # Skip empty characters
                    if char.strip():
                        # Get colors (pyrexpaint stores as integers 0-255)
                        fg_color = (tile.fg_r, tile.fg_g, tile.fg_b)
                        bg_color = (tile.bg_r, tile.bg_g, tile.bg_b)
                        
                        # Calculate pixel position
                        pixel_x = x * TILE_SIZE
                        pixel_y = y * TILE_SIZE
                        
                        # Draw background rectangle if background color is not black
                        if bg_color != (0, 0, 0):
                            bg_rect = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
                            pygame.draw.rect(screen, bg_color, bg_rect)
                        
                        # Render the character
                        if char != " ":
                            text_surface = font.render(char, True, fg_color)
                            screen.blit(text_surface, (pixel_x, pixel_y))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    # Cleanup
    pygame.quit()

if __name__ == "__main__":
    main()

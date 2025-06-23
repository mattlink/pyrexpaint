import pygame
import pyrexpaint
import sys
import os

# Initialize pygame
pygame.init()

# Load the .xp file
try:
    image_layers = pyrexpaint.load("hello.xp")
    layer = image_layers[0]  # Use the first layer
except FileNotFoundError:
    print("Error: hello.xp file not found. Make sure it exists in the examples directory.")
    sys.exit(1)

# Constants
TILE_SIZE = 16  # Size of each character tile
FONT_SIZE = 14

# Calculate window size based on the image dimensions
WINDOW_WIDTH = layer.width * TILE_SIZE
WINDOW_HEIGHT = layer.height * TILE_SIZE

# Create the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PyREXPaint - Pygame Example")

# Initialize font (using monospace font for better ASCII art display)
try:
    font = pygame.font.Font(pygame.font.match_font('courier'), FONT_SIZE)
except:
    font = pygame.font.Font(None, FONT_SIZE)

# Position calculation helper (same as ncurses example)
pos = lambda x, y: x + y * layer.height

def main():
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
        
        # Clear screen
        screen.fill((0, 0, 0))  # Black background
        
        # Draw tiles
        for x in range(layer.width):
            for y in range(layer.height):
                tile = layer.tiles[pos(x, y)]
                
                # Decode the character from cp437
                try:
                    char = tile.ascii_code.decode("cp437")
                    char = char.replace(chr(0), " ")  # Replace null chars with space
                    
                    # Skip empty characters
                    if not char or char == chr(0):
                        char = " "
                    
                    # Create colors from tile data
                    fg_color = (tile.fg_r, tile.fg_g, tile.fg_b)
                    bg_color = (tile.bg_r, tile.bg_g, tile.bg_b)
                    
                    # Calculate pixel position
                    pixel_x = x * TILE_SIZE
                    pixel_y = y * TILE_SIZE
                    
                    # Draw background rectangle if it's not black
                    if bg_color != (0, 0, 0):
                        bg_rect = pygame.Rect(pixel_x, pixel_y, TILE_SIZE, TILE_SIZE)
                        pygame.draw.rect(screen, bg_color, bg_rect)
                    
                    # Render and draw the character
                    if char.strip():  # Only render non-whitespace characters
                        text_surface = font.render(char, True, fg_color)
                        screen.blit(text_surface, (pixel_x, pixel_y))
                        
                except (UnicodeDecodeError, AttributeError):
                    # Skip problematic characters
                    pass
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    print("PyREXPaint Pygame Example")
    print("Press ESC or close window to exit")
    print(f"Loading image: {layer.width}x{layer.height} pixels")
    main()

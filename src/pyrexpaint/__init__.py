import gzip
from typing import List
from dataclasses import dataclass

META_SIZE = 8
META_OFFSETS = {
    "version": (0,4),
    "layers": (4,8),
}

# offsets relative to a given layer context (starting byte)
LAYER_META_SIZE = 8
LAYER_META_OFFSETS = {
    "width": (0, 4),
    "height": (4, 8),
}

# offests relative to given image contxt within layer
TILE_SIZE = 10
TILE_OFFSETS = {
    "ascii": (0, 4),
    "fg_r": (4, 5),
    "fg_g": (5, 6),
    "fg_b": (6, 7),
    "bg_r": (7, 8),
    "bg_g": (8, 9),
    "bg_b": (9, 10),
}

def load_offset_raw(xp_data: bytes, offsets: dict, offset_key: str) -> bytes:
    offset = offsets.get(offset_key)
    assert offset, f"No offset found for {offset_key}"
    return xp_data[offset[0]:offset[1]]

def load_offset(xp_data: bytes, offsets: dict, offset_key: str) -> int:
    offset = offsets.get(offset_key)
    assert offset, f"No offset found for {offset_key}"
    return int.from_bytes(
        xp_data[offset[0]:offset[1]],
        byteorder="little"
    )


@dataclass
class Tile:
    """Represents a single tile/character in a REXPaint image.
    
    Each tile contains an ASCII character and foreground/background color information.
    
    Attributes:
        ascii_code: Raw bytes representing the ASCII character code
        fg_r: Red component of foreground color (0-255)
        fg_g: Green component of foreground color (0-255) 
        fg_b: Blue component of foreground color (0-255)
        bg_r: Red component of background color (0-255)
        bg_g: Green component of background color (0-255)
        bg_b: Blue component of background color (0-255)
    """
    ascii_code: bytes
    fg_r: int
    fg_g: int
    fg_b: int
    bg_r: int
    bg_g: int
    bg_b: int


@dataclass
class ImageLayer:
    width: int
    height: int
    tiles: List[Tile]


def load(file_name: str) -> List[ImageLayer]:
    images = []

    xp_data = gzip.open(file_name).read()
    # Load and decompress the .xp file data
    offset = 0
 
    version = load_offset(xp_data[offset:], META_OFFSETS, "version")
    # Parse file metadata (version and layer count)
    layers = load_offset(xp_data[offset:], META_OFFSETS, "layers")
    offset += META_SIZE

    for layer in range(layers):
    # Process each layer in the file
        image_width = load_offset(xp_data[offset:], LAYER_META_OFFSETS, "width")
        # Parse layer dimensions
        image_height = load_offset(xp_data[offset:], LAYER_META_OFFSETS, "height")
        offset += LAYER_META_SIZE

        num_tiles = image_width * image_height
        # Parse all tiles in this layer
        tiles: List[Tile] = []
        
        for tile_idx in range(num_tiles):
            # Calculate offset for this specific tile
            tile_offset = offset + (tile_idx * TILE_SIZE)
            
            # Extract tile data (character and colors)
            ascii_code = load_offset_raw(xp_data[tile_offset:], TILE_OFFSETS, "ascii")
            fg_r = load_offset(xp_data[tile_offset:], TILE_OFFSETS, "fg_r")
            fg_g = load_offset(xp_data[tile_offset:], TILE_OFFSETS, "fg_g")
            fg_b = load_offset(xp_data[tile_offset:], TILE_OFFSETS, "fg_b")
            bg_r = load_offset(xp_data[tile_offset:], TILE_OFFSETS, "bg_r")
            bg_g = load_offset(xp_data[tile_offset:], TILE_OFFSETS, "bg_g")
            bg_b = load_offset(xp_data[tile_offset:], TILE_OFFSETS, "bg_b")

        # Move offset past all tiles in this layer
            tiles.append(Tile(ascii_code, fg_r, fg_g, fg_b, bg_r, bg_g, bg_b))

        offset += num_tiles * TILE_SIZE
        images.append(ImageLayer(image_width, image_height, tiles))

    return images

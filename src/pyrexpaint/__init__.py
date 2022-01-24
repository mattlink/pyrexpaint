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

def load_offset_raw(xp_data: bytes, offsets: dict, offset_key: str) -> str:
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
    ascii_code: str
    fg_r: str
    fg_g: str
    fg_b: str
    bg_r: str
    bg_g: str
    bg_b: str


@dataclass
class ImageLayer:
    width: int
    height: int
    tiles: List[Tile]


def load(file_name: str) -> List[ImageLayer]:
    images = []

    xp_data = gzip.open(file_name).read()
 
    version = load_offset(xp_data, META_OFFSETS, "version")
    layers = load_offset(xp_data, META_OFFSETS, "layers")

    # Reset offset context (we're done parsing metadata)
    xp_data = xp_data[META_SIZE:] 

    for layer in range(layers):
        image_width = load_offset(xp_data, LAYER_META_OFFSETS, "width")
        image_height = load_offset(xp_data, LAYER_META_OFFSETS, "height")

        image = ImageLayer(image_width, image_height, [])

        # Reset layer offset context
        xp_data = xp_data[LAYER_META_SIZE:]

        num_tiles = image_width * image_height
        for tile in range(num_tiles):
            
            ascii_code = load_offset_raw(xp_data, TILE_OFFSETS, "ascii")
            fg_r = load_offset(xp_data, TILE_OFFSETS, "fg_r")
            fg_g = load_offset(xp_data, TILE_OFFSETS, "fg_g")
            fg_b = load_offset(xp_data, TILE_OFFSETS, "fg_b")
            bg_r = load_offset(xp_data, TILE_OFFSETS, "bg_r")
            bg_g = load_offset(xp_data, TILE_OFFSETS, "bg_g")
            bg_b = load_offset(xp_data, TILE_OFFSETS, "bg_b")

            image.tiles.append(Tile(ascii_code, fg_r, fg_g, fg_b, bg_r, bg_g, bg_b))

            # Reset tile offset context
            xp_data = xp_data[TILE_SIZE:]

        images.append(image)

    return images
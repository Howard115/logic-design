from PIL import Image

def image_to_matrix(image_path: str) -> list[list[int]]:
    """Converts a 32x32 pixel art image into a binary matrix of 0s and 1s."""
    img = Image.open(image_path).convert('L').resize((32, 32))
    return [[1 if img.getpixel((col, row)) < 128 else 0 for col in range(32)] for row in range(32)]

import pyperclip

pyperclip.copy(image_to_matrix("/Users/howardlin/Downloads/pixelated-image.png"))


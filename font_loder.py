from PIL import Image, ImageDraw, ImageFont, ImageChops
import os
import math

ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!%()+,-;_.'"


def crop_left_right(image, background=255):
    """Przytnij tylko lewe i prawe marginesy — wysokość pozostaje bez zmian"""
    bg = Image.new(image.mode, image.size, background)
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    
    if bbox:
        left, _, right, _ = bbox
        _, height = image.size
        return image.crop((left, 0, right, height))  # zachowujemy pełną wysokość
    else:
        return image  # pusty obraz

def load_letters(font_name , font_size , offset, size_pt = 64, characters = ALFABET):
    
    font_path = f"fonts/{font_name}.ttf"  
    output_dir = f"letters\{font_name}"
    image_size = (size_pt, size_pt)

    os.makedirs(output_dir, exist_ok=True)

    font = ImageFont.truetype(font_path, font_size)
    
    for char in characters:
        image = Image.new("L", image_size, color=255)
        # image = ImageOps.invert(image)
        draw = ImageDraw.Draw(image)

        left, _, right, _ = draw.textbbox((0, 0), char, font=font)
        w = right - left
        x = math.ceil((image_size[0] - w)/2)
        y = offset # dobrane metodą prób i błędów

        draw.text((x, y), char, font=font, fill=0)
        image = crop_left_right(image)
        image = image.point(lambda p: 255 if p > 128 else 0)  # Próg = 128
        image.save(os.path.join(output_dir, f"{char}.png"), "PNG")

def main():
    load_letters("tahoma", 64,-14)
    load_letters("arial", 64,-10)
    load_letters("times_new_roman", 64,-10)
    load_letters("latin_modern_roman", 64,-23)

main()
from PIL import Image, ImageDraw, ImageFont, ImageChops
import os, math, random

ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!%()+,-;_.'"

def crop_all(image, background=255):
    """Przytnij tylko lewe i prawe marginesy — wysokość pozostaje bez zmian"""
    bg = Image.new(image.mode, image.size, background)
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    
    if bbox:
        return image.crop(bbox)  # zachowujemy pełną wysokość
    else:
        return image  # pusty obraz
    
def add_margin(image, margin = 100):
    """Przytnij tylko lewe i prawe marginesy — wysokość pozostaje bez zmian"""
    new_width = image.size[0] + 2 * margin
    new_height = image.size[1] + 2 * margin
    new_image = Image.new(image.mode, (new_width, new_height), 255)
    new_image.paste(image, (margin, margin))
    return new_image
def rotate_text(image, angle):
    """
    Obraca obraz o zadany kąt w stopniach.
    Zachowuje cały tekst w obrębie obrazu przez odpowiednie powiększenie.
    """
    # Oblicz nowy rozmiar obrazu po obrocie
    angle_rad = math.radians(angle)
    w, h = image.size
    
    # Oblicz nowe wymiary, aby zmieścić obrócony tekst
    new_w = abs(w * math.cos(angle_rad)) + abs(h * math.sin(angle_rad))
    new_h = abs(w * math.sin(angle_rad)) + abs(h * math.cos(angle_rad))
    
    # Stwórz nowy obraz z białym tłem
    new_image = Image.new('L', (int(new_w), int(new_h)), 255)
    
    # Wklej oryginalny obraz na środek
    paste_x = int((new_w - w) / 2)
    paste_y = int((new_h - h) / 2)
    new_image.paste(image, (paste_x, paste_y))
    
    # Obróć obraz względem środka
    rotated = new_image.rotate(angle, expand=True, fillcolor=255)
    
    return rotated

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import os

def create_font_text(text, name, font_name, rotate, font_size=66, output_dir="./text_images", blur=False, noise_level=50):
    font_path = f"fonts/{font_name}.ttf"  
    image = Image.new("L", (2**12, 2**12), color=255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)

    lines = text.split("\n")

    line_height = draw.textbbox((0, 0), "(", font=font)[3]

    y = 0  # pionowa pozycja początkowa
    for line in lines:
        bbox = draw.textbbox((0, y), line, font=font)
        w = bbox[2] - bbox[0]
        x = 0  # centrowanie poziome
        draw.text((x, y), line, font=font, fill=0)
        y += line_height * 1.2  # odstęp między liniami

    if rotate:
        image = rotate_text(image, -random.randint(15, 35))

    # Dodanie minimalnego zaszumienia
    image = add_margin(crop_all(image))
    
    if blur:
        image_np = np.array(image).astype(np.int16)  # konwersja do numpy, int16, żeby nie było przepełnień
        noise = np.random.randint(-noise_level, noise_level + 1, image_np.shape)  # szum w zakresie [-noise_level, noise_level]
        image_np += noise
        image_np = np.clip(image_np, 0, 255).astype(np.uint8)  # przycięcie wartości do zakresu 0-255 i konwersja z powrotem

        image = Image.fromarray(image_np)

    
    image.save(os.path.join(output_dir, f"{name}_{font_name}.png"), "PNG")


def main():
    text = "What is Lorem Ipsum \n\n"\
                "Lorem Ipsum is simply dummy text of the printing and typesetting\n" \
                "industry. Lorem Ipsum has been the industry's standard dummy\n" \
                "text ever since the 1500s, when an unknown printer took a galley\n" \
                "of type and scrambled it to make a type specimen book. It has\n" \
                "survived not only five centuries, but also the leap into electronic\n" \
                "typesetting, remaining essentially unchanged. It was popularised in\n" \
                "the 1960s with the release of Letraset sheets containing Lorem\n" \
                "Ipsum passages, and more recently with desktop publishing\n" \
                "software like Aldus PageMaker including versions of Lorem Ipsum!"
    
    # create_font_text(text, "text1", "arial", rotate = False)
    # create_font_text(text, "text1", "latin_modern_roman", rotate = False)
    # create_font_text(text, "text1", "times_new_roman", rotate = False)
    # create_font_text(text, "text1", "tahoma", rotate = False)

    # create_font_text(text, "text2", "arial", rotate = True)
    # create_font_text(text, "text2", "latin_modern_roman", rotate = True)
    # create_font_text(text, "text2", "times_new_roman", rotate = True)
    # create_font_text(text, "text2", "tahoma", rotate = True)

    text2 = "The quick brown fox jumps over the lazy dog. \n" \
                "Sphinx of black quartz, judge my vow \n" \
                "Pack my box with five dozen liquor jugs. \n" \
                "With 15% of all"

    create_font_text(text2, "text3", "arial", rotate = True, blur=True)
    create_font_text(text2, "text3", "latin_modern_roman", rotate = True, blur=True)
    create_font_text(text2, "text3", "times_new_roman", rotate = True, blur=True)
    create_font_text(text2, "text3", "tahoma", rotate = True, blur=True, blur=True)



main()
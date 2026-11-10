"""
App Logo Updater for TREVIORA AI DEFENDER
Processes D:\projects\antivirus\logo.png provided by user:
1. Generates resources/icon.png
2. Generates resources/treviora_logo.jpg
3. Generates resources/treviora_circular_avatar.png
4. Generates multi-resolution resources/icon.ico for Windows Executable & Taskbar
"""
import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw

BASE_DIR = Path("D:/projects/antivirus").resolve()
LOGO_SRC = BASE_DIR / "logo.png"
RESOURCES_DIR = BASE_DIR / "resources"
RESOURCES_DIR.mkdir(parents=True, exist_ok=True)

def update_logos():
    print(f"Loading user logo from: {LOGO_SRC}")
    if not LOGO_SRC.exists():
        print(f"Error: {LOGO_SRC} not found!")
        return False

    img = Image.open(LOGO_SRC).convert("RGBA")
    print(f"Original image size: {img.size}")

    # 1. Save standard high-res icon.png (512x512)
    icon_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
    icon_png_path = RESOURCES_DIR / "icon.png"
    icon_512.save(icon_png_path, "PNG")
    print(f"Generated: {icon_png_path}")

    # 2. Save treviora_logo.jpg (high quality RGB)
    rgb_img = Image.new("RGB", img.size, (4, 8, 20))
    rgb_img.paste(img, mask=img.split()[3])
    logo_jpg_path = RESOURCES_DIR / "treviora_logo.jpg"
    rgb_img.save(logo_jpg_path, "JPEG", quality=95)
    print(f"Generated: {logo_jpg_path}")

    # 3. Save circular avatar for UI headers & sidebars (512x512 circular mask)
    size = 512
    circ_img = img.resize((size, size), Image.Resampling.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (size, size)], radius=size // 4, fill=255)
    
    avatar = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    avatar.paste(circ_img, (0, 0), mask=mask)
    avatar_path = RESOURCES_DIR / "treviora_circular_avatar.png"
    avatar.save(avatar_path, "PNG")
    print(f"Generated: {avatar_path}")

    # 4. Generate multi-resolution icon.ico for Windows taskbar and EXE
    ico_path = RESOURCES_DIR / "icon.ico"
    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, format="ICO", sizes=icon_sizes)
    print(f"Generated Windows Icon: {ico_path}")

    # 5. Copy to dist folders as well so compiled exe picks it up immediately
    dist_res = BASE_DIR / "dist" / "Treviora_AI_Defender" / "_internal" / "resources"
    if dist_res.exists():
        icon_512.save(dist_res / "icon.png", "PNG")
        rgb_img.save(dist_res / "treviora_logo.jpg", "JPEG", quality=95)
        avatar.save(dist_res / "treviora_circular_avatar.png", "PNG")
        print("Updated internal dist resources as well.")

    print("\nALL LOGO ASSETS UPDATED SUCCESSFULLY!")
    return True

if __name__ == "__main__":
    update_logos()

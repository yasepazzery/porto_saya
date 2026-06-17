from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageFont

src = 'images/Foto yasep.jpg'
out = 'images/foto-yasep-theme.jpg'

img = Image.open(src).convert('RGBA')

w, h = img.size
size = (900, 1100)
base = Image.new('RGBA', size, (12, 23, 42, 255))

# Soft gradient background
for y in range(size[1]):
    t = y / size[1]
    r = int(13 + 20 * t)
    g = int(23 + 35 * t)
    b = int(42 + 70 * t)
    for x in range(size[0]):
        base.putpixel((x, y), (r, g, b, 255))

# Add subtle glow
shade = Image.new('RGBA', size, (0, 0, 0, 0))
for y in range(size[1]):
    for x in range(size[0]):
        dx = x - size[0] * 0.75
        dy = y - size[1] * 0.18
        d = (dx * dx + dy * dy) ** 0.5
        a = max(0, 120 - int(d * 1.6))
        if a:
            shade.putpixel((x, y), (56, 189, 248, a))
base = Image.alpha_composite(base, shade)

# Resize and round photo corners
photo = ImageOps.fit(img, (int(size[0] * 0.62), int(size[1] * 0.72)), method=Image.Resampling.LANCZOS)
photo = photo.convert('RGBA')
mask = Image.new('L', photo.size, 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, photo.size[0] - 1, photo.size[1] - 1), radius=45, fill=255)
rounded = Image.new('RGBA', photo.size, (0, 0, 0, 0))
rounded.paste(photo, (0, 0), mask)

bx = (size[0] - rounded.size[0]) // 2
by = 80
base.paste(rounded, (bx, by), rounded)

# Soft accent panel
panel = Image.new('RGBA', (size[0] - 120, 110), (255, 255, 255, 18))
panel = panel.filter(ImageFilter.GaussianBlur(1))
base.paste(panel, (60, size[1] - 160), panel)

# Add a small label for the portfolio theme
font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 28)
ImageDraw.Draw(base).text((90, size[1] - 132), 'Yasep Azzery • Tech Enthusiast', fill=(240, 247, 255, 255), font=font)

base = base.resize((640, 800), Image.Resampling.LANCZOS).convert('RGB')
base.save(out, quality=95)
print('saved', out, base.size)

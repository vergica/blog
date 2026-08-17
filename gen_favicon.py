#!/usr/bin/env python3
# 梅岭随记 favicon — 月光主题
# 生成: favicon.ico, favicon-16x16.png, favicon-32x32.png, apple-touch-icon.png, favicon-192x192.png
from PIL import Image, ImageDraw, ImageFilter
import random, os

S = 512
random.seed(42)

def lerp3(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

top = (26, 30, 70)     # 夜空顶: 深蓝
bot = (8, 10, 30)      # 夜空底: 更深蓝

# ---------- 1. 垂直渐变夜空 ----------
base = Image.new("RGBA", (S, S))
px = base.load()
for y in range(S):
    c = lerp3(top, bot, y / (S - 1))
    for x in range(S):
        px[x, y] = (c[0], c[1], c[2], 255)

# ---------- 2. 星光 ----------
star_fix = ImageDraw.Draw(base)
mcx, mcy = S * 0.5, S * 0.44
for i in range(11):
    for _ in range(60):
        x, y = random.random() * S, random.random() * S
        if (x - mcx) ** 2 + (y - mcy) ** 2 > (0.36 * S) ** 2 and y < S * 0.85:
            break
    r = random.choice([1, 1, 2])
    a = random.randint(120, 230)
    if r == 2:  # 亮星带小光晕
        st = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        ImageDraw.Draw(st).ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 255, 250, a))
        base = Image.alpha_composite(base, st.filter(ImageFilter.GaussianBlur(2)))
    else:
        star_fix.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 252, a))

# ---------- 3. 月晕 (高斯模糊的柔光) ----------
glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
glow_r = 0.30 * S
ImageDraw.Draw(glow).ellipse(
    [mcx - glow_r, mcy - glow_r, mcx + glow_r, mcy + glow_r],
    fill=(255, 240, 190, 255),
)
glow = glow.filter(ImageFilter.GaussianBlur(60))

# ---------- 4. 圆月 (锐利) ----------
moon = Image.new("RGBA", (S, S), (0, 0, 0, 0))
md = ImageDraw.Draw(moon)
R = 0.205 * S
md.ellipse([mcx - R, mcy - R, mcx + R, mcy + R], fill=(255, 246, 216, 255))
# 两处极淡环形山, 增加质感 (小尺寸下几乎不可见, 不破坏清晰)
md.ellipse([mcx - R * 0.2, mcy + R * 0.02, mcx - R * 0.03, mcy + R * 0.2], fill=(232, 211, 155, 70))
md.ellipse([mcx + R * 0.02, mcy - R * 0.28, mcx + R * 0.2, mcy - R * 0.06], fill=(232, 211, 155, 50))

# ---------- 合成 ----------
final = Image.alpha_composite(base, glow)
final = Image.alpha_composite(final, moon)

# ---------- 输出各尺寸 ----------
static = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

def save(name, size):
    img = final.resize((size, size), Image.LANCZOS)
    img.save(os.path.join(static, name))
    print(f"  {name}  {size}x{size}")

print("生成 favicon → static/:")
save("favicon-16x16.png", 16)
save("favicon-32x32.png", 32)
save("favicon-192x192.png", 192)
save("apple-touch-icon.png", 180)

# 多尺寸 ICO
ico = final.resize((64, 64), Image.LANCZOS)
ico.save(os.path.join(static, "favicon.ico"),
         sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64)])
print("  favicon.ico  [16,24,32,48,64]")

# 预览大图(便于核对效果)
final.resize((256, 256), Image.LANCZOS).save("/tmp/favicon_preview.png")
print("  /tmp/favicon_preview.png (256) 预览")
print("完成 ✓")

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
from pathlib import Path

st.set_page_config(page_title="CIE 1931 色度圖標示工具", layout="centered")

st.title("🎨 CIE 1931 色度圖標示工具")
st.markdown("請輸入 CIE xy 座標（格式：`x y label`），每行一組，例如：")
st.code("0.3127 0.3291 D65\n0.64 0.33 R\n0.30 0.60 G\n0.15 0.06 B")

# === 使用者輸入區 ===
user_input = st.text_area("輸入座標資料", height=150)
generate_btn = st.button("生成標示圖")

# === 基本設定 ===
bg_path = Path(__file__).parent / "assets" / "backkground.jpg"
x0_px, y0_px = 40, 735
x_max_px, y_max_px = 678, 735
y_top_px = 16
x_max, y_max = 0.8, 0.9

sx = (x_max_px - x0_px) / x_max
sy = (y0_px - y_top_px) / y_max

def xy_to_px(x, y):
    px = x0_px + sx * x
    py = y0_px - sy * y
    return px, py

# === 處理邏輯 ===
if generate_btn:
    if not user_input.strip():
        st.warning("請先輸入座標！")
    else:
        # 載入背景圖
        img = Image.open(bg_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        # 字型設定
        try:
            font = ImageFont.truetype("arial.ttf", 18)
        except:
            font = ImageFont.load_default()

        # 逐行解析輸入
        for line in user_input.strip().splitlines():
            try:
                parts = line.split()
                x, y = float(parts[0]), float(parts[1])
                label = parts[2] if len(parts) > 2 else ""
                if not (0 <= x <= x_max and 0 <= y <= y_max):
                    st.warning(f"⚠️ 超出範圍：({x},{y})，已略過。")
                    continue
                px, py = xy_to_px(x, y)
                r = 6
                draw.line((px - r, py, px + r, py), width=2, fill=(0, 0, 0))
                draw.line((px, py - r, px, py + r), width=2, fill=(0, 0, 0))
                draw.text((px + 8, py - 12), f"{label} ({x:.4f},{y:.4f})", fill=(0, 0, 0), font=font)
            except Exception as e:
                st.error(f"❌ 無法解析：{line}")

        # 轉成 bytes 並顯示
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="標示結果", use_container_width=True)

        st.download_button(
            label="⬇️ 下載標示後圖片",
            data=buf.getvalue(),
            file_name="cie_marked_points.png",
            mime="image/png"
        )

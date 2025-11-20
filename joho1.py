import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

st.title("画像の代表色抽出アプリ")
st.write('画像から色を摘出してくれます！')

# 画像アップロード
uploaded_file = st.file_uploader("画像をアップロードしてください。", type=["jpg", "jpeg", "png", "avif"])

if uploaded_file is not None:
    # 画像を開く（RGBに統一）
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    # NumPy配列に変換
    img_array = np.array(image)
    pixels = img_array.reshape(-1, 3)  # すべてのピクセルを1次元に並べる

    # クラスタ数（抽出したい代表色の数）
    n_colors = st.slider("抽出する代表色の数", 2, 40, 20)

    import time


    # K-meansでクラスタリング
    kmeans = KMeans(n_clusters=n_colors, random_state=0, n_init=10)
    kmeans.fit(pixels)

    # 各クラスタの代表色（RGB平均値）
    colors = kmeans.cluster_centers_.astype(int)
    st.subheader("抽出された代表色")

    # 結果を表示
    cols = st.columns(n_colors)
    for i, color in enumerate(colors):
        r, g, b = color
        hex_color = '#%02x%02x%02x' % (r, g, b)  # HEXに変換
        with cols[i]:
            st.markdown(
                f"""
                <div style="background-color:{hex_color};
                            width:100px;height:100px;
                            border-radius:10px;margin:auto"></div>
                <p style="text-align:center;">{hex_color}</p>
                """,
                unsafe_allow_html=True
            )

st.write('有名な色は以下の通りです。')
colors = [
    {"name": "赤",       "hex": "#ff0000", "rgb": (255, 0, 0)},
    {"name": "青",      "hex": "#0000ff", "rgb": (0, 0, 255)},
    {"name": "黄色",    "hex": "#ffff00", "rgb": (255, 255, 0)},
    {"name": "緑",     "hex": "#008000", "rgb": (0, 128, 0)},
    {"name": "黄緑",     "hex": "#9acd32", "rgb": (154, 205, 50)} ,
    {"name": "紫",    "hex": "#800080", "rgb": (128, 0, 128)},
    {"name": "オレンジ",    "hex": "#ffa500", "rgb": (255, 165, 0)},
    {"name": "橙",   "hex": "#ff8c00", "rgb": (255, 140, 0)},  # 橙（明るいオレンジ）
    {"name": "茶色",     "hex": "#8b4513", "rgb": (139, 69, 19)}
]

# 表の中身
for c in colors:
    st.markdown(
        f"""
        | <div style="width:30px; height:20px; background:{c['hex']}; 
                       border-radius:4px; border:1px solid #00000033"></div>
        | {c['name']} | {c['hex']} | 
        """,
        unsafe_allow_html=True
    )
import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans

# --- 1. キャッシュ機能 ---
@st.cache_data
def get_colors_from_image(img_array, n_colors):
    pixels = img_array.reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_colors, random_state=0, n_init=10)
    kmeans.fit(pixels)
    return kmeans.cluster_centers_.astype(int)

st.title("画像の代表色抽出アプリ")
st.write('画像から色を抽出してくれます！')

# 画像アップロード
uploaded_file = st.file_uploader("画像をアップロードしてください。", type=["jpg", "jpeg", "png", "avif"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    # --- 2. エラー回避のためのリサイズ ---
    image_small = image.resize((150, 150))
    img_array = np.array(image_small)

    # スライダー（上限40）
    n_colors = st.slider("抽出する代表色の数", 2, 40, 20)

    if st.button("色を抽出する"):
        with st.spinner('分析中...'):
            colors = get_colors_from_image(img_array, n_colors)
            st.subheader("抽出された代表色")

            # --- 3. 結果の表示（自動折り返し） ---
            cols_per_row = 8 
            for i in range(0, len(colors), cols_per_row):
                cols = st.columns(cols_per_row)
                batch_colors = colors[i : i + cols_per_row]
                
                for col, color in zip(cols, batch_colors):
                    r, g, b = color
                    hex_color = '#%02x%02x%02x' % (r, g, b)
                    # 文字色を背景に合わせて反転
                    text_color = "white" if (r*0.299 + g*0.587 + b*0.114) < 186 else "black"

                    with col:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:{hex_color};
                                width:100%; height:80px;
                                border-radius:8px;
                                display:flex; align-items:center; justify-content:center;
                                color:{text_color}; font-size:10px;
                                border: 1px solid rgba(0,0,0,0.1);
                            ">
                            <br>{hex_color}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

# --- 4. 参考データの表示（色見本を追加） ---
st.divider()
st.subheader('【参考】有名な色のRGB値')

ref_colors = [
    {"name": "赤",       "hex": "#ff0000"},
    {"name": "青",       "hex": "#0000ff"},
    {"name": "黄色",      "hex": "#ffff00"},
    {"name": "緑",       "hex": "#008000"},
    {"name": "黄緑",      "hex": "#9acd32"},
    {"name": "紫",       "hex": "#800080"},
    {"name": "オレンジ",    "hex": "#ffa500"},
    {"name": "茶色",      "hex": "#8b4513"}
]

# ヘッダーを表示
col1, col2, col3 = st.columns([1, 2, 2])
with col1: st.write("**色見本**")
with col2: st.write("**色名**")
with col3: st.write("**HEX値**")

# ループでリストを表示
for c in ref_colors:
    with st.container():
        c1, c2, c3 = st.columns([1, 2, 2]) # 比率: 色1 : 名前2 : コード2
        
        # 色見本 (HTMLで四角を描画)
        with c1:
            st.markdown(
                f'<div style="background-color:{c["hex"]}; height:25px; border-radius:5px; border:1px solid #ddd;"></div>',
                unsafe_allow_html=True
            )
        # 名前
        with c2:
            st.write(c["name"])
        # HEXコード (コピーしやすいようにcodeブロックまたはtext)
        with c3:
            st.text(c["hex"])
        
        # 行間の区切り線（お好みで削除可）
        st.markdown("<hr style='margin: 5px 0; opacity: 0.3;'>", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import numpy as np

st.title('色摘出アプリ')
st.write('取り込んだ画像を書くために必要な色を摘出します。')

from PIL import Image

# 画像ファイルをアップロード
uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "jpeg", "png","avif"])

if uploaded_file is not None:
    # 画像を開く（RGBに統一）
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    # NumPy配列に変換
    img_array = np.array(image)

    # 全ピクセルを (R,G,B) の形に並べる
    pixels = img_array.reshape(-1, 3)

    # 重複をなくしてユニークな色だけを取得
    unique_colors = np.unique(pixels, axis=0)

    # タプルのリストに変換
    color_list = [tuple(color) for color in unique_colors]

    st.write(f"この画像には **{len(color_list)} 種類** の色が使われています。")
    st.write(color_list[:100])  # 最初の100色を表示（多すぎると重いので）

    # 表示を見やすくする（各色を小さなボックスで表示）
    st.subheader("色見本（最初の50色）")
    cols = st.columns(10)
    for i, color in enumerate(color_list[:50]):
        with cols[i % 10]:
            hex_color = '#%02x%02x%02x' % color
            st.markdown(
                f"<div style='background-color:{hex_color}; width:50px; height:50px; border:1px solid #000;'></div>",
                unsafe_allow_html=True
            )
            st.caption(str(color))
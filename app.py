import streamlit as st
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="FANZAモザイクツール - 基本版",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 FANZA同人出版用モザイクツール - 基本版")
st.markdown("---")

st.markdown("### 📋 基本機能テスト版")

uploaded_file = st.file_uploader(
    "画像ファイルを選択してください",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.success("✅ 画像の読み込みに成功しました")
    st.image(image, caption="アップロードされた画像")

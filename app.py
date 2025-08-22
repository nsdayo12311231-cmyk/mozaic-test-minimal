import streamlit as st
import numpy as np
from PIL import Image
import io
import time

st.title("🔒 FANZA同人出版用モザイクツール - 軽量版")
st.markdown("---")

uploaded_files = st.file_uploader(
    "画像ファイルを選択してください（複数選択可能・最大500枚）",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"📁 {len(uploaded_files)}枚の画像が選択されました")
    st.write("🚀 モザイク処理開始ボタンをクリックしてください")

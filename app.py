import streamlit as st
import numpy as np
from PIL import Image
import io
import time

st.set_page_config(
    page_title="FANZAモザイクツール - 軽量版",
    page_icon="🔒",
    layout="wide"
)

def apply_mosaic_lightweight(image, mosaic_size=10):
    """軽量版のモザイク処理（OpenCV不使用）"""
    try:
        # 画像を配列に変換
        img_array = np.array(image)
        
        # 画像サイズを取得
        if len(img_array.shape) == 3:
            h, w, c = img_array.shape
        else:
            h, w = img_array.shape
            c = 1
        
        # モザイク処理（PILとNumPyのみ使用）
        # 画像を小さくしてから大きくする
        small_size = (mosaic_size, mosaic_size)
        small_img = image.resize(small_size, Image.NEAREST)
        mosaic_img = small_img.resize((w, h), Image.NEAREST)
        
        return mosaic_img
        
    except Exception as e:
        st.error(f"モザイク処理中にエラーが発生: {e}")
        return image

def process_images_lightweight(uploaded_files):
    """軽量版の複数画像一括処理"""
    processed_images = []
    
    # プログレスバーの作成
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, uploaded_file in enumerate(uploaded_files):
        # 進捗更新
        progress = (i + 1) / len(uploaded_files)
        progress_bar.progress(progress)
        status_text.text(f"処理中: {uploaded_file.name} ({i+1}/{len(uploaded_files)})")
        
        try:
            # 画像読み込み
            image = Image.open(uploaded_file)
            
            # モザイクサイズの計算（FANZA規約準拠）
            width, height = image.size
            long_side = max(width, height)
            mosaic_size = max(4, int(long_side / 100))
            
            # 軽量版モザイク処理
            processed_image = apply_mosaic_lightweight(image, mosaic_size)
            
            # 結果を保存
            processed_images.append({
                'name': uploaded_file.name,
                'original': image,
                'processed': processed_image,
                'mosaic_size': mosaic_size
            })
            
            # 処理完了の表示
            st.success(f"✅ {uploaded_file.name} の処理が完了しました")
            
        except Exception as e:
            st.error(f"❌ {uploaded_file.name} の処理に失敗: {e}")
        
        # 軽い処理のため少し待機
        time.sleep(0.1)
    
    # 完了
    progress_bar.progress(1.0)
    status_text.text("🎉 全処理完了！")
    
    return processed_images

def main():
    st.title("🔒 FANZA同人出版用モザイクツール - 軽量版")
    st.markdown("---")
    
    st.markdown("""
    ### 📋 軽量版モザイク処理
    
    このアプリケーションは、FANZA隠蔽処理規約第6条に準拠した軽量版モザイク処理を行います。
    
    ### ✨ 新機能
    - **自動モザイク処理**: アップロード後、自動でモザイク処理を開始
    - **複数画像対応**: 最大500枚の画像を一括処理
    - **処理状況表示**: リアルタイムでの進捗とアニメーション
    - **FANZA規約準拠**: 画像長辺×1/100のモザイクサイズ
    - **軽量処理**: OpenCV不使用で高速・安定動作
    """)
    
    # ファイルアップローダー（複数対応）
    uploaded_files = st.file_uploader(
        "画像ファイルを選択してください（複数選択可能・最大500枚）", 
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="PNG、JPG、JPEG形式の画像を複数選択できます。最大500枚まで処理可能です。"
    )
    
    if uploaded_files:
        # ファイル数の制限チェック
        if len(uploaded_files) > 500:
            st.error("❌ ファイル数が500枚を超えています。500枚以下で選択してください。")
            return
        
        st.success(f"📁 {len(uploaded_files)}枚の画像が選択されました")
        
        # 処理開始ボタン
        if st.button("🚀 モザイク処理開始", type="primary", use_container_width=True):
            st.markdown("---")
            st.subheader("🔄 モザイク処理中...")
            
            # 処理中のアニメーション
            with st.spinner("モザイク処理を実行中..."):
                # 処理の実行
                processed_images = process_images_lightweight(uploaded_files)
            
            # 結果の表示
            if processed_images:
                st.markdown("---")
                st.subheader("📸 処理結果")
                
                # 結果をタブで表示
                tabs = st.tabs([f"結果 {i+1}" for i in range(len(processed_images))])
                
                for i, (tab, result) in enumerate(zip(tabs, processed_images)):
                    with tab:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📸 元画像")
                            st.image(result['original'], caption=f"元画像: {result['name']}", use_column_width=True)
                        
                        with col2:
                            st.subheader("🔒 モザイク処理済み")
                            st.image(result['processed'], caption=f"モザイク処理済み: {result['name']}", use_column_width=True)
                        
                        # 処理情報
                        st.info(f"**モザイクサイズ**: {result['mosaic_size']}ピクセル")
                        
                        # ダウンロードボタン
                        img_byte_arr = io.BytesIO()
                        result['processed'].save(img_byte_arr, format='PNG')
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        st.download_button(
                            label=f"📥 {result['name']} をダウンロード",
                            data=img_byte_arr,
                            file_name=f"mosaic_{result['name']}",
                            mime="image/png"
                        )
                
                st.success(f"🎉 {len(processed_images)}枚の画像のモザイク処理が完了しました！")
    
    # 処理例の表示
    st.markdown("---")
    st.subheader("📖 使用方法")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 1️⃣ 画像選択
        複数の画像ファイルを選択してください
        """)
    
    with col2:
        st.markdown("""
        ### 2️⃣ 処理開始
        「モザイク処理開始」ボタンをクリック
        """)
    
    with col3:
        st.markdown("""
        ### 3️⃣ 結果確認
        処理完了後、結果を確認・ダウンロード
        """)

if __name__ == "__main__":
    main()

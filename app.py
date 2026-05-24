import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Đối soát bằng CCCD/ĐDCN", layout="wide")
st.title("⚖️ Công cụ đối soát bằng Mã định danh")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Tải DS 1", type=["xlsx"])
with col2:
    file2 = st.file_uploader("Tải DS 2", type=["xlsx"])

def get_cccd_col(df):
    # 1. Ưu tiên tìm theo TÊN CỘT (Nhãn)
    keywords = ['cccd', 'cmnd', 'định danh', 'dinhdanh', 'ddcn', 'mã định danh']
    for col in df.columns:
        col_name = str(col).lower()
        if any(kw in col_name for kw in keywords):
            return col
    
    # 2. Nếu không tìm thấy nhãn, mới quét dữ liệu 12 số
    for col in df.columns:
        sample = df[col].astype(str).str.replace('.0', '', regex=False)
        if sample.str.match(r'^\d{12}$').any():
            return col
    return None

if file1 and file2:
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        c1 = get_cccd_col(df1)
        c2 = get_cccd_col(df2)
        
        if not c1 or not c2:
            st.error("❌ Không tìm thấy cột nào chứa CCCD/ĐDCN (theo nhãn hoặc dữ liệu 12 số)!")
            st.write("Các cột hiện có trong DS1:", df1.columns.tolist())
            st.write("Các cột hiện có trong DS2:", df2.columns.tolist())
            st.stop()
            
        # Làm sạch và so sánh
        df1['key'] = df1[c1].astype(str).str.replace('.0', '', regex=False).str.strip()
        df2['key'] = df2[c2].astype(str).str.replace('.0', '', regex=False).str.strip()
        
        thieu2 = df1[~df1['key'].isin(df2['key'])]
        thieu1 = df2[~df2['key'].isin(df1['key'])]
        
        st.success("✅ Đối soát thành công!")
        st.metric("Thiếu ở DS2", len(thieu2))
        st.metric("Thiếu ở DS1", len(thieu1))
        
        # Xuất file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            thieu2.to_excel(writer, index=False, sheet_name='Thieu_trong_DS2')
            thieu1.to_excel(writer, index=False, sheet_name='Thieu_trong_DS1')
        st.download_button("📥 Tải kết quả", data=buffer, file_name="Ket_qua.xlsx")
            
    except Exception as e:
        st.error(f"Lỗi: {e}")

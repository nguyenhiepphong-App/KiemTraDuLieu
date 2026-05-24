import streamlit as st
import pandas as pd
import io
import re

st.title("⚖️ Công cụ đối soát CCCD (Chế độ Phẫu thuật Dữ liệu)")

f1 = st.file_uploader("DS 1", type=["xlsx"], key="f1")
f2 = st.file_uploader("DS 2", type=["xlsx"], key="f2")

def get_id_col(df):
    for col in df.columns:
        if any(k in str(col).lower() for k in ['định danh', 'cccd', 'cmnd']):
            return col
    return None

def clean_data(val):
    # CHUYỂN MỌI THỨ VỀ DẠNG CHUỖI
    s = str(val)
    # LẤY RA CHỈ CÁC CON SỐ, LOẠI BỎ MỌI THỨ KHÁC (DẤU CÁCH, KÝ TỰ ẨN, CHỮ CÁI)
    numbers = re.findall(r'\d+', s)
    # GHÉP LẠI
    return "".join(numbers)

if f1 and f2:
    df1 = pd.read_excel(f1)
    df2 = pd.read_excel(f2)
    
    c1, c2 = get_id_col(df1), get_id_col(df2)
    
    # Ép kiểu và làm sạch triệt để
    df1['clean_id'] = df1[c1].apply(clean_data)
    df2['clean_id'] = df2[c2].apply(clean_data)
    
    # CHUYỂN TẤT CẢ VỀ DẠNG CHUỖI ĐỂ TRÁNH LỖI SO SÁNH
    ids1 = set(df1['clean_id'].astype(str).tolist())
    ids2 = set(df2['clean_id'].astype(str).tolist())
    
    # Tìm thiếu
    missing_in_ds2 = [x for x in ids1 if x not in ids2 and x != '']
    missing_in_ds1 = [x for x in ids2 if x not in ids1 and x != '']
    
    st.write(f"Số em thiếu trong DS2: {len(missing_in_ds2)}")
    st.write(f"Số em thiếu trong DS1: {len(missing_in_ds1)}")
    
    # Hiển thị để ông soi
    if missing_in_ds2:
        st.write("Các mã bị báo thiếu trong DS2 (kiểm tra lại kỹ mã này trong file Excel gốc):")
        st.write(missing_in_ds2)

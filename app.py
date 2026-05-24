import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Đối soát danh sách", layout="wide")
st.title("⚖️ Công cụ đối soát dữ liệu (Xử lý định dạng ngày tháng)")

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Tải DS 1", type=["xlsx"])
with col2:
    file2 = st.file_uploader("Tải DS 2", type=["xlsx"])

def standardize_date(df, col_idx):
    """Ép kiểu cột ngày tháng về dạng chuỗi dd/mm/yyyy"""
    col_name = df.columns[col_idx]
    # Chuyển sang dạng datetime trước để loại bỏ sự khác biệt text/number
    # errors='coerce' sẽ biến các giá trị không phải ngày tháng thành NaT
    df[col_name] = pd.to_datetime(df[col_name], errors='coerce', dayfirst=True)
    # Chuyển về dạng chuỗi dd/mm/yyyy
    return df[col_name].dt.strftime('%d/%m/%Y')

if file1 and file2:
    try:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        
        # 1. Chuẩn hóa Họ tên (index 1)
        ten1 = df1.columns[1]
        ten2 = df2.columns[1]
        df1['clean_name'] = df1[ten1].astype(str).str.strip().str.lower()
        df2['clean_name'] = df2[ten2].astype(str).str.strip().str.lower()
        
        # 2. Chuẩn hóa Ngày sinh (index 2) - Dùng hàm xử lý mạnh
        df1['clean_date'] = standardize_date(df1, 2)
        df2['clean_date'] = standardize_date(df2, 2)
        
        # 3. Đối chiếu
        # Tạo khóa so sánh
        df1['key'] = df1['clean_name'] + "_" + df1['clean_date']
        df2['key'] = df2['clean_name'] + "_" + df2['clean_date']
        
        thieu_ds2 = df1[~df1['key'].isin(df2['key'])]
        thieu_ds1 = df2[~df2['key'].isin(df1['key'])]
        
        st.success(f"✅ Đã đối soát xong!")
        st.write(f"Số HS có ở DS1 nhưng thiếu trong DS2: **{len(thieu_ds2)}**")
        st.write(f"Số HS có ở DS2 nhưng thiếu trong DS1: **{len(thieu_ds1)}**")
        
        # Xuất file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            thieu_ds2.to_excel(writer, index=False, sheet_name='Thieu_trong_DS2')
            thieu_ds1.to_excel(writer, index=False, sheet_name='Thieu_trong_DS1')
        
        st.download_button("📥 Tải kết quả", data=buffer, file_name="Ket_qua_chuan_hoa.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
    except Exception as e:
        st.error(f"Lỗi: {e}. Hãy kiểm tra xem file có đúng cột thứ 2 là Ngày sinh không.")

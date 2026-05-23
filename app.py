import streamlit as st
import pandas as pd

st.title("🛡️ Kiểm tra dữ liệu & Xét lên lớp")
uploaded_file = st.file_uploader("Tải file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # 1. Định nghĩa các nhóm cột
    cols_mon_hoc = ["Toán", "Vật lí", "Hóa học", "Sinh học", "Tin học", "Ngữ Văn", "Lịch sử", "Địa lí", "Ngoại ngữ 1", "Công nghệ", "GDQP-AN", "Ngoại ngữ 2", "Toán Pháp", "Hoạt động trải nghiệm", "Giáo dục thể chất"]
    col_ngay_nghi = "Tổng số ngày nghỉ"
    
    bao_cao = []
    
    for idx, row in df.iterrows():
        vi_pham = []
        
        # 2. Kiểm tra lỗi môn học (Chỉ quét các cột môn học)
        for m in cols_mon_hoc:
            if m in df.columns and pd.notna(row.get(m)):
                val = row.get(m)
                # Chỉ kiểm tra nếu là số và < 5.0
                if isinstance(val, (int, float)) and val < 5.0:
                    vi_pham.append(f"{m}({val})<5.0")
        
        # 3. Kiểm tra riêng ngày nghỉ (Chỉ báo lỗi khi > 45)
        if col_ngay_nghi in df.columns and pd.notna(row.get(col_ngay_nghi)):
            nghi = row.get(col_ngay_nghi)
            if isinstance(nghi, (int, float)) and nghi > 45:
                vi_pham.append(f"Nghỉ quá 45 buổi ({nghi})")
        
        # 4. Đối soát dấu X
        co_tick = str(row.get("Được lên lớp", "")).strip().upper() == 'X'
        
        # Lọc dữ liệu: Chỉ báo lỗi khi có vi phạm thực sự
        if vi_pham and co_tick:
            bao_cao.append({"Lớp": row["Mã lớp"], "Họ tên": row["Họ tên"], "Lý do": ", ".join(vi_pham)})
        elif not vi_pham and not co_tick and row.get("Được lên lớp") is not None:
             # Trường hợp này là đủ điều kiện nhưng chưa tích X
             pass 

    if bao_cao:
        st.table(pd.DataFrame(bao_cao))
    else:
        st.success("✅ Không tìm thấy học sinh nào vi phạm.")

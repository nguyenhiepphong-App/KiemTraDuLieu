import streamlit as st
import pandas as pd

st.title("🛡️ Kiểm tra lý do không đủ điều kiện lên lớp")
uploaded_file = st.file_uploader("Tải file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    all_subjects = ["Toán", "Vật lí", "Hóa học", "Sinh học", "Tin học", "Ngữ Văn", "Lịch sử", "Địa lí", "Ngoại ngữ 1", "Công nghệ", "GDQP-AN", "Ngoại ngữ 2", "Toán Pháp", "Hoạt động trải nghiệm", "Giáo dục thể chất"]
    cols_nhan_xet = ["Hoạt động trải nghiệm", "Giáo dục thể chất"]
    
    bao_cao = []
    
    for idx, row in df.iterrows():
        # Kiểm tra tiêu chuẩn Thông tư 22
        ly_do_truot = []
        
        # 1. Kiểm tra điểm môn học
        for col in all_subjects:
            if col in df.columns and pd.notna(row.get(col)):
                val = row.get(col)
                if col not in cols_nhan_xet and isinstance(val, (int, float)) and val < 5.0:
                    ly_do_truot.append(f"{col}<5.0")
                if col in cols_nhan_xet and str(val).strip().upper() == 'CĐ':
                    ly_do_truot.append(f"{col}:CĐ")
        
        # Kiểm tra xem có dấu X không
        co_tick = str(row.get("Được lên lớp", "")).strip().upper() == 'X'
        
        # CHỈ GHI NHẬN KHI: Đã đủ dữ liệu (không thiếu môn) MÀ VẪN KHÔNG LÊN LỚP
        # Hoặc: Đã tích X nhưng thực tế lại vi phạm
        if ly_do_truot and co_tick:
            bao_cao.append({"Họ tên": row.get("Họ tên"), "Lý do không đạt": ", ".join(ly_do_truot), "Tình trạng": "Cần xóa X"})
        elif ly_do_truot and not co_tick:
            bao_cao.append({"Họ tên": row.get("Họ tên"), "Lý do không đạt": ", ".join(ly_do_truot), "Tình trạng": "Chính xác (Không lên lớp)"})

    if bao_cao:
        st.table(pd.DataFrame(bao_cao))
    else:
        st.success("✅ Không phát hiện học sinh nào vi phạm tiêu chuẩn Thông tư 22.")

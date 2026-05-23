import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Kiểm tra lên lớp", layout="wide")
st.title("🛡️ App Kiểm tra dữ liệu & Xét lên lớp")

uploaded_file = st.file_uploader("Tải file Excel kết quả học tập", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # Xác định cột môn học (Giả sử từ cột thứ 6: Toán, Vật lí, Hóa học...)
    # Ông có thể điều chỉnh chỉ số [5:] tùy theo vị trí thực tế trên file
    cols_mon = df.columns[5:] 
    
    errors = []
    
    for idx, row in df.iterrows():
        ly_do = []
        
        # 1. Kiểm tra điểm môn học (< 5.0)
        for mon in cols_mon:
            if mon == "Danh hiệu cả năm": continue # Bỏ qua cột này
            if pd.notna(row[mon]) and isinstance(row[mon], (int, float)) and row[mon] < 5.0:
                ly_do.append(f"Môn {mon} ({row[mon]}) < 5.0")
        
        # 2. Kiểm tra các điều kiện khác (Nếu có trong file của ông)
        # Giả sử file có cột 'Kết quả rèn luyện'
        if 'Kết quả rèn luyện' in df.columns and row['Kết quả rèn luyện'] == 'Chưa đạt':
            ly_do.append("Rèn luyện: Chưa đạt")

        # 3. Xét logic lên lớp
        # Cột 'Được lên lớp' giả định chứa dấu 'x' hoặc 'X'
        co_tick = str(row.get("Được lên lớp", "")).strip().upper() == 'X'
        
        if not co_tick and not ly_do:
            errors.append({"Dòng": idx+2, "Họ tên": row["Họ tên"], "Lỗi": "Thiếu dấu X (Không rõ lý do)"})
        elif not co_tick and ly_do:
            errors.append({"Dòng": idx+2, "Họ tên": row["Họ tên"], "Lỗi": f"Chưa đạt: {'; '.join(ly_do)}"})
        elif co_tick and ly_do:
            errors.append({"Dòng": idx+2, "Họ tên": row["Họ tên"], "Lỗi": f"Cần xem lại: Có dấu X nhưng vi phạm: {'; '.join(ly_do)}"})

    # Hiển thị và Xuất kết quả
    if errors:
        err_df = pd.DataFrame(errors)
        st.warning(f"Phát hiện {len(errors)} trường hợp bất thường!")
        st.table(err_df)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            err_df.to_excel(writer, index=False, sheet_name="BaoCao")
        st.download_button("📥 Tải file báo cáo lỗi (.xlsx)", data=output.getvalue(), file_name="Bao_cao_xet_len_lop.xlsx")
    else:
        st.success("✅ Dữ liệu hoàn toàn hợp lệ!")

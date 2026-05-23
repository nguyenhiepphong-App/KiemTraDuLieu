import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trợ lý giáo vụ", layout="wide")
st.title("🛡️ Trợ lý giáo vụ: Kiểm tra dữ liệu & Xét lên lớp")

uploaded_file = st.file_uploader("Tải file Excel (kết quả học tập)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # 1. DANH SÁCH CÁC MÔN HỌC (Ông sửa tên cho khớp với file Excel của ông)
    all_subjects = ["Toán", "Vật lí", "Hóa học", "Sinh học", "Tin học", "Ngữ Văn", "Lịch sử", "Địa lí", "Ngoại ngữ 1", "Công nghệ", "GDQP-AN", "Ngoại ngữ 2", "Toán Pháp", "Hoạt động trải nghiệm", "Giáo dục thể chất"]
    cols_nhan_xet = ["Hoạt động trải nghiệm", "Giáo dục thể chất"]
    
    errors = []
    
    # 2. XỬ LÝ THEO LỚP
    for lop, group in df.groupby("Mã lớp"):
        for idx, row in group.iterrows():
            ly_do_bui = [] # Lưu ý: "bui" = bất thường & lỗi
            
            # Kiểm tra tính đồng nhất (So sánh với các bạn trong lớp)
            for col in all_subjects:
                if col in df.columns:
                    # Nếu > 50% lớp có dữ liệu mà hs này trống -> Bất thường
                    if group[col].notna().sum() > len(group) * 0.5 and pd.isna(row.get(col)):
                        ly_do_bui.append(f"Thiếu dữ liệu môn '{col}'")
            
            # Kiểm tra tiêu chuẩn lên lớp (Thông tư 22)
            for col in all_subjects:
                if col in df.columns and pd.notna(row.get(col)):
                    val = row.get(col)
                    # Môn điểm số (< 5.0)
                    if col not in cols_nhan_xet and isinstance(val, (int, float)) and val < 5.0:
                        ly_do_bui.append(f"Môn {col} ({val}) < 5.0")
                    # Môn nhận xét (Chưa đạt)
                    if col in cols_nhan_xet and str(val).strip().upper() == 'CĐ':
                        ly_do_bui.append(f"Môn {col} bị CĐ")
            
            # 3. Đối soát dấu X
            co_tick = str(row.get("Được lên lớp", "")).strip().upper() == 'X'
            
            if not co_tick:
                if not ly_do_bui:
                    errors.append({"Lớp": lop, "Họ tên": row.get("Họ tên"), "Gợi ý": "Đủ điều kiện nhưng thiếu dấu X"})
                else:
                    errors.append({"Lớp": lop, "Họ tên": row.get("Họ tên"), "Gợi ý": f"Chưa đạt: {', '.join(ly_do_bui)}"})
            elif co_tick and ly_do_bui:
                errors.append({"Lớp": lop, "Họ tên": row.get("Họ tên"), "Gợi ý": f"Cần xem lại: Có X nhưng vi phạm: {', '.join(ly_do_bui)}"})

    # 4. HIỂN THỊ KẾT QUẢ
    if errors:
        st.warning(f"Phát hiện {len(errors)} trường hợp cần kiểm tra!")
        st.table(pd.DataFrame(errors))
    else:
        st.success("✅ Dữ liệu lớp đồng nhất và hợp lệ!")

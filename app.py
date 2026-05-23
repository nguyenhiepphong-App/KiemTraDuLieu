import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Trợ lý giáo vụ", layout="wide")
st.title("🛡️ Kiểm tra dữ liệu & Xét lên lớp")
uploaded_file = st.file_uploader("Tải file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    cols_mon_hoc = ["Toán", "Vật lí", "Hóa học", "Sinh học", "Tin học", "Ngữ Văn", "Lịch sử", "Địa lí", "Ngoại ngữ 1", "Công nghệ", "GDQP-AN", "Ngoại ngữ 2", "Toán Pháp", "Hoạt động trải nghiệm", "Giáo dục thể chất"]
    cols_nhan_xet = ["Hoạt động trải nghiệm", "Giáo dục thể chất"]
    col_ngay_nghi = "Tổng số ngày nghỉ"
    
    ds_thieu = []
    ds_khong_len_lop = []
    
    for lop, group in df.groupby("Mã lớp"):
        for idx, row in group.iterrows():
            # 1. Sheet 1: DS thiếu dữ liệu (So sánh cùng lớp)
            thieu = [m for m in cols_mon_hoc if m in df.columns and group[m].notna().sum() > len(group) * 0.5 and pd.isna(row.get(m))]
            if thieu:
                ds_thieu.append({"Lớp": lop, "Họ tên": row.get("Họ tên"), "Môn thiếu": ", ".join(thieu)})
            
            # 2. Sheet 2: DS không lên lớp + Gợi ý nguyên nhân
            co_tick = str(row.get("Được lên lớp", "")).strip().upper() == 'X'
            if not co_tick:
                nguyen_nhan = []
                # Check ngày nghỉ
                nghi = row.get(col_ngay_nghi, 0)
                if pd.notna(nghi) and isinstance(nghi, (int, float)) and nghi > 45:
                    nguyen_nhan.append(f"Nghỉ ({nghi}) > 45 buổi")
                # Check điểm số
                for m in cols_mon_hoc:
                    val = row.get(m)
                    if pd.notna(val):
                        if m not in cols_nhan_xet and isinstance(val, (int, float)) and val < 5.0:
                            nguyen_nhan.append(f"{m}({val})<5.0")
                        elif m in cols_nhan_xet and str(val).strip().upper() == 'CĐ':
                            nguyen_nhan.append(f"{m}:CĐ")
                
                # Chỉ đưa vào danh sách nếu có nguyên nhân (hoặc thiếu dữ liệu)
                if nguyen_nhan:
                    ds_khong_len_lop.append({"Lớp": lop, "Họ tên": row.get("Họ tên"), "Gợi ý nguyên nhân": ", ".join(nguyen_nhan)})

    # Xuất file
    if ds_thieu or ds_khong_len_lop:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            pd.DataFrame(ds_thieu).to_excel(writer, index=False, sheet_name='DS_thieu_du_lieu')
            pd.DataFrame(ds_khong_len_lop).to_excel(writer, index=False, sheet_name='DS_khong_len_lop')
            
        st.download_button("📥 Tải kết quả (2 sheets)", data=buffer, file_name="Ket_qua_kiem_tra.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.success("✅ Dữ liệu hoàn hảo!")

st.markdown("---")
st.markdown("Người thực hiện: **Nguyen Hiep Phong - THPT Bến Tre**")

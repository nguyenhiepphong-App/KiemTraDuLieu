import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Trợ lý giáo vụ", layout="wide")
st.title("🛡️ Kiểm tra: Sót dữ liệu & Xét lên lớp")

uploaded_file = st.file_uploader("Tải file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    info_cols = ["Mã lớp", "Họ tên", "Được lên lớp", "Danh hiệu cả năm", "Tổng số ngày nghỉ"]
    all_subjects = [c for c in df.columns if c not in info_cols]
    cols_nhan_xet = ["Hoạt động trải nghiệm", "Giáo dục thể chất"]
    
    # 2 danh sách riêng biệt
    ds_thieu_du_lieu = []
    ds_khong_len_lop = []
    
    for lop, group in df.groupby("Mã lớp"):
        for idx, row in group.iterrows():
            # 1. Check thiếu dữ liệu
            thieu = [col for col in all_subjects if group[col].notna().sum() > len(group) * 0.5 and pd.isna(row.get(col))]
            if thieu:
                ds_thieu_du_lieu.append({"Lớp": lop, "Họ tên": row.get("Họ tên"), "Môn thiếu": ", ".join(thieu)})
            
            # 2. Check không được lên lớp
            co_tick = str(row.get("Được lên lớp", "")).strip().upper() == 'X'
            if not co_tick:
                vi_pham = []
                nghi_hoc = row.get("Tổng số ngày nghỉ", 0)
                if pd.notna(nghi_hoc) and isinstance(nghi_hoc, (int, float)) and nghi_hoc > 45:
                    vi_pham.append(f"Nghỉ ({nghi_hoc}) > 45")
                for col in all_subjects:
                    val = row.get(col)
                    if pd.notna(val):
                        if col not in cols_nhan_xet and isinstance(val, (int, float)) and val < 5.0:
                            vi_pham.append(f"{col}({val})<5.0")
                        elif col in cols_nhan_xet and str(val).strip().upper() == 'CĐ':
                            vi_pham.append(f"{col}:CĐ")
                
                if vi_pham:
                    ds_khong_len_lop.append({"Lớp": lop, "Họ tên": row.get("Họ tên"), "Lý do": ", ".join(vi_pham)})
                else:
                    ds_khong_len_lop.append({"Lớp": lop, "Họ tên": row.get("Họ tên"), "Lý do": "Đủ điều kiện nhưng thiếu X"})

    # Hiển thị
    if ds_thieu_du_lieu or ds_khong_len_lop:
        st.warning("⚠️ Đã phát hiện bất thường!")
        
        # Tạo file Excel 2 sheet
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            pd.DataFrame(ds_thieu_du_lieu).to_excel(writer, index=False, sheet_name='DS_thieu_du_lieu')
            pd.DataFrame(ds_khong_len_lop).to_excel(writer, index=False, sheet_name='DS_khong_len_lop')
            
        st.download_button("📥 Tải file kết quả (2 sheets)", data=buffer, file_name="Ket_qua_kiem_tra.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.success("✅ Dữ liệu hoàn hảo!")

st.markdown("---")
st.markdown("Người thực hiện: **Nguyen Hiep Phong - THPT Bến Tre**")

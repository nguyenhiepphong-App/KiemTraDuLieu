import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trợ lý giáo vụ", layout="wide")
st.title("🛡️ Kiểm tra: Sót dữ liệu & Xét lên lớp")

uploaded_file = st.file_uploader("Tải file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Các cột không phải môn học
    info_cols = ["Mã lớp", "Họ tên", "Được lên lớp", "Danh hiệu cả năm", "Tổng số ngày nghỉ"]
    all_subjects = [c for c in df.columns if c not in info_cols]
    cols_nhan_xet = ["Hoạt động trải nghiệm", "Giáo dục thể chất"]
    
    bao_cao = []
    
    for lop, group in df.groupby("Mã lớp"):
        for idx, row in group.iterrows():
            ly_do_bat_thuong = []
            
            # 1. Kiểm tra thiếu dữ liệu
            for col in all_subjects:
                if group[col].notna().sum() > len(group) * 0.5 and pd.isna(row.get(col)):
                    ly_do_bat_thuong.append(f"Thiếu {col}")
            
            # 2. Xét lên lớp (Thông tư 22)
            co_tick = str(row.get("Được lên lớp", "")).strip().upper() == 'X'
            
            if not co_tick:
                vi_pham = []
                nghi_hoc = row.get("Tổng số ngày nghỉ", 0)
                if pd.notna(nghi_hoc) and isinstance(nghi_hoc, (int, float)) and nghi_hoc > 45:
                    vi_pham.append(f"Nghỉ quá 45 buổi ({nghi_hoc})")
                
                for col in all_subjects:
                    val = row.get(col)
                    if pd.notna(val):
                        if col not in cols_nhan_xet and isinstance(val, (int, float)) and val < 5.0:
                            vi_pham.append(f"{col}({val})<5.0")
                        elif col in cols_nhan_xet and str(val).strip().upper() == 'CĐ':
                            vi_pham.append(f"{col}:CĐ")
                
                if vi_pham:
                    ly_do_bat_thuong.append(f"Lý do chưa đạt: {', '.join(vi_pham)}")
                else:
                    ly_do_bat_thuong.append("Đủ điều kiện nhưng thiếu dấu X")

            if ly_do_bat_thuong:
                bao_cao.append({"Lớp": lop, "Họ tên": row.get("Họ tên"), "Bất thường": "; ".join(ly_do_bat_thuong)})

    if bao_cao:
        df_report = pd.DataFrame(bao_cao)
        st.table(df_report)
        
        # Nút tải file
        csv = df_report.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Tải danh sách lỗi (.csv)", data=csv, file_name="danh_sach_loi.csv", mime="text/csv")
    else:
        st.success("✅ Dữ liệu hoàn hảo!")

# Thông tin cuối giao diện
st.markdown("---")
st.markdown("Người thực hiện: **Nguyen Hiep Phong - THPT Bến Tre**")

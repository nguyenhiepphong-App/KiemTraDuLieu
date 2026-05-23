import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trợ lý giáo vụ", layout="wide")
st.title("🛡️ Kiểm tra bất thường: Dữ liệu & Xét lên lớp")

uploaded_file = st.file_uploader("Tải file Excel kết quả học tập", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Loại trừ các cột không phải môn học
    info_cols = ["Mã lớp", "Họ tên", "Được lên lớp", "Danh hiệu cả năm"]
    all_cols = [c for c in df.columns if c not in info_cols]
    
    bao_cao = []
    
    # Duyệt qua từng lớp
    for lop, group in df.groupby("Mã lớp"):
        for idx, row in group.iterrows():
            ly_do_bat_thuong = []
            
            # --- 1. KIỂM TRA THIẾU DỮ LIỆU (So sánh ngang hàng trong lớp) ---
            for col in all_cols:
                # Nếu quá 50% lớp có dữ liệu mà hs này trống -> Thiếu dữ liệu
                if group[col].notna().sum() > len(group) * 0.5 and pd.isna(row.get(col)):
                    ly_do_bat_thuong.append(f"Thiếu dữ liệu môn {col}")
            
            # --- 2. XÉT LÊN LỚP (Đối soát Thông tư 22) ---
            # Chỉ xét nếu học sinh không có dấu "x"
            co_tick = str(row.get("Được lên lớp", "")).strip().upper() == 'X'
            
            if not co_tick:
                vi_pham_tt22 = []
                for col in all_cols:
                    val = row.get(col)
                    if pd.notna(val):
                        # Môn điểm số (< 5.0)
                        if isinstance(val, (int, float)) and val < 5.0:
                            vi_pham_tt22.append(f"{col}({val})<5.0")
                        # Môn nhận xét (Chưa đạt)
                        elif str(val).strip().upper() == 'CĐ':
                            vi_pham_tt22.append(f"{col}:CĐ")
                
                if vi_pham_tt22:
                    ly_do_bat_thuong.append(f"Lý do chưa lên lớp: {', '.join(vi_pham_tt22)}")
                else:
                    ly_do_bat_thuong.append("Đủ điều kiện nhưng chưa có dấu X")

            # Ghi lại nếu có bất thường
            if ly_do_bat_thuong:
                bao_cao.append({
                    "Lớp": lop,
                    "Họ tên": row.get("Họ tên"),
                    "Bất thường": "; ".join(ly_do_bat_thuong)
                })

    # Hiển thị kết quả
    if bao_cao:
        st.warning(f"Phát hiện {len(bao_cao)} trường hợp bất thường:")
        st.table(pd.DataFrame(bao_cao))
    else:
        st.success("✅ Dữ liệu lớp đồng nhất và kết quả lên lớp hợp lệ!")

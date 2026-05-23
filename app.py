import streamlit as st
import pandas as pd

st.title("🔍 Trợ lý giáo vụ: Quét dữ liệu & Lên lớp")
uploaded_file = st.file_uploader("Tải file Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    cols_mon = ["Toán", "Vật lí", "Hóa học", "Sinh học", "Tin học", "Ngữ Văn", "Lịch sử", "Địa lí", "Ngoại ngữ 1", "Công nghệ", "GDQP-AN", "Ngoại ngữ 2", "Toán Pháp", "Hoạt động trải nghiệm"]
    
    errors = []
    
    for lop, group in df.groupby("Mã lớp"):
        for idx, row in group.iterrows():
            ly_do_thieu = []
            
            # 1. Kiểm tra thiếu môn so với lớp (So sánh ngang hàng)
            for col in cols_mon:
                if col in df.columns and group[col].notna().sum() > len(group) * 0.5:
                    if pd.isna(row[col]):
                        ly_do_thieu.append(f"Thiếu môn '{col}'")
            
            # 2. Kiểm tra tiêu chuẩn lên lớp (Thông tư 22)
            mon_duoi_5 = [m for m in cols_mon if m in df.columns and pd.notna(row[m]) and row[m] < 5.0]
            
            # 3. Đối soát dấu "X"
            co_tick = str(row.get("Được lên lớp", "")).strip().upper() == 'X'
            
            # Gợi ý lý do bất thường
            if not co_tick:
                if not mon_duoi_5 and not ly_do_thieu:
                    errors.append({"Lớp": lop, "Họ tên": row["Họ tên"], "Gợi ý": "Đủ điều kiện nhưng thiếu dấu X"})
                else:
                    ly_do_full = ly_do_thieu + [f"Môn {m}<5.0" for m in mon_duoi_5]
                    errors.append({"Lớp": lop, "Họ tên": row["Họ tên"], "Gợi ý": f"Chưa đạt: {', '.join(ly_do_full)}"})
            elif co_tick and (mon_duoi_5 or ly_do_thieu):
                errors.append({"Lớp": lop, "Họ tên": row["Họ tên"], "Gợi ý": "Có dấu X nhưng dữ liệu chưa đạt chuẩn"})

    if errors:
        st.table(pd.DataFrame(errors))
    else:
        st.success("✅ Dữ liệu hoàn hảo!")

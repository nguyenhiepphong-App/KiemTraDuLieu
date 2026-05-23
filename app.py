import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Kiểm tra dữ liệu", layout="wide")
st.title("🛡️ App Kiểm tra dữ liệu bất thường")

uploaded_file = st.file_uploader("Tải file Excel (.xlsx) tại đây", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    # Cột môn bắt đầu từ cột thứ 6 trở đi (theo cấu trúc ảnh ông đã gửi)
    cols_mon = df.columns[5:] 

    errors = []
    for lop, group in df.groupby("Mã lớp"):
        # Môn chung: môn mà trên 50% lớp có điểm
        mon_chung = [col for col in cols_mon if group[col].notna().sum() > len(group) * 0.5]

        for idx, row in group.iterrows():
            for mon in mon_chung:
                if pd.isna(row[mon]):
                    errors.append({"Dòng": idx+2, "Lớp": lop, "Học sinh": row["Họ tên"], "Lỗi": f"Thiếu điểm {mon}"})

    if errors:
        err_df = pd.DataFrame(errors)
        st.warning(f"Tìm thấy {len(errors)} bất thường!")
        st.table(err_df)

        # Xuất file kết quả
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            err_df.to_excel(writer, index=False, sheet_name="BaoCaoLoi")
        st.download_button("📥 Tải báo cáo lỗi (.xlsx)", data=output.getvalue(), file_name="Bao_cao_loi.xlsx")
    else:
        st.success("✅ Dữ liệu hoàn toàn đồng nhất!")

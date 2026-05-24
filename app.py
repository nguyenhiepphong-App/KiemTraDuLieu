import streamlit as st
import pandas as pd
import io
import re

st.title("⚖️ Công cụ đối soát CCCD (Chế độ lọc sạch tuyệt đối)")

def clean_id_hardcore(val):
    """Loại bỏ mọi thứ trừ chữ số, chỉ lấy chuỗi số"""
    s = str(val)
    # Dùng Regex lấy ra đúng các ký tự số, bỏ qua mọi dấu cách, dấu chấm, dấu phẩy, ký tự ẩn
    numbers = re.findall(r'\d+', s)
    # Ghép lại thành 1 chuỗi số
    return "".join(numbers)

# ... (Phần tải file giữ nguyên)

# Khi xử lý:
df1['clean_id'] = df1[c1].apply(clean_id_hardcore)
df2['clean_id'] = df2[c2].apply(clean_id_hardcore)

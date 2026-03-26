import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Hệ thống Chọn Thiết Bị Riken", page_icon="⚙️", layout="wide")

# ==========================================
# 1. HỆ THỐNG ĐỌC DỮ LIỆU THÔNG MINH (CÓ NÚT UPLOAD)
# ==========================================
file_path = "riken_database.xlsx"

# Tạo nút Upload file ở thanh Sidebar bên trái
with st.sidebar:
    st.markdown("### 📂 Cập nhật Dữ liệu Hãng")
    st.markdown("Nếu hệ thống chưa có dữ liệu, hãy tải file Excel `riken_database.xlsx` lên đây:")
    uploaded_file = st.file_uploader("Chọn file Excel", type=["xlsx", "xls"])

@st.cache_data
def load_data(file_upload):
    # Ưu tiên 1: Đọc file người dùng vừa upload trực tiếp trên web
    if file_upload is not None:
        return pd.read_excel(file_upload).fillna("N/A"), True
        
    # Ưu tiên 2: Đọc file có sẵn trong kho GitHub
    elif os.path.exists(file_path):
        return pd.read_excel(file_path).fillna("N/A"), True
        
    # Nếu không có cả 2 -> Dùng dữ liệu mẫu
    else:
        data = {
            "Detection Gas": ["Hydrogen sulfide", "Carbon monoxide", "Methane", "Ammonia"],
            "Remarks": ["", "For steel plant", "General purpose", "Toxics"],
            "Gas Cymbol": ["H2S", "CO", "CH4", "NH3"],
            "CAS Number": ["7783-06-4", "630-08-0", "74-82-8", "7664-41-7"],
            "Chemical Formula": ["H2S", "CO", "CH4", "NH3"],
            "Principle": ["Electrochemical", "Electrochemical", "Catalytic Combustion", "Electrochemical"],
            "Sensor": ["ES-1821", "ES-1827", "NC-6264A", "ES-18"],
            "Portable/Fixed": ["Portable", "Fixed", "Portable", "Fixed"],
            "Detector": ["GX-3R", "SD-3", "RX-8000", "GD-70D"],
            "Measuring Rang": ["0-30 ppm", "0-500 ppm", "0-100% LEL", "0-75 ppm"]
        }
        return pd.DataFrame(data).fillna("N/A"), False

# Gọi hàm tải dữ liệu
df, is_real_data = load_data(uploaded_file)

# Hiển thị cảnh báo nếu vẫn dùng dữ liệu mẫu
if not is_real_data:
    st.warning("⚠️ Đang hiển thị dữ liệu mẫu. Vui lòng sử dụng cột bên trái để tải file Excel 'riken_database.xlsx' lên hệ thống.")

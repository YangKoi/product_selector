import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Hệ thống Chọn Thiết Bị Riken", page_icon="⚙️", layout="wide")

# ==========================================
# 1. ĐỌC FILE EXCEL GỐC CỦA RIKEN KEIKI
# ==========================================
file_path = "riken_database.xlsx"

# Dùng cache để web load cực nhanh, không phải đọc lại file Excel mỗi lần bấm nút
@st.cache_data
def load_data():
    if os.path.exists(file_path):
        # Đọc trực tiếp file Excel của sếp
        df = pd.read_excel(file_path)
    else:
        st.warning("⚠️ Chưa tìm thấy file 'riken_database.xlsx'. Đang hiển thị dữ liệu mẫu để test giao diện.")
        # Dữ liệu mẫu mô phỏng đúng các cột trong ảnh của sếp
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
        df = pd.DataFrame(data)
    
    # Xử lý các ô trống trong Excel để code không bị lỗi
    return df.fillna("N/A")

df = load_data()

# ==========================================
# 2. GIAO DIỆN TÌM KIẾM
# ==========================================
st.title("🎯 Công Cụ Chọn Thiết Bị (Dữ liệu gốc Riken Keiki)")
st.markdown("Tra cứu cấu hình thiết bị dựa trên danh mục chuẩn của hãng.")
st.markdown("---")

with st.container(border=True):
    st.subheader("⚙️ Bộ Lọc Thông Số")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Lọc theo kiểu máy (Lấy từ cột Portable/Fixed)
        loai_may_list = ["Tất cả"] + list(df["Portable/Fixed"].unique())
        chon_loai = st.selectbox("1. Kiểu lắp đặt (Portable/Fixed):", loai_may_list)
        
    with col2:
        # Lọc theo nguyên lý đo (Lấy từ cột Principle)
        principle_list = ["Tất cả"] + list(df["Principle"].unique())
        chon_nguyen_ly = st.selectbox("2. Nguyên lý cảm biến (Principle):", principle_list)

    with col3:
        # Ô nhập tự do: Có thể tìm tên khí, công thức hóa học, hoặc mã model
        tu_khoa = st.text_input("3. Tên khí / Công thức / Model:", placeholder="VD: H2S, Carbon, GX-3R...")

# ==========================================
# 3. THUẬT TOÁN LỌC
# ==========================================
filtered_df = df.copy()

if chon_loai != "Tất cả":
    filtered_df = filtered_df[filtered_df["Portable/Fixed"] == chon_loai]

if chon_nguyen_ly != "Tất cả":
    filtered_df = filtered_df[filtered_df["Principle"] == chon_nguyen_ly]

if tu_khoa:
    # Tìm kiếm bao trùm nhiều cột cùng lúc (Tên khí, Công thức, Symbol, Model)
    mask = filtered_df.apply(lambda row: row.astype(str).str.contains(tu_khoa, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# ==========================================
# 4. HIỂN THỊ KẾT QUẢ
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader(f"✅ TÌM THẤY {len(filtered_df)} KẾT QUẢ")

if not filtered_df.empty:
    cols = st.columns(3) 
    for index, row in filtered_df.reset_index().iterrows():
        with cols[index % 3]:
            with st.container(border=True):
                st.markdown(f"<h3 style='text-align: center; color: #d10000;'>{row['Detector']}</h3>", unsafe_allow_html=True)
                st.markdown(f"**🔹 Kiểu máy:** {row['Portable/Fixed']}")
                st.markdown(f"**🧪 Loại khí:** {row['Detection Gas']} ({row['Chemical Formula']})")
                st.markdown(f"**📏 Dải đo:** {row['Measuring Rang']}")
                st.markdown(f"**🔬 Nguyên lý:** {row['Principle']}")
                st.markdown(f"**🔌 Cảm biến:** {row['Sensor']}")
                
                if row['Remarks'] and row['Remarks'] != "N/A":
                    st.info(f"💡 Lưu ý: {row['Remarks']}")
                
                # Nút tìm Catalog tự động
                search_link = f"https://www.google.com/search?q={row['Detector']}+Riken+Keiki+datasheet+pdf"
                st.link_button(f"📥 Tìm Catalog {row['Detector']}", search_link, use_container_width=True)
else:
    st.error("⚠️ Không tìm thấy thiết bị phù hợp. Hãy thử rút ngắn từ khóa (VD: thay vì gõ 'Hydrogen sulfide' hãy gõ 'H2S').")

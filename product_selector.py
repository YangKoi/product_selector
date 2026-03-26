import streamlit as st
import pandas as pd

st.set_page_config(page_title="Công cụ Chọn Thiết Bị Riken", page_icon="⚙️", layout="wide")

# ==========================================
# 1. DATABASE THIẾT BỊ (Mô phỏng các dòng Riken Keiki)
# ==========================================
data = {
    "Model": ["GX-3R", "RX-8000", "SD-3", "GD-70D", "GW-3"],
    "Loại máy": ["Cầm tay (Portable)", "Cầm tay (Portable)", "Cố định (Fixed)", "Cố định (Fixed)", "Cầm tay (Portable)"],
    "Kiểu lấy mẫu": ["Khuếch tán (Diffusion)", "Hút bơm (Pump)", "Khuếch tán (Diffusion)", "Hút bơm (Pump)", "Khuếch tán (Diffusion)"],
    "Khí đo được": ["LEL, O2, H2S, CO", "HC, O2, H2S, CO", "LEL, Toxics, O2", "Toxics, VOCs", "O2, CO, H2S (Đơn khí)"],
    "Môi trường / Chứng chỉ": ["ATEX, IECEx", "ATEX, MED", "ATEX, IECEx, SIL2", "Phòng sạch (Cleanroom)", "ATEX, IECEx"],
    "Tính năng nổi bật": ["Nhỏ nhẹ nhất thế giới", "Đo được nồng độ cao (100% vol)", "Thiết kế thông minh, SIL 2", "Độ chính xác cực cao cho bán dẫn", "Đeo cổ tay, kẹp áo nhỏ gọn"],
    "Hình ảnh": ["https://www.rikenkeiki.co.jp/english/products/img/gx-3r.jpg", 
                 "https://www.rikenkeiki.co.jp/english/products/img/rx-8000.jpg",
                 "https://www.rikenkeiki.co.jp/english/products/img/sd-3.jpg",
                 "https://www.rikenkeiki.co.jp/english/products/img/gd-70d.jpg",
                 "https://www.rikenkeiki.co.jp/english/products/img/gw-3.jpg"]
}
df = pd.DataFrame(data)

# ==========================================
# 2. GIAO DIỆN CÔNG CỤ TÌM KIẾM
# ==========================================
st.title("🎯 Hệ thống Cấu hình & Lựa chọn Thiết bị")
st.markdown("Vui lòng chọn các thông số kỹ thuật theo yêu cầu thực tế của dự án. Hệ thống sẽ lọc ra các thiết bị phù hợp nhất.")
st.markdown("---")

# Tạo thanh công cụ lọc (Filter Sidebar/Top bar)
with st.container(border=True):
    st.subheader("⚙️ Thông số đầu vào")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Lọc Loại máy
        loai_may_list = ["Tất cả"] + list(df["Loại máy"].unique())
        chon_loai = st.selectbox("1. Kiểu lắp đặt:", loai_may_list)
        
    with col2:
        # Lọc Kiểu lấy mẫu
        lay_mau_list = ["Tất cả"] + list(df["Kiểu lấy mẫu"].unique())
        chon_lay_mau = st.selectbox("2. Kiểu lấy mẫu:", lay_mau_list)
        
    with col3:
        # Lọc Môi trường (Chứng chỉ)
        # Tách các chứng chỉ ra khỏi chuỗi để tạo list độc lập
        all_certs = set([cert.strip() for certs in df["Môi trường / Chứng chỉ"].str.split(',') for cert in certs])
        chon_moi_truong = st.selectbox("3. Yêu cầu chứng chỉ đặc biệt:", ["Tất cả"] + sorted(list(all_certs)))

    # Ô nhập loại khí tìm kiếm tự do (Vì tổ hợp khí rất nhiều)
    chon_khi = st.text_input("4. Nhập loại khí cần đo (VD: LEL, H2S, NH3... để trống nếu chưa xác định):", placeholder="VD: LEL")

# ==========================================
# 3. THUẬT TOÁN LỌC DỮ LIỆU
# ==========================================
filtered_df = df.copy()

if chon_loai != "Tất cả":
    filtered_df = filtered_df[filtered_df["Loại máy"] == chon_loai]
    
if chon_lay_mau != "Tất cả":
    filtered_df = filtered_df[filtered_df["Kiểu lấy mẫu"] == chon_lay_mau]

if chon_moi_truong != "Tất cả":
    # Kiểm tra xem chứng chỉ được chọn có nằm trong cột không
    filtered_df = filtered_df[filtered_df["Môi trường / Chứng chỉ"].str.contains(chon_moi_truong, case=False, na=False)]

if chon_khi:
    filtered_df = filtered_df[filtered_df["Khí đo được"].str.contains(chon_khi, case=False, na=False)]

# ==========================================
# 4. HIỂN THỊ KẾT QUẢ ĐỀ XUẤT
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader(f"✅ Đề xuất phù hợp: TÌM THẤY {len(filtered_df)} THIẾT BỊ")

if not filtered_df.empty:
    # Hiển thị kết quả dạng lưới (Grid) thay vì bảng nhàm chán
    cols = st.columns(3) # Hiển thị 3 sản phẩm 1 hàng
    
    for index, row in filtered_df.reset_index().iterrows():
        # Phân phối tuần tự vào 3 cột
        with cols[index % 3]:
            with st.container(border=True):
                # Dùng HTML để canh giữa ảnh và giới hạn chiều cao
                st.markdown(f"<div style='text-align: center;'><img src='{row['Hình ảnh']}' height='150'></div>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align: center; color: #d10000;'>{row['Model']}</h3>", unsafe_allow_html=True)
                st.markdown(f"**Kiểu máy:** {row['Loại máy']}")
                st.markdown(f"**Lấy mẫu:** {row['Kiểu lấy mẫu']}")
                st.markdown(f"**Khí đo:** {row['Khí đo được']}")
                st.markdown(f"**Chứng chỉ:** {row['Môi trường / Chứng chỉ']}")
                st.info(f"💡 {row['Tính năng nổi bật']}")
                st.button(f"📥 Tải Datasheet {row['Model']}", key=f"btn_{row['Model']}", use_container_width=True)
else:
    st.warning("⚠️ Không có thiết bị nào thỏa mãn toàn bộ các tiêu chí trên. Vui lòng giảm bớt bộ lọc hoặc liên hệ phòng Kỹ thuật.")

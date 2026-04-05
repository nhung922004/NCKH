import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cấu hình trang rộng
st.set_page_config(page_title="Dự báo nội lực sàn EC2", layout="wide")

# Tiêu đề chính
st.markdown("<h1 style='text-align: center;'>🏗️ HỆ THỐNG DỰ BÁO NỘI LỰC SÀN THEO EUROCODE 2</h1>", unsafe_allow_html=True)
st.write(f"**Sinh viên:** Ngô Thị Phương Nhung | **MSV:** 111220049")

# Chia làm 2 cột: Trái (Input) - Phải (Biểu đồ)
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("📥 Thông số đầu vào")
    with st.container(border=True):
        Lx = st.number_input("Chiều dài nhịp Lx (m)", value=5.0, step=0.1)
        Ly = st.number_input("Chiều rộng nhịp Ly (m)", value=4.0, step=0.1)
        
        # Lấy danh sách bề dày h từ database nếu có, hoặc cho chọn thủ công
        h_options = [0.10, 0.12, 0.15, 0.18, 0.20, 0.22, 0.25]
        h = st.selectbox("Bề dày sàn (m)", options=h_options, index=2)
        
        q = st.number_input("Tải trọng phân bố (kN/m2)", value=10.0, step=1.0)
        
        btn_calc = st.button("🚀 AI TÍNH TOÁN NGAY!", use_container_width=True, type="primary")

with col_right:
    st.subheader("📊 Biểu đồ Nội lực (Mô men M11)")
    
    if btn_calc:
        # Giả lập tính toán phân phối Moment (Để vẽ Heatmap như ảnh)
        # Trong thực tế, đây là nơi gọi model AI hoặc tra cứu từ Database_San_EC2_Full.csv
        grid_size = 10
        x = np.linspace(0, Lx, grid_size)
        y = np.linspace(0, Ly, grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Công thức mô phỏng hình dạng moment sàn kê 4 cạnh (giá trị max ở giữa)
        # Moment ~ q * L^2 * sin(pi*x/L) * sin(pi*y/L)
        Z = (q * min(Lx, Ly)**2 / 12) * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)
        
        # Vẽ Heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(Z, annot=False, cmap="jet", ax=ax, 
                    xticklabels=np.round(x, 1), yticklabels=np.round(y, 1))
        
        ax.set_xlabel("Trục X (Nhịp Lx)")
        ax.set_ylabel("Trục Y (Nhịp Ly)")
        
        st.pyplot(fig)
    else:
        st.info("Vui lòng điền thông số và nhấn 'Tính toán' để xem kết quả.")

# Phần hiển thị dữ liệu gốc bên dưới (Nếu cần)
with st.expander("📂 Xem cơ sở dữ liệu gốc (CSV)"):
    try:
        df = pd.read_csv("Database_San_EC2_Final_V4.csv")
        st.dataframe(df.head(100))
    except:
        st.warning("Chưa tìm thấy file Database_San_EC2_Full.csv trên GitHub.")

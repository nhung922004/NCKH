import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Cấu hình trang (Nên để rộng để hiển thị biểu đồ đẹp hơn)
st.set_page_config(page_title="AI Heatmap Sàn", layout="wide")

# ==========================================
# 1. SIDEBAR - THÔNG SỐ THIẾT KẾ
# ==========================================
with st.sidebar:
    st.header("📊 Thông số thiết kế")
    
    Lx = st.number_input("Chiều dài sàn (m)", value=5.00, step=0.5)
    Ly = st.number_input("Chiều rộng sàn (m)", value=6.00, step=0.5)
    h = st.number_input("Bề dày sàn (m)", value=0.20, step=0.01)
    
    # Cấp độ bền bê tông (bạn có thể tuỳ chỉnh list này theo TCVN hoặc EC2)
    cap_do_ben = st.selectbox("Cấp độ bền", ["B10", "B15", "B20", "B25", "B30"])
    
    q = st.number_input("Tải trọng q (kN/m2)", value=12.00, step=1.0)

# ==========================================
# 2. MAIN CONTENT - GIAO DIỆN CHÍNH
# ==========================================
st.title("📊 Phân Tích Nội Lực Sàn Thông Minh (AI Heatmap)")

st.markdown("### 🧐 Phân tích sơ bộ từ AI & Tiêu chuẩn")

# Tạo 3 thẻ thông tin (Metrics)
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Hệ thống đề xuất:** RC (Bê tông thường)")
with col2:
    st.info("**Loại biên dự kiến:** ngam_4_canh")
with col3:
    # Tính tỷ lệ nhịp L/B (Giả sử L là cạnh ngắn, B là cạnh dài hoặc ngược lại tuỳ bạn quy ước)
    ty_le = round(Lx / Ly, 2) if Ly != 0 else 0
    st.info(f"**Tỷ lệ nhịp L/B:** {ty_le}")

# ==========================================
# 3. TÍNH TOÁN DỮ LIỆU & BIỂU ĐỒ (PLOTLY)
# ==========================================
st.markdown("### 🎨 Biểu đồ phân bố Momen (Di chuột để xem giá trị)")

# Tạo Tabs cho M11 và M22
tab1, tab2 = st.tabs(["Momen M11", "Momen M22"])

# -- Tạo dữ liệu ma trận (giữ nguyên công thức của bạn) --
# Tăng số điểm chia để biểu đồ mượt hơn (ví dụ: 100x100)
x_vals = np.linspace(0, Lx, 100)
y_vals = np.linspace(0, Ly, 100)
X, Y = np.meshgrid(x_vals, y_vals)

# Công thức tính Moment mô phỏng (theo code cũ của bạn)
Z_M11 = (q * min(Lx, Ly)**2 / 12) * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)

# (Tuỳ chọn) Nếu bạn muốn giá trị âm như trong ảnh 2, bạn có thể nhân với -1 hoặc điều chỉnh công thức cho đúng chuẩn EC2
# Z_M11 = -Z_M11 

with tab1:
    st.markdown("**Phân bố Momen M11**")
    
    # Vẽ bằng Plotly thay vì Seaborn
    fig_m11 = go.Figure(data=go.Heatmap(
        z=Z_M11,
        x=x_vals,
        y=y_vals,
        colorscale='Viridis', # Bảng màu giống trong ảnh 1 & 2
        zsmooth='best',       # Làm mượt các ô màu
        hovertemplate='X: %{x:.2f}m<br>Y: %{y:.2f}m<br>M11: %{z:.2f} kNm<extra></extra>' # Định dạng khung hover
    ))
    
    fig_m11.update_layout(
        xaxis_title="Chiều dài (m)",
        yaxis_title="Chiều rộng (m)",
        margin=dict(l=20, r=20, t=30, b=20),
        height=500
    )
    
    st.plotly_chart(fig_m11, use_container_width=True)

with tab2:
    st.markdown("**Phân bố Momen M22**")
    st.info("Chèn logic tính toán và biểu đồ tương tự cho Momen M22 vào đây.")

# ==========================================
# 4. HIỂN THỊ DỮ LIỆU GỐC (CSV)
# ==========================================
with st.expander("📁 Xem cơ sở dữ liệu gốc (CSV)"):
    try:
        df = pd.read_csv("Database_San_EC2_Final_V4.csv")
        st.dataframe(df.head(100))
    except FileNotFoundError:
        st.warning("Không tìm thấy file Database_San_EC2_Final_V4.csv. Hãy đảm bảo file nằm cùng thư mục với app.py")

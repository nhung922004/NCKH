import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Cấu hình trang (Nên để rộng để hiển thị biểu đồ đẹp hơn)
st.set_page_config(page_title="AI Heatmap Sàn", layout="wide")

# ==========================================
# 1. SIDEBAR - THÔNG SỐ THIẾT KẾ
# ==========================================
with st.sidebar:
    st.markdown("<div style='background-color: #00BCD4; padding: 10px; border-radius: 5px;'><h3 style='color: white; margin: 0;'>INPUTS</h3></div>", unsafe_allow_html=True)
    
    Lx = st.number_input("Length (L) (m)", value=4.0, step=0.5)
    Ly = st.number_input("Width (W) (m)", value=3.0, step=0.5)
    h = st.number_input("Thickness (h) (m)", value=0.5, step=0.01)
    q = st.number_input("Uniform Load (ULS) (kN/m2)", value=10.0, step=1.0)
    
    st.markdown("<div style='background-color: #00BCD4; padding: 10px; border-radius: 5px; margin-top: 20px;'><h3 style='color: white; margin: 0;'>STANDARDS</h3></div>", unsafe_allow_html=True)
    
    # Cấp độ bền bê tông PHẢI NẰM TRÊN dòng chọn tiêu chuẩn
    cap_do_ben = st.selectbox("Strength Grade (Cấp độ bền)", ["B10", "B15", "B20", "B25", "B30"])
    
    # Tiêu chuẩn
    standard1 = st.checkbox("TCVN 5574:2018", value=True)
    standard2 = st.checkbox("Eurocode 2")
    standard3 = st.checkbox("ACI 318-19")

# ==========================================
# 2. MAIN CONTENT - GIAO DIỆN CHÍNH
# ==========================================
col_main_left, col_main_right = st.columns([1, 2.5])

with col_main_left:
    st.markdown("---")
    st.markdown("<h3 style='color: #00BCD4;'>📋 INPUTS</h3>", unsafe_allow_html=True)
    
    # Hiển thị thông số đã nhập
    st.write(f"**Length (L):** {Lx} m")
    st.write(f"**Width (W):** {Ly} m")
    st.write(f"**Thickness (h):** {h} m")
    st.write(f"**Uniform Load (q):** {q} kN/m²")
    st.write(f"**Strength Grade:** {cap_do_ben}")

with col_main_right:
    st.title("📊 AI Heatmap - Floor Slab Internal Force Analysis")
    
    st.markdown("### 🧐 Phân tích sơ bộ từ AI & Tiêu chuẩn")
    
    # Tạo 3 thẻ thông tin (Metrics)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Hệ thống đề xuất:** RC (Bê tông thường)")
    with col2:
        st.info("**Loại biên dự kiến:** ngam_4_canh")
    with col3:
        # Tính tỷ lệ nhịp L/B
        ty_le = round(Lx / Ly, 2) if Ly != 0 else 0
        st.info(f"**Tỷ lệ nhịp L/B:** {ty_le}")

# ==========================================
# 3. TÍNH TOÁN DỮ LIỆU & BIỂU ĐỒ (PLOTLY)
# ==========================================
st.markdown("---")
st.markdown("### 🎨 Biểu đồ phân bố Momen (Di chuột để xem giá trị)")

# Tạo Tabs cho M11 và M22
tab1, tab2 = st.tabs(["Momen M11", "Momen M22"])

# -- Tạo dữ liệu ma trận (giữ nguyên công thức của bạn) --
# Tăng số điểm chia để biểu đồ mượt hơn
x_vals = np.linspace(0, Lx, 100)
y_vals = np.linspace(0, Ly, 100)
X, Y = np.meshgrid(x_vals, y_vals)

# Công thức tính Moment mô phỏng (theo code cũ của bạn)
Z_M11 = (q * min(Lx, Ly)**2 / 12) * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)
Z_M22 = (q * min(Lx, Ly)**2 / 12) * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly) * 0.8  # M22 thường nhỏ hơn M11

def create_beautiful_3d_surface(x, y, z, title, zlabel):
    """Tạo biểu đồ 3D đẹp như ảnh mẫu - với nền sáng và trục bê tông"""
    fig = go.Figure(data=[go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale=[
            [0.0, '#0D0887'],      # Xanh đậm
            [0.1, '#46039F'],
            [0.2, '#3B4CC0'],
            [0.3, '#1984D2'],
            [0.4, '#35B779'],      # Xanh lá
            [0.5, '#FDE724'],      # Vàng
            [0.6, '#FFA500'],      # Cam
            [0.7, '#FF6E3A'],
            [0.8, '#C81D25'],      # Đỏ
            [0.9, '#8B0000'],
            [1.0, '#550000']       # Đỏ tối
        ],
        contours={
            "z": {
                "show": True,
                "usecolorscale": True,
                "highlightcolor": "limegreen",
                "project": {"z": True}
            }
        },
        hovertemplate='X: %{x:.2f}m<br>Y: %{y:.2f}m<br>' + zlabel + ': %{z:.2f} kNm<extra></extra>'
    )])
    
    # Cấu hình scene để giống ảnh mẫu - góc nhìn isometric
    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 16}
        },
        scene=dict(
            xaxis=dict(
                title="Length (L) (m)",
                backgroundcolor="rgb(240, 240, 240)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white",
            ),
            yaxis=dict(
                title="Width (W) (m)",
                backgroundcolor="rgb(240, 240, 240)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white"
            ),
            zaxis=dict(
                title=zlabel + " (kNm)",
                backgroundcolor="rgb(240, 240, 240)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white",
            ),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.3)  # Góc nhìn isometric 3D đẹp
            ),
            aspectratio=dict(x=1, y=0.75, z=0.5)
        ),
        height=600,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False,
        paper_bgcolor='rgba(240, 240, 240, 1)',
        plot_bgcolor='rgba(240, 240, 240, 1)'
    )
    
    return fig

def create_2d_heatmap(x, y, z, title, zlabel):
    """Tạo biểu đồ 2D Heatmap chiếu bằng"""
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale=[
            [0.0, '#0D0887'],
            [0.1, '#46039F'],
            [0.2, '#3B4CC0'],
            [0.3, '#1984D2'],
            [0.4, '#35B779'],
            [0.5, '#FDE724'],
            [0.6, '#FFA500'],
            [0.7, '#FF6E3A'],
            [0.8, '#C81D25'],
            [0.9, '#8B0000'],
            [1.0, '#550000']
        ],
        zsmooth='best',
        hovertemplate='X: %{x:.2f}m<br>Y: %{y:.2f}m<br>' + zlabel + ': %{z:.2f} kNm<extra></extra>',
        colorbar=dict(
            title=zlabel + "<br>(kNm)",
            thickness=15,
            len=0.7,
        )
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Length (L) (m)",
        yaxis_title="Width (W) (m)",
        height=500,
        margin=dict(l=60, r=60, t=50, b=60),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray')
    )
    
    return fig

with tab1:
    st.markdown("**Phân bố Momen M11 - 3D View & 2D Top View**")
    
    col_3d, col_2d = st.columns(2)
    
    with col_3d:
        # Vẽ 3D Surface đẹp như ảnh mẫu
        fig_m11_3d = create_beautiful_3d_surface(x_vals, y_vals, Z_M11, "M11 Bending Moment - 3D Surface", "M11")
        st.plotly_chart(fig_m11_3d, use_container_width=True)
    
    with col_2d:
        # Vẽ 2D Heatmap chiếu bằng
        fig_m11_2d = create_2d_heatmap(x_vals, y_vals, Z_M11, "M11 Bending Moment - 2D Top View (Chiếu bằng)", "M11")
        st.plotly_chart(fig_m11_2d, use_container_width=True)

with tab2:
    st.markdown("**Phân bố Momen M22 - 3D View & 2D Top View**")
    
    col_3d, col_2d = st.columns(2)
    
    with col_3d:
        # Vẽ 3D Surface đẹp như ảnh mẫu
        fig_m22_3d = create_beautiful_3d_surface(x_vals, y_vals, Z_M22, "M22 Bending Moment - 3D Surface", "M22")
        st.plotly_chart(fig_m22_3d, use_container_width=True)
    
    with col_2d:
        # Vẽ 2D Heatmap chiếu bằng
        fig_m22_2d = create_2d_heatmap(x_vals, y_vals, Z_M22, "M22 Bending Moment - 2D Top View (Chiếu bằng)", "M22")
        st.plotly_chart(fig_m22_2d, use_container_width=True)

# ==========================================
# 4. HIỂN THỊ DỮ LIỆU GỐC (CSV)
# ==========================================
st.markdown("---")
with st.expander("📁 Xem cơ sở dữ liệu gốc (CSV)"):
    try:
        df = pd.read_csv("Database_San_EC2_Final_V4.csv")
        st.dataframe(df.head(100))
    except FileNotFoundError:
        st.warning("Không tìm thấy file Database_San_EC2_Final_V4.csv. Hãy đảm bảo file nằm cùng thư mục với app.py")

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
    st.markdown("<div style='background-color: #00BCD4; padding: 10px; border-radius: 5px;'><h3 style='color: white; margin: 0;'>⚙️ INPUTS</h3></div>", unsafe_allow_html=True)
    
    Lx = st.number_input("Length (L) (m)", value=4.0, step=0.5)
    Ly = st.number_input("Width (W) (m)", value=3.0, step=0.5)
    h = st.number_input("Thickness (h) (m)", value=0.5, step=0.01)
    q = st.number_input("Uniform Load (ULS) (kN/m²)", value=10.0, step=1.0)
    
    st.markdown("<div style='background-color: #00BCD4; padding: 10px; border-radius: 5px; margin-top: 20px;'><h3 style='color: white; margin: 0;'>📋 STANDARDS</h3></div>", unsafe_allow_html=True)
    
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
    st.markdown("<h3 style='color: #00BCD4;'>📝 PARAMETERS</h3>", unsafe_allow_html=True)
    
    # Hiển thị thông số đã nhập
    st.write(f"**Length (L):** {Lx} m")
    st.write(f"**Width (W):** {Ly} m")
    st.write(f"**Thickness (h):** {h} m")
    st.write(f"**Uniform Load (q):** {q} kN/m²")
    st.write(f"**Strength Grade:** {cap_do_ben}")

with col_main_right:
    st.title("🏗️ Reinforced Concrete Slab Analysis")
    
    st.markdown("### 📊 Bending Moment Distribution & Internal Force Assessment")
    
    # Tạo 3 thẻ thông tin (Metrics)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**System:** RC (Conventional Concrete)")
    with col2:
        st.info("**Support Type:** Four-Side Support")
    with col3:
        # Tính tỷ lệ nhịp L/B
        ty_le = round(Lx / Ly, 2) if Ly != 0 else 0
        st.info(f"**Aspect Ratio L/B:** {ty_le}")

# ==========================================
# 3. TÍNH TOÁN DỮ LIỆU & BIỂU ĐỒ (PLOTLY)
# ==========================================
st.markdown("---")
st.markdown("### 📈 Bending Moment Distribution (Hover for details)")

# Tạo Tabs cho M11 và M22
tab1, tab2 = st.tabs(["M11 Distribution", "M22 Distribution"])

# -- Tạo dữ liệu ma trận (giữ nguyên công thức của bạn) --
# Tăng số điểm chia để biểu đồ mượt hơn
x_vals = np.linspace(0, Lx, 120)
y_vals = np.linspace(0, Ly, 120)
X, Y = np.meshgrid(x_vals, y_vals)

# Công thức tính Moment mô phỏng (theo code cũ của bạn)
Z_M11 = (q * min(Lx, Ly)**2 / 12) * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly)
Z_M22 = (q * min(Lx, Ly)**2 / 12) * np.sin(np.pi * X / Lx) * np.sin(np.pi * Y / Ly) * 0.8

def create_3d_surface_professional(x, y, z, title, zlabel):
    """Tạo biểu đồ 3D Surface chuyên nghiệp như ảnh mẫu"""
    fig = go.Figure(data=[go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            title=f"{zlabel}<br>(kNm)",
            thickness=20,
            len=0.7,
            x=1.02
        ),
        hovertemplate='<b>Position</b><br>X: %{x:.2f}m<br>Y: %{y:.2f}m<br>' + zlabel + ': %{z:.2f} kNm<extra></extra>',
        lighting=dict(
            ambient=0.8,
            diffuse=0.9,
            fresnel=0.04,
            roughness=0.5,
            specular=0.5
        ),
        opacity=0.95
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#00BCD4", family="Arial Black")
        ),
        scene=dict(
            xaxis=dict(
                title="Length (m)",
                backgroundcolor="rgba(230, 230, 230, 0.9)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white",
                titlefont=dict(size=12)
            ),
            yaxis=dict(
                title="Width (m)",
                backgroundcolor="rgba(230, 230, 230, 0.9)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white",
                titlefont=dict(size=12)
            ),
            zaxis=dict(
                title=f"{zlabel} (kNm)",
                backgroundcolor="rgba(230, 230, 230, 0.9)",
                gridcolor="white",
                showbackground=True,
                zerolinecolor="white",
                titlefont=dict(size=12)
            ),
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.5),
                center=dict(x=0, y=0, z=0)
            ),
            aspectratio=dict(x=1.2, y=0.9, z=0.6)
        ),
        height=650,
        margin=dict(l=0, r=100, t=80, b=0),
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=11)
    )
    
    return fig

def create_2d_heatmap_professional(x, y, z, title, zlabel):
    """Tạo biểu đồ 2D Heatmap chiếu bằng chuyên nghiệp"""
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale='Viridis',
        zsmooth='best',
        hovertemplate='<b>Position</b><br>X: %{x:.2f}m<br>Y: %{y:.2f}m<br>' + zlabel + ': %{z:.2f} kNm<extra></extra>',
        colorbar=dict(
            title=f"{zlabel}<br>(kNm)",
            thickness=20,
            len=0.7
        )
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=18, color="#00BCD4", family="Arial Black")
        ),
        xaxis=dict(
            title="Length (m)",
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        yaxis=dict(
            title="Width (m)",
            showgrid=True,
            gridwidth=1,
            gridcolor='LightGray'
        ),
        height=650,
        margin=dict(l=70, r=100, t=80, b=70),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=11)
    )
    
    return fig

with tab1:
    st.markdown("#### Bending Moment M11 - 3D Surface & 2D Plan View")
    
    col_3d, col_2d = st.columns(2)
    
    with col_3d:
        fig_m11_3d = create_3d_surface_professional(x_vals, y_vals, Z_M11, "M11 Bending Moment - 3D Visualization", "M11")
        st.plotly_chart(fig_m11_3d, use_container_width=True)
    
    with col_2d:
        fig_m11_2d = create_2d_heatmap_professional(x_vals, y_vals, Z_M11, "M11 Bending Moment - 2D Top View (Plan)", "M11")
        st.plotly_chart(fig_m11_2d, use_container_width=True)

with tab2:
    st.markdown("#### Bending Moment M22 - 3D Surface & 2D Plan View")
    
    col_3d, col_2d = st.columns(2)
    
    with col_3d:
        fig_m22_3d = create_3d_surface_professional(x_vals, y_vals, Z_M22, "M22 Bending Moment - 3D Visualization", "M22")
        st.plotly_chart(fig_m22_3d, use_container_width=True)
    
    with col_2d:
        fig_m22_2d = create_2d_heatmap_professional(x_vals, y_vals, Z_M22, "M22 Bending Moment - 2D Top View (Plan)", "M22")
        st.plotly_chart(fig_m22_2d, use_container_width=True)

# ==========================================
# 4. HIỂN THỊ DỮ LIỆU GỐC (CSV)
# ==========================================
st.markdown("---")
with st.expander("💾 Database - Raw Data (CSV)"):
    try:
        df = pd.read_csv("Database_San_EC2_Final_V4.csv")
        st.dataframe(df.head(100), use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ File not found: Database_San_EC2_Final_V4.csv - Make sure it's in the same folder as app.py")

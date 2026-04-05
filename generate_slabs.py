import pandas as pd
import numpy as np
import random

def generate_final_data(num_records=10000):
    data = []
    concrete_classes = ["C20/25", "C25/30", "C30/37", "C35/45", "C40/50"]
    
    for i in range(1, num_records + 1):
        s_types = ["Ban_dam_1_phuong", "Ban_ke_4_canh_2_phuong", "San_phang_Flat_Slab", "San_console_Cantilever", "San_o_co_Waffle_Slab"]
        s_type = random.choice(s_types)
        c_class = random.choice(concrete_classes)
        
        # Giữ nguyên tĩnh tải và hoạt tải để thuận tiện cho việc kiểm chứng trên Excel
        g_add = 1.2  
        q_k = 2.0    
        
        # Kích thước (L, W, h) được trả lại tính ngẫu nhiên (random.uniform)
        if s_type == "Ban_dam_1_phuong":
            W = round(random.uniform(2.0, 4.0), 2)
            L = round(W * random.uniform(2.1, 3.5), 2)
            h = round(random.uniform(0.10, 0.15), 2)
            q_Ed = round(1.35 * (h * 25 + g_add) + 1.5 * q_k, 2)
            m11 = round(0.8 * (q_Ed * W**2) / 8, 3)
            m22 = round(m11 * 0.2, 3)
            
        elif s_type == "Ban_ke_4_canh_2_phuong":
            W = round(random.uniform(3.0, 6.0), 2)
            L = round(W * random.uniform(1.0, 2.0), 2)
            h = round(random.uniform(0.12, 0.20), 2)
            q_Ed = round(1.35 * (h * 25 + g_add) + 1.5 * q_k, 2)
            m11 = round(0.045 * q_Ed * W**2, 3)
            m22 = round(0.035 * q_Ed * L**2, 3)
            
        elif s_type == "San_phang_Flat_Slab":
            W = round(random.uniform(6.0, 10.0), 2)
            L = round(W * random.uniform(1.0, 1.5), 2)
            h = round(random.uniform(0.20, 0.30), 2)
            q_Ed = round(1.35 * (h * 25 + g_add) + 1.5 * q_k, 2)
            m_total_0 = (q_Ed * L * W**2) / 8
            m11 = round((0.6 * m_total_0) / W, 3)
            m22 = round((0.4 * m_total_0) / L, 3)
            
        elif s_type == "San_console_Cantilever":
            W = round(random.uniform(1.2, 2.5), 2)
            L = round(random.uniform(3.0, 8.0), 2)
            h = round(random.uniform(0.10, 0.15), 2)
            q_Ed = round(1.35 * (h * 25 + g_add) + 1.5 * q_k, 2)
            m11 = round(-1 * (q_Ed * W**2) / 2, 3)
            m22 = round(m11 * 0.1, 3)
            
        else: # San_o_co_Waffle_Slab
            W = round(random.uniform(8.0, 12.0), 2)
            L = round(W * random.uniform(1.0, 1.5), 2)
            h = round(random.uniform(0.35, 0.50), 2)
            
            # Chiều dày tương đương luôn bằng 45% chiều dày tổng thể (h_eq = h * 0.45)
            h_eq = round(h * 0.45, 2) 
            
            q_Ed = round(1.35 * (h_eq * 25 + g_add) + 1.5 * q_k, 2)
            m11 = round(0.048 * q_Ed * W**2, 3)
            m22 = round(0.048 * q_Ed * L**2, 3)

        data.append([s_type, c_class, L, W, h, q_Ed, 1000+i, m11, m22])

    df = pd.DataFrame(data, columns=["Loai_San", "Cap_Do_Ben", "Chieu_dai_L(m)", "Chieu_ron_W(m)", "Be_day_h(m)", "Tai_trong_ULS(kN/m2)", "Phan_tu_so", "Momen_M11(kNm/m)", "Momen_M22(kNm/m)"])
    return df

if __name__ == "__main__":
    df = generate_final_data(10000)
    df.to_csv("Database_San_EC2_Final_V4.csv", index=False, encoding='utf-8-sig')
    print("Dữ liệu chuẩn 10,000 dòng đã được tạo lại với phân phối tự nhiên!")
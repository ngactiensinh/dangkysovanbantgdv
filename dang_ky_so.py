import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import pytz
from supabase import create_client, Client
import streamlit.components.v1 as components

st.set_page_config(page_title="Đăng ký Số Văn Bản - TGDV", page_icon="📑", layout="wide")

# ==========================================
# CẤU HÌNH SUPABASE
# ==========================================
SUPABASE_URL = "https://qqzsdxhqrdfvxnlurnyb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFxenNkeGhxcmRmdnhubHVybnliIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU2MjY0NjAsImV4cCI6MjA5MTIwMjQ2MH0.H62F5zYEZ5l47fS4IdAE2JdRdI7inXQqWG0nvXhn2P8"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except:
    pass

# --- MẬT KHẨU & CẤU HÌNH NHIỆM KỲ ---
PASS_VAN_THU = "Admin@2026"
DS_NAM_NHIEM_KY = [2026, 2027, 2028, 2029, 2030]

# --- HÀM LẤY DANH MỤC ĐỘNG TỪ SUPABASE ---
@st.cache_data(ttl=5)
def get_dynamic_categories():
    try:
        res = supabase.table("danh_muc_loai_vb").select("*").order("ten_loai").execute()
        return {item['ten_loai']: item['ky_hieu'] for item in res.data}
    except:
        return {}

# --- DANH MỤC CỐ ĐỊNH KHÁC ---
DS_PHONG_BAN = ["Văn phòng Ban", "Phòng Lý luận chính trị, Lịch sử Đảng", "Phòng Tuyên truyền, Báo chí - Xuất bản", "Phòng Khoa giáo, Văn hóa - Văn nghệ", "Phòng Dân vận các cơ quan Nhà nước", "Phòng Đoàn thể và các Hội"]
DS_NGUOI_KY = [
    "Trần Mạnh Lợi - Trưởng Ban", "Nguyễn Lam Sơn - Phó Trưởng ban Thường trực", 
    "Lê Mạnh Cường - Phó Trưởng Ban", "Chẩu Thị Thu - Phó Trưởng Ban", 
    "Hoàng Thị Hằng - Phó Trưởng Ban", "Nguyễn Văn Hưng - Phó Trưởng Ban", 
    "Vương Thúy Hằng - Phó Trưởng Ban", "Đặng Ái Xoan - Phó Trưởng Ban", 
    "Đinh Thị Thúy - Chánh Văn phòng", "KT. Chánh Văn phòng"
]

def get_vn_now():
    return datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))

# --- CSS TÙY CHỈNH ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .header-box { background-color: #ffffff; border-top: 4px solid #004B87; border-radius: 8px; padding: 15px 30px; margin-bottom: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); text-align: center;}
    .main-title { font-size: 24px; font-weight: 900; color: #004B87; text-transform: uppercase; margin: 0;}
    .number-display { font-size: 38px; font-weight: 900; color: #C8102E; text-align: center; padding: 20px; background: #fff5f5; border: 2px dashed #C8102E; border-radius: 12px; margin: 10px 0;}
    div[data-testid="stForm"] { background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #e0e6ed;}
    .report-card { background-color: #ffffff; padding: 15px; border-radius: 8px; border-left: 5px solid #17a2b8; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px;}
    
    /* MA THUẬT DÀN TRANG KHI XUẤT LƯU PDF */
    @media print {
        section[data-testid="stSidebar"] { display: none !important; }
        header[data-testid="stHeader"] { display: none !important; }
        .stTabs [data-baseweb="tab-list"] { display: none !important; }
        div[data-testid="stToolbar"] { display: none !important; }
        iframe { display: none !important; }
        .stApp { background-color: #ffffff !important; }
        .header-box { border-top: none; box-shadow: none; margin-bottom: 10px; padding: 0;}
        .report-card { border-left: none; box-shadow: none; padding: 0;}
        /* Thu nhỏ chữ bảng để không bị tràn viền khi in */
        table { font-size: 11px !important; }
        th { background-color: #f0f2f6 !important; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""<div class="header-box"><div class="main-title">HỆ THỐNG CẤP SỐ VÀ QUẢN LÝ VĂN BẢN ĐI</div><div style="font-size: 13px; font-weight: bold; color: #6c757d; margin-top:3px;">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div></div>""", unsafe_allow_html=True)

DS_LOAI_VB_DONG = get_dynamic_categories()
nam_hien_tai = get_vn_now().year
idx_nam_hien_tai = DS_NAM_NHIEM_KY.index(nam_hien_tai) if nam_hien_tai in DS_NAM_NHIEM_KY else 0

tab1, tab2, tab3, tab4 = st.tabs(["📝 CẤP SỐ", "📂 TRA CỨU SỔ VĂN THƯ", "📊 THỐNG KÊ & BÁO CÁO", "⚙️ CẤU HÌNH"])

# ==========================================
# TAB 1: CẤP SỐ (Chuyên viên)
# ==========================================
with tab1:
    if not DS_LOAI_VB_DONG:
        st.error("⚠️ Hệ thống chưa có danh mục Loại văn bản.")
    else:
        col_f, col_r = st.columns([2, 1])
        with col_f:
            with st.form("form_cap_so", clear_on_submit=True):
                st.markdown("### ✍️ Đăng ký văn bản")
                c1, c2 = st.columns(2)
                loai_vb = c1.selectbox("📌 Loại văn bản:", list(DS_LOAI_VB_DONG.keys()))
                phong_ban = c2.selectbox("🏢 Đơn vị soạn thảo:", DS_PHONG_BAN)
                trich_yeu = st.text_area("📝 Trích yếu nội dung:", height=80)
                c3, c4, c5 = st.columns([1.5, 1, 1])
                nguoi_ky = c3.selectbox("✍️ Người ký:", DS_NGUOI_KY)
                ngay_vb = c4.date_input("📅 Ngày văn bản:", value=get_vn_now().date())
                nam_chon = ngay_vb.year
                c5.info(f"📅 Năm: **{nam_chon}**")

                if st.form_submit_button("🚀 LẤY SỐ VĂN BẢN", type="primary", use_container_width=True):
                    if not trich_yeu.strip(): st.error("⚠️ Nhập trích yếu!")
                    elif nam_chon not in DS_NAM_NHIEM_KY: st.error("⚠️ Năm không hợp lệ!")
                    else:
                        try:
                            res_so = supabase.table("so_van_ban").select("so_vb").eq("nam", nam_chon).eq("loai_vb", loai_vb).order("so_vb", desc=True).limit(1).execute()
                            max_so_cap = res_so.data[0]['so_vb'] if res_so.data else 0
                            
                            res_moi = supabase.table("cau_hinh_so").select("so_bat_dau").eq("nam", nam_chon).eq("loai_vb", loai_vb).execute()
                            so_moi_admin = res_moi.data[0]['so_bat_dau'] if res_moi.data else 0
                            
                            so_moi = max(max_so_cap, so_moi_admin) + 1
                            ky_hieu = f"{so_moi}-{DS_LOAI_VB_DONG[loai_vb]}"
                            
                            supabase.table("so_van_ban").insert({
                                "nam": nam_chon, "loai_vb": loai_vb, "so_vb": so_moi, "ky_hieu": ky_hieu, 
                                "trich_yeu": trich_yeu, "nguoi_ky": nguoi_ky, "phong_ban": phong_ban, "ngay_van_ban": ngay_vb.strftime("%Y-%m-%d")
                            }).execute()
                            
                            st.session_state['vua_cap'] = ky_hieu; st.session_state['vua_ngay'] = ngay_vb.strftime("%d/%m/%Y"); st.session_state['vua_ty'] = trich_yeu
                            st.success("✅ Cấp số thành công!"); st.rerun()
                        except Exception as e: st.error(f"Lỗi: {e}")
        with col_r:
            if 'vua_cap' in st.session_state:
                st.markdown(f"<div class='number-display'><div style='font-size:14px; color:#666; font-weight:normal;'>Số văn bản:</div>{st.session_state['vua_cap']}<div style='font-size:14px; color:#666; font-weight:normal; margin-top:10px;'>Ngày văn bản:</div>{st.session_state['vua_ngay']}</div>", unsafe_allow_html=True)
                st.info(f"**Nội dung:** {st.session_state['vua_ty']}")

# ==========================================
# TAB 2: TRA CỨU ĐA TẦNG
# ==========================================
with tab2:
    st.markdown("### 🔎 Bộ lọc tra cứu Sổ Văn thư")
    f1, f2, f3, f4 = st.columns(4)
    n_loc = f1.selectbox("📅 Nhiệm kỳ / Năm:", DS_NAM_NHIEM_KY, index=idx_nam_hien_tai)
    l_loc = f2.selectbox("📌 Loại VB:", ["Tất cả"] + list(DS_LOAI_VB_DONG.keys()))
    p_loc = f3.selectbox("🏢 Đơn vị soạn thảo:", ["Tất cả"] + DS_PHONG_BAN)
    k_loc = f4.selectbox("✍️ Người ký:", ["Tất cả"] + DS_NGUOI_KY)
    t_khoa = st.text_input("🔍 Tìm theo trích yếu nội dung...")
    
    if st.button("🔄 Lấy dữ liệu Sổ", type="primary"):
        res_h = supabase.table("so_van_ban").select("*").eq("nam", n_loc).order("so_vb", desc=True).execute()
        df = pd.DataFrame(res_h.data)
        if not df.empty:
            df['ngay_van_ban'] = pd.to_datetime(df['ngay_van_ban']).dt.strftime("%d/%m/%Y")
            if l_loc != "Tất cả": df = df[df['loai_vb'] == l_loc]
            if p_loc != "Tất cả": df = df[df['phong_ban'] == p_loc]
            if k_loc != "Tất cả": df = df[df['nguoi_ky'] == k_loc]
            if t_khoa: df = df[df['trich_yeu'].str.contains(t_khoa, case=False, na=False)]
            
            if df.empty: st.warning("Không tìm thấy văn bản nào khớp với bộ lọc!")
            else:
                st.success(f"Tìm thấy **{len(df)}** văn bản.")
                df_show = df[['ngay_van_ban', 'ky_hieu', 'trich_yeu', 'nguoi_ky', 'phong_ban']].rename(columns={'ngay_van_ban':'Ngày VB', 'ky_hieu':'Số/Ký hiệu', 'trich_yeu':'Trích yếu', 'nguoi_ky':'Người ký', 'phong_ban':'Phòng'})
                st.dataframe(df_show, use_container_width=True)
                csv = df_show.to_csv(index=False).encode('utf-8-sig')
                st.download_button(label="⬇️ Tải file danh sách (CSV)", data=csv, file_name=f"SoVanBan_{n_loc}.csv", mime="text/csv")
        else: st.info("Sổ chưa có dữ liệu.")

# ==========================================
# TAB 3: THỐNG KÊ & BÁO CÁO LÃNH ĐẠO (BẢNG FULL CHUẨN IN PDF)
# ==========================================
with tab3:
    col_t1, col_t2 = st.columns([3, 1])
    col_t1.markdown("### 📊 BÁO CÁO TỔNG HỢP VĂN BẢN ĐI")
    
    c1, c2 = st.columns([1, 2])
    bc_nam = c1.selectbox("Chọn Năm báo cáo:", DS_NAM_NHIEM_KY, index=idx_nam_hien_tai)
    ky_bao_cao_list = ["Cả năm (Tháng 1 - 12)", "Quý I", "Quý II", "Quý III", "Quý IV"] + [f"Tháng {i}" for i in range(1, 13)]
    bc_ky = c2.selectbox("Chọn Kỳ báo cáo:", ky_bao_cao_list)
    
    if st.button("📈 Tạo Báo Cáo", type="primary"):
        with st.spinner("Đang tổng hợp dữ liệu..."):
            res_bc = supabase.table("so_van_ban").select("*").eq("nam", bc_nam).execute()
            df_bc = pd.DataFrame(res_bc.data)
            
            if df_bc.empty:
                st.warning(f"Chưa có dữ liệu văn bản nào trong năm {bc_nam}.")
            else:
                df_bc['ngay_datetime'] = pd.to_datetime(df_bc['ngay_van_ban'])
                df_bc['thang'] = df_bc['ngay_datetime'].dt.month
                
                if bc_ky == "Quý I": df_bc = df_bc[df_bc['thang'].isin([1, 2, 3])]
                elif bc_ky == "Quý II": df_bc = df_bc[df_bc['thang'].isin([4, 5, 6])]
                elif bc_ky == "Quý III": df_bc = df_bc[df_bc['thang'].isin([7, 8, 9])]
                elif bc_ky == "Quý IV": df_bc = df_bc[df_bc['thang'].isin([10, 11, 12])]
                elif bc_ky.startswith("Tháng"): df_bc = df_bc[df_bc['thang'] == int(bc_ky.replace("Tháng ", ""))]
                
                if df_bc.empty:
                    st.info(f"Không có văn bản nào phát hành trong {bc_ky} năm {bc_nam}.")
                else:
                    st.markdown(f"<div class='report-card'><b>TỔNG SỐ VĂN BẢN PHÁT HÀNH TRONG KỲ:</b> <span style='font-size: 24px; color: #C8102E;'>{len(df_bc)}</span></div>", unsafe_allow_html=True)
                    
                    st.markdown("#### ✍️ Thống kê theo Người ký")
                    pivot_nguoi_ky = pd.crosstab(df_bc['nguoi_ky'], df_bc['loai_vb'])
                    pivot_nguoi_ky['TỔNG CỘNG'] = pivot_nguoi_ky.sum(axis=1)
                    # Thêm dòng tổng dưới cùng
                    pivot_nguoi_ky.loc['TỔNG SỐ (Tất cả Lãnh đạo)'] = pivot_nguoi_ky.sum()
                    st.table(pivot_nguoi_ky)
                    
                    # Biểu đồ Người ký (Loại bỏ dòng Tổng cộng khi vẽ biểu đồ)
                    st.bar_chart(pivot_nguoi_ky.drop(index='TỔNG SỐ (Tất cả Lãnh đạo)', columns=['TỔNG CỘNG']))
                    
                    st.markdown("#### 🏢 Thống kê theo Đơn vị soạn thảo")
                    pivot_phong_ban = pd.crosstab(df_bc['phong_ban'], df_bc['loai_vb'])
                    pivot_phong_ban['TỔNG CỘNG'] = pivot_phong_ban.sum(axis=1)
                    # Thêm dòng tổng dưới cùng
                    pivot_phong_ban.loc['TỔNG SỐ (Tất cả Phòng ban)'] = pivot_phong_ban.sum()
                    st.table(pivot_phong_ban)
                    
                    # Biểu đồ Đơn vị (Loại bỏ dòng Tổng cộng khi vẽ biểu đồ)
                    st.bar_chart(pivot_phong_ban.drop(index='TỔNG SỐ (Tất cả Phòng ban)', columns=['TỔNG CỘNG']))
                        
                    st.markdown("---")
                    components.html(
                        """
                        <style>
                        .btn-pdf {
                            background-color: #004B87; color: white; padding: 12px 24px;
                            text-align: center; text-decoration: none; display: inline-block;
                            font-size: 16px; font-weight: bold; border-radius: 8px; border: none; 
                            cursor: pointer; font-family: sans-serif; width: 100%; 
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s;
                        }
                        .btn-pdf:hover { background-color: #C8102E; }
                        </style>
                        <button class="btn-pdf" onclick="window.parent.print()">🖨️ BẤM VÀO ĐÂY ĐỂ IN / LƯU BÁO CÁO THÀNH FILE PDF</button>
                        """,
                        height=60
                    )

# ==========================================
# TAB 4: CẤU HÌNH (ADMIN)
# ==========================================
with tab4:
    st.markdown("### ⚙️ QUẢN TRỊ HỆ THỐNG")
    mk = st.text_input("Nhập mật khẩu Văn thư:", type="password")
    if mk == PASS_VAN_THU:
        st.success("🔓 Đã xác thực")
        c_left, c_right = st.columns([1, 1.2])
        
        with c_left:
            st.markdown("#### 📁 Quản lý Danh mục Loại văn bản")
            with st.form("form_add_cate", clear_on_submit=True):
                new_ten = st.text_input("Tên loại mới (VD: Quy định):")
                new_kh = st.text_input("Ký hiệu đi kèm (VD: QĐi/BTGDV):")
                if st.form_submit_button("➕ THÊM LOẠI VĂN BẢN MỚI"):
                    if new_ten and new_kh:
                        try:
                            supabase.table("danh_muc_loai_vb").insert({"ten_loai": new_ten, "ky_hieu": new_kh}).execute()
                            st.success(f"✅ Đã thêm '{new_ten}'!"); st.cache_data.clear(); st.rerun()
                        except: st.error("❌ Bị trùng tên hoặc có lỗi xảy ra.")
            if DS_LOAI_VB_DONG:
                st.markdown("**Danh sách đang dùng:**")
                for ten, kh in DS_LOAI_VB_DONG.items():
                    if st.button(f"🗑️ Xóa {ten} ({kh})", key=f"del_{kh}"):
                        supabase.table("danh_muc_loai_vb").delete().eq("ten_loai", ten).execute()
                        st.cache_data.clear(); st.rerun()

        with c_right:
            st.markdown("#### 🛠️ Quản lý Mồi số hiện tại")
            with st.form("form_config"):
                cfg_nam = st.selectbox("Năm:", DS_NAM_NHIEM_KY, index=idx_nam_hien_tai)
                cfg_loai = st.selectbox("Loại VB:", list(DS_LOAI_VB_DONG.keys()))
                cfg_so = st.number_input("Số hiện tại muốn thiết lập:", min_value=0, step=1)
                if st.form_submit_button("💾 LƯU CẤU HÌNH"):
                    try:
                        check = supabase.table("cau_hinh_so").select("*").eq("nam", cfg_nam).eq("loai_vb", cfg_loai).execute()
                        if check.data: supabase.table("cau_hinh_so").update({"so_bat_dau": cfg_so}).eq("nam", cfg_nam).eq("loai_vb", cfg_loai).execute()
                        else: supabase.table("cau_hinh_so").insert({"nam": cfg_nam, "loai_vb": cfg_loai, "so_bat_dau": cfg_so}).execute()
                        st.success("✅ Đã cập nhật số mồi!"); st.rerun()
                    except Exception as e: st.error(f"Lỗi: {e}")
            
            st.write("---")
            st.markdown("**📋 Danh sách các số đã mồi:**")
            res_cfg = supabase.table("cau_hinh_so").select("*").order("nam", desc=True).execute()
            if res_cfg.data:
                for item in res_cfg.data:
                    col_info, col_del = st.columns([3, 1])
                    col_info.write(f"📅 **{item['nam']}** | {item['loai_vb']}: Số **{item['so_bat_dau']}**")
                    if col_del.button("🗑️ Xóa", key=f"del_cfg_{item['id']}"):
                        supabase.table("cau_hinh_so").delete().eq("id", item['id']).execute()
                        st.warning(f"Đã xóa cấu hình {item['loai_vb']}"); st.rerun()
            else: st.info("Chưa có cấu hình mồi số nào.")

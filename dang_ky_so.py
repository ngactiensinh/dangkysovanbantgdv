import streamlit as st
import pandas as pd
import base64
from datetime import datetime
import pytz
from supabase import create_client, Client

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

# --- MẬT KHẨU ---
PASS_VAN_THU = "Admin@2026"

# --- HÀM LẤY DANH MỤC DỘNG ---
@st.cache_data(ttl=5)
def get_dynamic_categories():
    try:
        res = supabase.table("danh_muc_loai_vb").select("*").order("ten_loai").execute()
        return {item['ten_loai']: item['ky_hieu'] for item in res.data}
    except:
        return {}

# --- DANH MỤC KHÁC ---
DS_PHONG_BAN = ["Văn phòng Ban", "Phòng Lý luận chính trị, Lịch sử Đảng", "Phòng Tuyên truyền, Báo chí - Xuất bản", "Phòng Khoa giáo, Văn hóa - Văn nghệ", "Phòng Dân vận các cơ quan Nhà nước", "Phòng Đoàn thể và các Hội"]
DS_NGUOI_KY = ["Trưởng Ban", "Phó Trưởng ban Thường trực", "Phó Trưởng Ban", "Chánh Văn phòng", "KT. Chánh Văn phòng"]

def get_vn_now():
    return datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))

# --- CSS ---
st.markdown("""
<style>
    .stApp { background-color: #f4f6f9; }
    .header-box { background-color: #ffffff; border-top: 4px solid #004B87; border-radius: 8px; padding: 15px 30px; margin-bottom: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); text-align: center;}
    .main-title { font-size: 24px; font-weight: 900; color: #004B87; text-transform: uppercase; margin: 0;}
    .number-display { font-size: 38px; font-weight: 900; color: #C8102E; text-align: center; padding: 20px; background: #fff5f5; border: 2px dashed #C8102E; border-radius: 12px; margin: 10px 0;}
    div[data-testid="stForm"] { background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #e0e6ed;}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""<div class="header-box"><div class="main-title">HỆ THỐNG CẤP SỐ VÀ QUẢN LÝ VĂN BẢN ĐI</div><div style="font-size: 13px; font-weight: bold; color: #6c757d; margin-top:3px;">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div></div>""", unsafe_allow_html=True)

DS_LOAI_VB_DONG = get_dynamic_categories()
tab1, tab2, tab3 = st.tabs(["📝 CẤP SỐ (Chuyên viên)", "📂 TRA CỨU SỔ VĂN THƯ", "⚙️ CẤU HÌNH HỆ THỐNG"])

# --- TAB 1: CẤP SỐ ---
with tab1:
    if not DS_LOAI_VB_DONG:
        st.error("⚠️ Chưa có danh mục Loại văn bản.")
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
                # BỔ SUNG NGÀY VĂN BẢN
                ngay_vb = c4.date_input("📅 Ngày văn bản:", value=get_vn_now().date())
                nam_hien_tai = ngay_vb.year
                c5.info(f"📅 Năm: **{nam_hien_tai}**")

                if st.form_submit_button("🚀 LẤY SỐ VĂN BẢN", type="primary", use_container_width=True):
                    if not trich_yeu.strip(): st.error("⚠️ Nhập trích yếu!")
                    else:
                        try:
                            res_so = supabase.table("so_van_ban").select("so_vb").eq("nam", nam_hien_tai).eq("loai_vb", loai_vb).order("so_vb", desc=True).limit(1).execute()
                            max_so_cap = res_so.data[0]['so_vb'] if res_so.data else 0
                            res_moi = supabase.table("cau_hinh_so").select("so_bat_dau").eq("nam", nam_hien_tai).eq("loai_vb", loai_vb).execute()
                            so_moi_admin = res_moi.data[0]['so_bat_dau'] if res_moi.data else 0
                            
                            so_moi = max(max_so_cap, so_moi_admin) + 1
                            ky_hieu = f"{so_moi}-{DS_LOAI_VB_DONG[loai_vb]}"
                            
                            supabase.table("so_van_ban").insert({
                                "nam": nam_hien_tai, 
                                "loai_vb": loai_vb, 
                                "so_vb": so_moi, 
                                "ky_hieu": ky_hieu, 
                                "trich_yeu": trich_yeu, 
                                "nguoi_ky": nguoi_ky, 
                                "phong_ban": phong_ban,
                                "ngay_van_ban": ngay_vb.strftime("%Y-%m-%d")
                            }).execute()
                            
                            st.session_state['vua_cap'] = ky_hieu
                            st.session_state['vua_ngay'] = ngay_vb.strftime("%d/%m/%Y")
                            st.session_state['vua_ty'] = trich_yeu
                            st.success("✅ Thành công!"); st.rerun()
                        except Exception as e: st.error(f"Lỗi: {e}")
        with col_r:
            if 'vua_cap' in st.session_state:
                st.markdown(f"""
                <div class='number-display'>
                    <div style='font-size:14px; color:#666; font-weight:normal;'>Số văn bản:</div>{st.session_state['vua_cap']}
                    <div style='font-size:14px; color:#666; font-weight:normal; margin-top:10px;'>Ngày văn bản:</div>{st.session_state['vua_ngay']}
                </div>
                """, unsafe_allow_html=True)
                st.info(f"**Nội dung:** {st.session_state['vua_ty']}")

# --- TAB 2: TRA CỨU ---
with tab2:
    f1, f2, f3 = st.columns([1, 1, 2])
    n_loc = f1.selectbox("Năm:", [get_vn_now().year, get_vn_now().year - 1])
    l_loc = f2.selectbox("Loại VB:", ["Tất cả"] + list(DS_LOAI_VB_DONG.keys()))
    t_khoa = f3.text_input("🔍 Tìm theo trích yếu...")
    
    if st.button("🔄 Cập nhật sổ"):
        res_h = supabase.table("so_van_ban").select("*").eq("nam", n_loc).order("so_vb", desc=True).execute()
        df = pd.DataFrame(res_h.data)
        if not df.empty:
            # Format lại ngày hiển thị cho đẹp
            df['ngay_van_ban'] = pd.to_datetime(df['ngay_van_ban']).dt.strftime("%d/%m/%Y")
            if l_loc != "Tất cả": df = df[df['loai_vb'] == l_loc]
            if t_khoa: df = df[df['trich_yeu'].str.contains(t_khoa, case=False, na=False)]
            
            st.dataframe(df[['ngay_van_ban', 'ky_hieu', 'trich_yeu', 'nguoi_ky', 'phong_ban']].rename(
                columns={'ngay_van_ban':'Ngày VB', 'ky_hieu':'Số/Ký hiệu', 'trich_yeu':'Trích yếu', 'nguoi_ky':'Người ký', 'phong_ban':'Phòng'}
            ), use_container_width=True)
        else: st.info("Sổ chưa có dữ liệu.")

# --- TAB 3: CẤU HÌNH (ADMIN) --- (Giữ nguyên như bản V3)
with tab3:
    st.markdown("### ⚙️ QUẢN TRỊ HỆ THỐNG")
    mk = st.text_input("Nhập mật khẩu Văn thư:", type="password")
    if mk == PASS_VAN_THU:
        st.success("🔓 Đã xác thực")
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown("#### 📁 Quản lý Danh mục")
            with st.form("form_add_cate", clear_on_submit=True):
                new_ten = st.text_input("Tên loại mới:")
                new_kh = st.text_input("Ký hiệu:")
                if st.form_submit_button("➕ THÊM"):
                    if new_ten and new_kh:
                        supabase.table("danh_muc_loai_vb").insert({"ten_loai": new_ten, "ky_hieu": new_kh}).execute()
                        st.cache_data.clear(); st.rerun()
            if DS_LOAI_VB_DONG:
                for ten, kh in DS_LOAI_VB_DONG.items():
                    if st.button(f"🗑️ Xóa {ten}", key=f"del_{kh}"):
                        supabase.table("danh_muc_loai_vb").delete().eq("ten_loai", ten).execute()
                        st.cache_data.clear(); st.rerun()
        with c_right:
            st.markdown("#### 🛠️ Mồi số hiện tại")
            with st.form("form_config"):
                cfg_nam = st.selectbox("Năm:", [get_vn_now().year, get_vn_now().year + 1])
                cfg_loai = st.selectbox("Loại VB:", list(DS_LOAI_VB_DONG.keys()))
                cfg_so = st.number_input("Số hiện tại:", min_value=0, step=1)
                if st.form_submit_button("💾 LƯU"):
                    check = supabase.table("cau_hinh_so").select("*").eq("nam", cfg_nam).eq("loai_vb", cfg_loai).execute()
                    if check.data: supabase.table("cau_hinh_so").update({"so_bat_dau": cfg_so}).eq("nam", cfg_nam).eq("loai_vb", cfg_loai).execute()
                    else: supabase.table("cau_hinh_so").insert({"nam": cfg_nam, "loai_vb": cfg_loai, "so_bat_dau": cfg_so}).execute()
                    st.success("✅ Đã lưu!"); st.rerun()

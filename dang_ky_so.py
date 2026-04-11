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

# --- DANH MỤC ---
DS_LOAI_VB = {
    "Nghị quyết": "NQ-TU", "Quyết định": "QĐ-TU", "Kế hoạch": "KH-TU",
    "Công văn": "CV-TU", "Báo cáo": "BC-TU", "Hướng dẫn": "HD-TU",
    "Thông báo": "TB-TU", "Tờ trình": "TTr-TU"
}
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
    .number-display { font-size: 42px; font-weight: 900; color: #C8102E; text-align: center; padding: 25px; background: #fff5f5; border: 2px dashed #C8102E; border-radius: 12px; margin: 15px 0;}
    div[data-testid="stForm"] { background-color: #ffffff; padding: 20px; border-radius: 8px; border: 1px solid #e0e6ed;}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""<div class="header-box"><div class="main-title">HỆ THỐNG CẤP SỐ VÀ QUẢN LÝ VĂN BẢN ĐI</div><div style="font-size: 13px; font-weight: bold; color: #6c757d; margin-top:3px;">BAN TUYÊN GIÁO VÀ DÂN VẬN TỈNH ỦY TUYÊN QUANG</div></div>""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📝 CẤP SỐ (Chuyên viên)", "📂 TRA CỨU SỔ VĂN THƯ", "⚙️ CẤU HÌNH HỆ THỐNG"])

# --- TAB 1: CẤP SỐ ---
with tab1:
    col_f, col_r = st.columns([2, 1])
    with col_f:
        with st.form("form_cap_so", clear_on_submit=True):
            st.markdown("### ✍️ Đăng ký văn bản")
            c1, c2 = st.columns(2)
            loai_vb = c1.selectbox("📌 Loại văn bản:", list(DS_LOAI_VB.keys()))
            phong_ban = c2.selectbox("🏢 Đơn vị soạn thảo:", DS_PHONG_BAN)
            trich_yeu = st.text_area("📝 Trích yếu nội dung:", height=80)
            c3, c4 = st.columns(2)
            nguoi_ky = c3.selectbox("✍️ Người ký:", DS_NGUOI_KY)
            nam_hien_tai = get_vn_now().year
            c4.info(f"📅 Năm: **{nam_hien_tai}**")

            if st.form_submit_button("🚀 LẤY SỐ VĂN BẢN", type="primary", use_container_width=True):
                if not trich_yeu.strip(): st.error("⚠️ Nhập trích yếu!")
                else:
                    try:
                        # Lấy số lớn nhất từ sổ đã cấp
                        res_so = supabase.table("so_van_ban").select("so_vb").eq("nam", nam_hien_tai).eq("loai_vb", loai_vb).order("so_vb", desc=True).limit(1).execute()
                        max_so_cap = res_so.data[0]['so_vb'] if res_so.data else 0
                        
                        # Lấy số mồi từ cấu hình Admin
                        res_moi = supabase.table("cau_hinh_so").select("so_bat_dau").eq("nam", nam_hien_tai).eq("loai_vb", loai_vb).execute()
                        so_moi_admin = res_moi.data[0]['so_bat_dau'] if res_moi.data else 0
                        
                        # Số mới = Max(số đã cấp, số mồi) + 1
                        so_moi = max(max_so_cap, so_moi_admin) + 1
                        ky_hieu = f"{so_moi}-{DS_LOAI_VB[loai_vb]}"
                        
                        supabase.table("so_van_ban").insert({"nam": nam_hien_tai, "loai_vb": loai_vb, "so_vb": so_moi, "ky_hieu": ky_hieu, "trich_yeu": trich_yeu, "nguoi_ky": nguoi_ky, "phong_ban": phong_ban}).execute()
                        st.session_state['vua_cap'] = ky_hieu; st.session_state['ty'] = trich_yeu
                        st.success("✅ Đã cấp số và lưu vào sổ!"); st.rerun()
                    except Exception as e: st.error(f"Lỗi: {e}")
    with col_r:
        if 'vua_cap' in st.session_state:
            st.markdown(f"<div class='number-display'><div style='font-size:14px; color:#666; font-weight:normal;'>Số văn bản của bạn:</div>{st.session_state['vua_cap']}</div>", unsafe_allow_html=True)
            st.info(f"**Nội dung:** {st.session_state['ty']}")

# --- TAB 2: TRA CỨU ---
with tab2:
    f1, f2, f3 = st.columns([1, 1, 2])
    n_loc = f1.selectbox("Năm:", [nam_hien_tai, nam_hien_tai-1])
    l_loc = f2.selectbox("Loại VB:", ["Tất cả"] + list(DS_LOAI_VB.keys()))
    t_khoa = f3.text_input("🔍 Tìm từ khóa trích yếu...")
    
    if st.button("🔄 Cập nhật danh sách"):
        res_h = supabase.table("so_van_ban").select("*").eq("nam", n_loc).order("created_at", desc=True).execute()
        df = pd.DataFrame(res_h.data)
        if not df.empty:
            df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert('Asia/Ho_Chi_Minh').dt.strftime("%d/%m/%Y %H:%M")
            if l_loc != "Tất cả": df = df[df['loai_vb'] == l_loc]
            if t_khoa: df = df[df['trich_yeu'].str.contains(t_khoa, case=False, na=False)]
            st.dataframe(df[['created_at', 'ky_hieu', 'trich_yeu', 'nguoi_ky', 'phong_ban']].rename(columns={'created_at':'Thời gian','ky_hieu':'Số/Ký hiệu','trich_yeu':'Trích yếu','nguoi_ky':'Người ký','phong_ban':'Phòng'}), use_container_width=True)
        else: st.info("Sổ trống.")

# --- TAB 3: CẤU HÌNH (ADMIN) ---
with tab3:
    st.markdown("### ⚙️ QUẢN TRỊ HỆ THỐNG")
    mk = st.text_input("Nhập mật khẩu Văn thư để cấu hình:", type="password")
    if mk == PASS_VAN_THU:
        st.success("🔓 Đã xác thực quyền Văn thư")
        st.markdown("---")
        st.markdown("#### 🛠️ Thiết lập Số hiện tại (Mồi số)")
        st.info("💡 Ví dụ: Sổ giấy đang dừng ở số 150, sếp nhập 150 vào đây. Người tiếp theo đăng ký sẽ nhận số 151.")
        
        with st.form("form_config"):
            c1, c2, c3 = st.columns(3)
            cfg_nam = c1.selectbox("Chọn năm:", [nam_hien_tai, nam_hien_tai+1])
            cfg_loai = c2.selectbox("Loại văn bản:", list(DS_LOAI_VB.keys()))
            cfg_so = c3.number_input("Số hiện tại đang dừng ở:", min_value=0, step=1)
            
            if st.form_submit_button("💾 LƯU CẤU HÌNH SỐ BẮT ĐẦU"):
                try:
                    # Kiểm tra xem đã có cấu hình cho năm/loại này chưa
                    check = supabase.table("cau_hinh_so").select("*").eq("nam", cfg_nam).eq("loai_vb", cfg_loai).execute()
                    if check.data:
                        supabase.table("cau_hinh_so").update({"so_bat_dau": cfg_so}).eq("nam", cfg_nam).eq("loai_vb", cfg_loai).execute()
                    else:
                        supabase.table("cau_hinh_so").insert({"nam": cfg_nam, "loai_vb": cfg_loai, "so_bat_dau": cfg_so}).execute()
                    st.success(f"✅ Đã chốt số mồi cho {cfg_loai} năm {cfg_nam} là: {cfg_so}")
                except Exception as e: st.error(f"Lỗi: {e}")

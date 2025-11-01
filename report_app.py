import streamlit as st

# --- تنظیمات اولیه صفحه ---
st.set_page_config(page_title="مولد گزارش رادیولوژی", layout="wide")

# --- 🚀 اعمال استایل RTL (راست‌چین) ---
st.markdown(
    """
    <style>
    body, .main, .stTextInput, .stTextArea, .stButton>button, .stRadio>label, .stCheckbox>label, .stSelectbox>label {
        direction: rtl !important;
        text-align: right !important;
        font-size: 1.1rem !important; 
    }
    .stRadio>div, .stCheckbox {
        flex-direction: row-reverse;
        justify-content: flex-end;
        gap: 1rem;
    }
    .stButton>button {
        padding: 0.25rem 0.5rem;
        margin: 0.1rem;
        font-size: 1rem !important;
    }
    .stButton>button[kind="primary"], .stButton>button[kind="secondary"] {
        font-size: 1.1rem !important;
    }
    .stCheckbox { padding: 5px; }
    /* جدا کردن بخش‌های فرم */
    .form-section {
        border-top: 1px solid #444;
        padding-top: 15px;
        margin-top: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- بخش ۱: لیست‌های ثابت ---
ENDO_CANAL_OPTIONS = [
    "MB", "MB1", "MB2", "MB3", "DB", "P", "L", "ML", "DL", "B", "M", "D", "C-Shaped",
    "... سایر (تایپ دستی)"
]

# --- بخش ۲: مدیریت حافظه (Session State) ---

def init_cbct_state():
    """مقادیر پیش‌فرض فرم CBCT"""
    st.session_state.sinus_maxillary = False
    st.session_state.sinus_ethmoid = False
    st.session_state.sinus_frontal = False
    st.session_state.sinus_sphenoid = False
    st.session_state.septum_status = "مشاهده نشد"
    st.session_state.septum_deviation = "۱. راست"
    st.session_state.septum_area = "۱. استخوانی"
    st.session_state.nasal_spur = "۲. مشاهده نمی شود"
    st.session_state.osteum_status = "۱. باز"
    st.session_state.concha_occurrence = "۲. مشاهده نمی شود"
    st.session_state.concha_side = "۱. راست"
    st.session_state.haller_cells = "۲. مشاهده نمی شود"
    st.session_state.cbct_generated_report = ""

def init_endo_state():
    """مقادیر پیش‌فرض فرم Endo"""
    st.session_state.endo_canals = []
    st.session_state.endo_tooth_id = None
    st.session_state.endo_generated_report = ""

def init_surgery_state():
    """مقادیر پیش‌فرض فرم Surgery"""
    st.session_state.surgery_tooth_id = None
    st.session_state.root_count = 1
    st.session_state.root_m_majza = False
    st.session_state.root_m_beham = False
    st.session_state.root_m_mostaghim = False
    st.session_state.root_m_kerv = False
    st.session_state.apex_pos_superior = False
    st.session_state.apex_pos_inferior = False
    st.session_state.apex_pos_buccal = False
    st.session_state.apex_pos_lingual = False
    st.session_state.paresthesia_risk = "ندارد"
    st.session_state.fracture_risk = "ندارد"
    st.session_state.plate_pos_buccal = False
    st.session_state.plate_pos_lingual = False
    st.session_state.submandibular_risk = "ندارد"
    st.session_state.decay_status = "بسته است"
    st.session_state.resorption_status = "نشده است"
    st.session_state.pdl_status = "مشاهده"
    st.session_state.ankylosis_risk = "ندارد"
    st.session_state.surgery_generated_report = ""

# راه‌اندازی اولیه برنامه
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = "main"  # <--- صفحه اصلی
    init_cbct_state()
    init_endo_state()
    init_surgery_state()

# --- بخش ۳: توابع ناوبری (Navigation) ---

def navigate_to(mode):
    """تابع برای جابجایی بین صفحات و ریست کردن فرم‌ها"""
    st.session_state.app_mode = mode
    # با هر بار جابجایی، هر سه فرم ریست می‌شوند
    init_cbct_state()
    init_endo_state()
    init_surgery_state()

# --- چارت دندانی (به عنوان یک تابع مشترک) ---
def draw_dental_chart(on_click_function_name):
    """یک چارت دندانی قابل کلیک رسم می‌کند و نام تابع کلیک را می‌گیرد"""
    upper_right_teeth = [18, 17, 16, 15, 14, 13, 12, 11]
    upper_left_teeth = [21, 22, 23, 24, 25, 26, 27, 28]
    lower_left_teeth = [31, 32, 33, 34, 35, 36, 37, 38]
    lower_right_teeth = [48, 47, 46, 45, 44, 43, 42, 41]
    
    col_right, col_left = st.columns(2)
    with col_right:
        st.markdown("<h5 style='text-align: center;'>راست (Right)</h5>", unsafe_allow_html=True)
        cols_ur = st.columns(8)
        for i, tooth in enumerate(upper_right_teeth):
            cols_ur[i].button(str(tooth), key=f"t{tooth}", on_click=on_click_function_name, args=(tooth,), use_container_width=True)
        cols_lr = st.columns(8)
        for i, tooth in enumerate(lower_right_teeth):
            cols_lr[i].button(str(tooth), key=f"t{tooth}", on_click=on_click_function_name, args=(tooth,), use_container_width=True)
    with col_left:
        st.markdown("<h5 style='text-align: center;'>چپ (Left)</h5>", unsafe_allow_html=True)
        cols_ul = st.columns(8)
        for i, tooth in enumerate(upper_left_teeth):
            cols_ul[i].button(str(tooth), key=f"t{tooth}", on_click=on_click_function_name, args=(tooth,), use_container_width=True)
        cols_ll = st.columns(8)
        for i, tooth in enumerate(lower_left_teeth):
            cols_ll[i].button(str(tooth), key=f"t{tooth}", on_click=on_click_function_name, args=(tooth,), use_container_width=True)

# --- بخش ۴: روتِر اصلی برنامه (Main Router) ---

# ==================================================================
# ===                      صفحه اصلی (منو)                      ===
# ==================================================================
if st.session_state.app_mode == "main":
    st.title("به مولد گزارش رادیولوژی خوش آمدید")
    st.subheader("لطفاً نوع گزارشی که می‌خواهید ایجاد کنید را انتخاب نمایید:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button(
            "📄 گزارش CBCT",
            on_click=navigate_to,
            args=("cbct",),
            use_container_width=True, type="primary"
        )
        st.caption("برای گزارش‌های مربوط به سینوس، سپتوم و آناتومی کلی.")
        
    with col2:
        st.button(
            "🦷 گزارش Endo (طول کانال)",
            on_click=navigate_to,
            args=("endo",),
            use_container_width=True, type="primary"
        )
        st.caption("برای بررسی طول کرکرد کانال‌ها در درمان ریشه.")
        
    with col3:
        st.button(
            " surgically مولد گزارش جراحی",
            on_click=navigate_to,
            args=("surgery",),
            use_container_width=True, type="primary"
        )
        st.caption("برای بررسی‌های قبل از جراحی دندان عقل.")

# ==================================================================
# ===                     صفحه گزارش CBCT                       ===
# ==================================================================
elif st.session_state.app_mode == "cbct":
    
    st.button(" بازگشت به منوی اصلی", on_click=navigate_to, args=("main",))
    st.divider()
    st.title("📄 مولد گزارش رادیوگرافی CBCT")
    st.info("لطفاً موارد مشاهده شده در رادیوگرافی را انتخاب کنید.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("بخش ۱: سینوس‌ها و سپتوم")
        with st.expander("افزایش ضخامت مخاط سینوس", expanded=True):
            st.checkbox("۱. ماگزیلاری", key="sinus_maxillary")
            st.checkbox("۲. اتموئید", key="sinus_ethmoid")
            st.checkbox("۳. فرونتال", key="sinus_frontal")
            st.checkbox("۴. اسفنوئید", key="sinus_sphenoid")
        with st.expander("انحراف سپتوم بینی", expanded=True):
            st.radio("وضعیت انحراف سپتوم:", ("مشاهده نشد", "مشاهده شد"), horizontal=True, key="septum_status")
            if st.session_state.septum_status == "مشاهده شد":
                st.radio("جهت انحراف:", ("۱. راست", "۲. چپ", "۳. S-Curve"), horizontal=True, key="septum_deviation")
                st.radio("ناحیه انحراف:", ("۱. استخوانی", "۲. غضروفی", "۳. استخوانی غضروفی"), horizontal=True, key="septum_area")
        with st.expander("Nasal Spur", expanded=True):
            st.radio("Nasal Spur در سپتوم بینی:", ("۱. مشاهده میشود", "۲. مشاهده نمی شود"), key="nasal_spur", horizontal=True)
    with col2:
        st.subheader("بخش ۲: یافته‌های دیگر")
        with st.expander("استئوم سینوس ماگزیلاری", expanded=True):
            st.radio("وضعیت استئوم:", ("۱. باز", "۲. بسته"), key="osteum_status", horizontal=True)
        with st.expander("Concha Bullosa", expanded=True):
            st.radio("وضعیت Concha Bullosa:", ("۱. مشاهده میشود", "۲. مشاهده نمی شود"), key="concha_occurrence", horizontal=True)
            if st.session_state.concha_occurrence == "۱. مشاهده میشود":
                st.radio("در توربینیت میانی کدام سمت؟", ("۱. راست", "۲. چپ", "۳. دو طرف"), key="concha_side", horizontal=True)
        with st.expander("Haller Cells", expanded=True):
            st.radio("Haller cells در فضای تحتانی اوربیت:", ("۱. مشاهده می شود", "۲. مشاهده نمی شود"), key="haller_cells", horizontal=True)
    st.divider()

    if st.button("🚀 تولید گزارش نهایی CBCT", type="primary", use_container_width=True):
        report_lines = []
        report_lines.append("با سلام و احترام\nخدمت استاد گرامی\n\nدر رادیو گرافی CBCT به عمل آمده از بیمار در مقاطع اگزیال و کرونال:\n" + "-" * 20)
        selected_sinuses = []
        if st.session_state.sinus_maxillary: selected_sinuses.append("ماگزیلاری")
        if st.session_state.sinus_ethmoid: selected_sinuses.append("اتموئید")
        if st.session_state.sinus_frontal: selected_sinuses.append("فرونتال")
        if st.session_state.sinus_sphenoid: selected_sinuses.append("اسفنوئید")
        if selected_sinuses:
            report_lines.append(f". افزایش ضخامت مخاط در سینوس **{'، '.join(selected_sinuses)}** مشاهده می شود.")
        if st.session_state.septum_status == "مشاهده شد": 
            clean_deviation = st.session_state.septum_deviation.split('. ')[-1]
            clean_area = st.session_state.septum_area.split('. ')[-1]
            report_lines.append(f". انحراف سپتوم بینی به سمت **{clean_deviation}** در ناحیه **{clean_area}** مشاهده می گردد.")
        clean_spur = st.session_state.nasal_spur.split('. ')[-1]
        report_lines.append(f". در سپتوم بینی Nasal Spur **{clean_spur}**.")
        clean_osteum = st.session_state.osteum_status.split('. ')[-1]
        report_lines.append(f". استئوم سینوس ماگزیلاری **{clean_osteum}** می باشد.")
        clean_concha_occurrence = st.session_state.concha_occurrence.split('. ')[-1]
        if clean_concha_occurrence == "مشاهده میشود":
            clean_concha_side = st.session_state.concha_side.split('. ')[-1] 
            report_lines.append(f". در توربینیت میانی **{clean_concha_side}** Conch bullosa **مشاهده میشود**.")
        else:
            report_lines.append(f". Conch bullosa در توربینیت میانی **مشاهده نمی شود**.")
        clean_haller = st.session_state.haller_cells.split('. ')[-1]
        report_lines.append(f". Haller cells در فضای تحتانی اوربیت **{clean_haller}**.")
        report_lines.append("-" * 20 + "\n\nبا احترام")
        st.session_state.cbct_generated_report = "\n".join(report_lines)
        st.success("گزارش CBCT با موفقیت تولید شد!")

    if st.session_state.cbct_generated_report:
        st.subheader("✅ گزارش نهایی CBCT")
        st.text_area("متن گزارش:", value=st.session_state.cbct_generated_report.replace("**", ""), height=300)

# ==================================================================
# ===                     صفحه گزارش Endo                        ===
# ==================================================================
elif st.session_state.app_mode == "endo":

    st.button(" بازگشت به منوی اصلی", on_click=navigate_to, args=("main",))
    st.divider()
    
    # --- توابع کمکی مخصوص Endo ---
    def endo_select_tooth(tooth_number):
        st.session_state.endo_tooth_id = str(tooth_number)
        st.session_state.endo_generated_report = "" 
        st.session_state.endo_canals = [] 
    def endo_add_canal():
        new_canal = {"name": ENDO_CANAL_OPTIONS[0], "custom_name": "", "status": "مناسب", "measurement": ""}
        st.session_state.endo_canals.append(new_canal)
        st.session_state.endo_generated_report = ""
    def endo_remove_canal(index):
        if 0 <= index < len(st.session_state.endo_canals):
            st.session_state.endo_canals.pop(index)
            st.session_state.endo_generated_report = ""

    # --- UI اصلی Endo ---
    st.title("🦷 مولد گزارش اندو (بررسی طول کانال)")
    st.subheader("۱. دندان مورد نظر را انتخاب کنید:")
    if st.session_state.endo_tooth_id:
        st.success(f"**دندان انتخاب شده: {st.session_state.endo_tooth_id}**")
    else:
        st.info("لطفا یک دندان از چارت زیر انتخاب کنید.")
    st.caption("چارت بر اساس شماره‌گذاری استاندارد FDI")
    draw_dental_chart(endo_select_tooth) # <--- استفاده از تابع مشترک چارت
    st.divider()

    if st.session_state.endo_tooth_id:
        st.subheader(f"۲. لیست کانال‌های دندان {st.session_state.endo_tooth_id}:")
        col_header_1, col_header_2, col_header_3 = st.columns([3, 5, 1])
        with col_header_1: st.markdown("**نام کانال**")
        with col_header_2: st.markdown("**وضعیت و اندازه (mm)**")
        with col_header_3: st.markdown("**حذف**")
        if not st.session_state.endo_canals: st.caption("هنوز هیچ کانالی اضافه نشده است.")

        for index, canal in enumerate(st.session_state.endo_canals):
            col1, col2, col3 = st.columns([3, 5, 1])
            with col1:
                if canal["name"] in ENDO_CANAL_OPTIONS: select_index = ENDO_CANAL_OPTIONS.index(canal["name"])
                else: select_index = ENDO_CANAL_OPTIONS.index("... سایر (تایپ دستی)")
                canal["name"] = st.selectbox("نام کانال", ENDO_CANAL_OPTIONS, index=select_index, key=f"name_select_{index}", label_visibility="collapsed")
                if canal["name"] == "... سایر (تایپ دستی)":
                    canal["custom_name"] = st.text_input("نام سفارشی", value=canal["custom_name"], key=f"name_custom_{index}", placeholder="...نام کانال را وارد کنید")
            with col2:
                sub_col_status, sub_col_measurement = st.columns([3, 1])
                with sub_col_status:
                    status_options = ("کوتاه تر", "بیشتر", "مناسب")
                    default_index = status_options.index(canal["status"]) if canal["status"] in status_options else 2
                    canal["status"] = st.radio("وضعیت", status_options, index=default_index, horizontal=True, key=f"status_{index}", label_visibility="collapsed")
                with sub_col_measurement:
                    if canal["status"] != "مناسب":
                        canal["measurement"] = st.text_input("مقدار (mm)", value=canal.get("measurement", ""), key=f"measurement_{index}", placeholder="mm", label_visibility="collapsed")
                    else:
                        canal["measurement"] = "" 
            with col3:
                st.button("🗑️", key=f"del_{index}", on_click=endo_remove_canal, args=(index,), type="secondary")
        st.button("➕ افزودن ردیف کانال", on_click=endo_add_canal, use_container_width=True, type="primary")
        st.divider()

        if st.button("🚀 تولید گزارش نهایی Endo", type="primary", use_container_width=True):
            error_found = False
            if not st.session_state.endo_canals:
                st.error("لطفاً حداقل یک کانال را اضافه کنید."); error_found = True
            for canal in st.session_state.endo_canals:
                if canal["name"] == "... سایر (تایپ دستی)" and not canal["custom_name"]:
                    st.error("لطفاً نام کانال سفارشی (سایر) را وارد کنید."); error_found = True; break
            if not error_found:
                report_lines = []
                report_lines.append("با سلام و احترام\nخدمت همکار گرامی جناب آقای دکتر/خانم دکتر ...\n")
                fdi_id = st.session_state.endo_tooth_id
                report_lines.append(f"در بررسی رادیوگرافی به عمل آمده از **دندان {fdi_id}** پیشنهاد می گردد طول کرکرد کانال:")
                needs_correction = False
                for canal in st.session_state.endo_canals:
                    canal_name = canal["custom_name"] if canal["name"] == "... سایر (تایپ دستی)" else canal["name"]
                    canal_status = canal["status"]
                    canal_measurement = canal.get("measurement", "")
                    if canal_status == "مناسب":
                        report_lines.append(f"• **{canal_name}** : **مناسب** می باشد.")
                    else:
                        needs_correction = True
                        if canal_measurement:
                            report_lines.append(f"• **{canal_name}** : به اندازه **{canal_measurement}mm** **{canal_status}** گردد.")
                        else:
                            report_lines.append(f"• **{canal_name}** : **{canal_status}** گردد.")
                report_lines.append("")
                if not needs_correction: report_lines.append("تمامی طول‌های کرکرد بررسی شده مناسب به نظر می‌رسند.")
                report_lines.append("\nبا تشکر")
                st.session_state.endo_generated_report = "\n".join(report_lines)
                st.success("گزارش Endo با موفقیت تولید شد!")

    if st.session_state.endo_generated_report:
        st.subheader("✅ گزارش نهایی Endo")
        st.text_area("متن گزارش:", value=st.session_state.endo_generated_report.replace("**", ""), height=300)

# ==================================================================
# ===                   صفحه گزارش جراحی (Surgery)              ===
# ==================================================================
elif st.session_state.app_mode == "surgery":

    st.button(" بازگشت به منوی اصلی", on_click=navigate_to, args=("main",))
    st.divider()

    # --- توابع کمکی مخصوص Surgery ---
    def surgery_select_tooth(tooth_number):
        st.session_state.surgery_tooth_id = str(tooth_number)
        st.session_state.surgery_generated_report = "" 
        
    def surgery_reset_form():
        init_surgery_state() # فقط استیت جراحی را ریست می‌کند
        
    # --- UI اصلی Surgery ---
    st.title(" surgically مولد گزارش جراحی (دندان عقل)")
    st.button("🔄 پاک کردن این فرم", on_click=surgery_reset_form, use_container_width=True, type="secondary")
    st.divider()
    
    st.subheader("۱. دندان مورد نظر را انتخاب کنید:")
    if st.session_state.surgery_tooth_id:
        st.success(f"**دندان انتخاب شده: {st.session_state.surgery_tooth_id}**")
    else:
        st.info("لطفا یک دندان از چارت زیر انتخاب کنید.")
    draw_dental_chart(surgery_select_tooth) # <--- استفاده از تابع مشترک چارت
    st.divider()

    if st.session_state.surgery_tooth_id:
        st.subheader("۲. هدر گزارش")
        st.markdown("---")
        st.markdown("با سلام و احترام")
        st.markdown("خدمت همکار گرامی")
        st.markdown(f"در بررسی به عمل آمده از ناحیه دندان **{st.session_state.surgery_tooth_id}** در مقاطع کراس سکشنال، اگزیال و ساجیتال:")
        st.markdown("---")

        # --- بخش ۳: ریشه‌ها ---
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("۳. بررسی ریشه‌ها")
        col_text1, col_input1, col_text2 = st.columns([2, 1, 6])
        with col_text1: st.write("دندان مورد نظر دارای")
        with col_input1: st.number_input("تعداد ریشه:", min_value=1, step=1, key="root_count", label_visibility="collapsed")
        with col_text2: st.write("ریشه بوده و ریشه‌ها:")
        col_cb1, col_cb2, col_cb3, col_cb4 = st.columns(4)
        with col_cb1: st.checkbox("مجزا", key="root_m_majza")
        with col_cb2: st.checkbox("بهم چسبیده", key="root_m_beham")
        with col_cb3: st.checkbox("مستقیم", key="root_m_mostaghim")
        with col_cb4: st.checkbox("کرو دار (Curve)", key="root_m_kerv")
        st.write("می باشند.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- بخش ۴: عصب و ریسک ---
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("۴. بررسی عصب و ریسک‌ها")
        st.write("اپکس ریشه در موقعیت:")
        col_pos1, col_pos2, col_pos3, col_pos4 = st.columns(4)
        with col_pos1: st.checkbox("مجاورت فوقانی (Superior)", key="apex_pos_superior")
        with col_pos2: st.checkbox("مجاورت تحتانی (Inferior)", key="apex_pos_inferior")
        with col_pos3: st.checkbox("باکالی (Buccal)", key="apex_pos_buccal")
        with col_pos4: st.checkbox("لینگالی (Lingual)", key="apex_pos_lingual")
        st.write("کانال عصبی فک تحتانی قرار گرفته است.")
        col_risk1, col_risk2 = st.columns(2)
        with col_risk1: st.radio("و احتمال پاراستزی وجود:", ("دارد", "ندارد"), key="paresthesia_risk", horizontal=True, index=1)
        with col_risk2: st.radio("و احتمال شکستگی ریشه حین جراحی وجود:", ("دارد", "ندارد"), key="fracture_risk", horizontal=True, index=1)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- بخش ۵: جداره استخوانی ---
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("۵. بررسی جداره استخوانی")
        st.write("دندان مورد نظر در مجاورت جداره (کورتکس):")
        col_plate1, col_plate2, col_plate3 = st.columns([2, 2, 5])
        with col_plate1: st.checkbox("باکال", key="plate_pos_buccal")
        with col_plate2: st.checkbox("لینگوال", key="plate_pos_lingual")
        with col_plate3: st.write("قرار گرفته است.")
        st.radio("و احتمال نفوذ به فضای تحت فکی (Submandibular) حین جراحی وجود:", ("دارد", "ندارد"), key="submandibular_risk", horizontal=True, index=1)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- بخش ۶: پوسیدگی مجاور ---
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("۶. بررسی پوسیدگی مجاور")
        col_decay1, col_decay2 = st.columns([3, 2])
        with col_decay1: st.write("دندان مورد نظر باعث ایجاد پوسیدگی در دندان مجاور:")
        with col_decay2: st.radio("وضعیت پوسیدگی:", ("بسته است", "باز است"), key="decay_status", horizontal=True, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- بخش ۷: تحلیل ریشه مجاور ---
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("۷. بررسی تحلیل ریشه مجاور")
        col_resorp1, col_resorp2 = st.columns([3, 2])
        with col_resorp1: st.write("دندان مورد نظر باعث تحلیل ریشه در دندان مجاور:")
        with col_resorp2: st.radio("وضعیت تحلیل:", ("شده است", "نشده است"), key="resorption_status", horizontal=True, index=1, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # --- بخش ۸: PDL و انکلوز ---
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.subheader("۸. بررسی PDL و انکلوز")
        col_pdl1, col_pdl2, col_pdl3 = st.columns([1, 2, 4])
        with col_pdl1: st.write("باتوجه به:")
        with col_pdl2: st.radio("PDL", ("مشاهده", "عدم مشاهده"), key="pdl_status", horizontal=True, label_visibility="collapsed")
        with col_pdl3: st.write("فضای PDL،")
        col_ank1, col_ank2 = st.columns([1, 2])
        with col_ank1: st.write("احتمال انکلوز وجود:")
        with col_ank2: st.radio("Ankylosis", ("دارد", "ندارد"), key="ankylosis_risk", horizontal=True, index=1, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()
        
        # --- بخش ۹: دکمه سابمیت و تولید گزارش ---
        if st.button("🚀 تولید گزارش نهایی جراحی", type="primary", use_container_width=True):
            report_lines = []
            report_lines.append("با سلام و احترام")
            report_lines.append("خدمت همکار گرامی")
            report_lines.append(f"در بررسی به عمل آمده از ناحیه دندان **{st.session_state.surgery_tooth_id}** در مقاطع کراس سکشنال، اگزیال و ساجیتال:")
            
            root_count = st.session_state.root_count
            selected_morphologies = []
            if st.session_state.root_m_majza: selected_morphologies.append("مجزا")
            if st.session_state.root_m_beham: selected_morphologies.append("بهم چسبیده")
            if st.session_state.root_m_mostaghim: selected_morphologies.append("مستقیم")
            if st.session_state.root_m_kerv: selected_morphologies.append("کرو دار")
            morphology_text = " و ".join(selected_morphologies);
            if not morphology_text: morphology_text = "(موردی انتخاب نشد)"
            if root_count == 1:
                report_lines.append(f"• دندان مورد نظر دارای **{root_count}** ریشه بوده و ریشه **{morphology_text}** می باشد.")
            else:
                report_lines.append(f"• دندان مورد نظر دارای **{root_count}** ریشه بوده و ریشه‌ها **{morphology_text}** می باشند.")
            
            selected_positions = []
            if st.session_state.apex_pos_superior: selected_positions.append("مجاورت فوقانی")
            if st.session_state.apex_pos_inferior: selected_positions.append("مجاورت تحتانی")
            if st.session_state.apex_pos_buccal: selected_positions.append("باکالی")
            if st.session_state.apex_pos_lingual: selected_positions.append("لینگالی")
            position_text = " و ".join(selected_positions);
            if not position_text: position_text = "(موقعیتی انتخاب نشد)"
            report_lines.append(f"• اپکس ریشه در موقعیت **{position_text}** کانال عصبی فک تحتانی قرار گرفته است و احتمال پاراستزی وجود **{st.session_state.paresthesia_risk}** و احتمال شکستگی ریشه حین جراحی وجود **{st.session_state.fracture_risk}**.")
            
            selected_plates = []
            if st.session_state.plate_pos_buccal: selected_plates.append("باکال")
            if st.session_state.plate_pos_lingual: selected_plates.append("لینگوال")
            plate_text = " و ".join(selected_plates);
            if not plate_text: plate_text = "(موردی انتخاب نشد)"
            report_lines.append(f"• دندان مورد نظر در مجاورت جداره **{plate_text}** قرار گرفته است و احتمال نفوذ به فضای تحت فکی حین جراحی وجود **{st.session_state.submandibular_risk}**.")
            
            report_lines.append(f"• دندان مورد نظر باعث ایجاد پوسیدگی در دندان مجاور **{st.session_state.decay_status}**.")
            report_lines.append(f"• دندان مورد نظر باعث تحلیل ریشه در دندان مجاور **{st.session_state.resorption_status}**.")
            report_lines.append(f"• باتوجه به **{st.session_state.pdl_status}** فضای PDL، احتمال انکلوز وجود **{st.session_state.ankylosis_risk}**.")
            
            report_lines.append("\nبا احترام")
            st.session_state.surgery_generated_report = "\n".join(report_lines)
            st.success("گزارش با موفقیت تولید شد!")

    if st.session_state.surgery_generated_report:
        st.subheader("✅ گزارش نهایی جراحی")
        st.text_area("نسخه ساده برای کپی:", value=st.session_state.surgery_generated_report.replace("**", ""), height=300)

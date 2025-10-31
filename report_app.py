import streamlit as st

# --- تنظیمات اولیه صفحه ---
st.set_page_config(page_title="مولد گزارش CBCT", layout="wide")

# --- 🚀 اعمال استایل RTL (راست‌چین) ---
st.markdown(
    """
    <style>
    body, .main, .stTextInput, .stTextArea, .stButton>button, .stRadio>label, .stCheckbox>label {
        direction: rtl !important;
        text-align: right !important;
    }
    .stRadio>div {
        flex-direction: row-reverse;
        justify-content: flex-end;
        gap: 1rem;
    }
    .stCheckbox {
        flex-direction: row-reverse;
        gap: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- 🚀 بخش ۱: مدیریت حافظه (Session State) ---

def init_state():
    """مقادیر پیش‌فرض تمام ورودی‌ها را تنظیم می‌کند"""
    st.session_state.sinus_maxillary = False
    st.session_state.sinus_ethmoid = False
    st.session_state.sinus_frontal = False
    st.session_state.sinus_sphenoid = False
    
    st.session_state.septum_status = "مشاهده نشد" # این همان گزینه شرطی جدید است
    st.session_state.septum_deviation = "۱. راست"
    st.session_state.septum_area = "۱. استخوانی"
    
    st.session_state.nasal_spur = "۲. مشاهده نمی شود"
    st.session_state.osteum_status = "۱. باز"
    
    st.session_state.concha_occurrence = "۲. مشاهده نمی شود"
    st.session_state.concha_side = "۱. راست"
    
    st.session_state.haller_cells = "۲. مشاهده نمی شود"
    
    st.session_state.generated_report = "" # متن گزارش نهایی را خالی می‌کند

# اگر حافظه هنوز راه‌اندازی نشده، آن را راه‌اندازی کن
if 'generated_report' not in st.session_state:
    init_state()

def reset_form():
    """تابع بازنشانی که توسط دکمه فراخوانی می‌شود"""
    init_state()

# --- پایان بخش مدیریت حافظه ---


# --- عنوان برنامه ---
st.title("📄 مولد گزارش رادیوگرافی CBCT")
st.info("لطفاً موارد مشاهده شده در رادیوگرافی را بر اساس فایل PDF انتخاب کنید.")

# --- 🚀 دکمه جدید: بازنشانی فرم (درخواست ۲) ---
st.button(
    "🔄 شروع گزارش جدید (بازنشانی فرم)",
    on_click=reset_form,
    use_container_width=True
)
st.divider()

# --- فرم ورود اطلاعات ---
# توجه: تمام ویجت‌ها اکنون به 'key' در session_state متصل هستند
col1, col2 = st.columns(2)

# === ستون اول ===
with col1:
    st.subheader("بخش ۱: سینوس‌ها و سپتوم")

    # --- ۱. ضخامت مخاط سینوس ---
    with st.expander("افزایش ضخامت مخاط سینوس", expanded=True):
        st.write("کدام سینوس‌ها درگیر هستند؟")
        st.checkbox("۱. ماگزیلاری", key="sinus_maxillary")
        st.checkbox("۲. اتموئید", key="sinus_ethmoid")
        st.checkbox("۳. فرونتال", key="sinus_frontal")
        st.checkbox("۴. اسفنوئید", key="sinus_sphenoid")

    # --- 🚀 ۲. انحراف سپتوم بینی (درخواست ۱) ---
    with st.expander("انحراف سپتوم بینی", expanded=True):
        # این دکمه رادیویی اصلی برای شرطی کردن است
        st.radio(
            "وضعیت انحراف سپتوم:",
            ("مشاهده نشد", "مشاهده شد"), # گزینه‌های ساده شده
            horizontal=True,
            key="septum_status" # اتصال به حافظه
        )
        
        # --- بخش شرطی ---
        # این بخش فقط اگر "مشاهده شد" انتخاب شود، ظاهر می‌شود
        if st.session_state.septum_status == "مشاهده شد":
            st.radio(
                "جهت انحراف:",
                ("۱. راست", "۲. چپ", "۳. S-Curve"),
                horizontal=True,
                key="septum_deviation"
            )
            st.radio(
                "ناحیه انحراف:",
                ("۱. استخوانی", "۲. غضروفی", "۳. استخوانی غضروفی"),
                horizontal=True,
                key="septum_area"
            )

    # --- ۳. Nasal Spur ---
    with st.expander("Nasal Spur", expanded=True):
        st.radio(
            "Nasal Spur در سپتوم بینی:",
            ("۱. مشاهده میشود", "۲. مشاهده نمی شود"),
            key="nasal_spur",
            horizontal=True
        )

# === ستون دوم ===
with col2:
    st.subheader("بخش ۲: یافته‌های دیگر")

    # --- ۴. استئوم سینوس ماگزیلاری ---
    with st.expander("استئوم سینوس ماگزیلاری", expanded=True):
        st.radio(
            "وضعیت استئوم:",
            ("۱. باز", "۲. بسته"),
            key="osteum_status",
            horizontal=True
        )

    # --- ۵. Concha Bullosa ---
    with st.expander("Concha Bullosa", expanded=True):
        st.radio(
            "وضعیت Concha Bullosa:",
            ("۱. مشاهده میشود", "۲. مشاهده نمی شود"),
            key="concha_occurrence",
            horizontal=True
        )
        # بخش شرطی برای سمت
        if st.session_state.concha_occurrence == "۱. مشاهده میشود":
            st.radio(
                "در توربینیت میانی کدام سمت؟",
                ("۱. راست", "۲. چپ", "۳. دو طرف"),
                key="concha_side",
                horizontal=True
            )

    # --- ۶. Haller Cells ---
    with st.expander("Haller Cells", expanded=True):
        st.radio(
            "Haller cells در فضای تحتانی اوربیت:",
            ("۱. مشاهده می شود", "۲. مشاهده نمی شود"),
            key="haller_cells",
            horizontal=True
        )

st.divider()

# --- دکمه تولید گزارش ---
if st.button("🚀 تولید گزارش نهایی", type="primary", use_container_width=True):
    
    # --- منطق ساخت متن گزارش (اکنون از session_state می‌خواند) ---
    report_lines = []
    
    report_lines.append("با سلام و احترام")
    report_lines.append("خدمت استاد گرامی")
    report_lines.append("") 
    report_lines.append("در رادیو گرافی CBCT به عمل آمده از بیمار در مقاطع اگزیال و کرونال:")
    report_lines.append("-" * 20) 

    # ۱. منطق سینوس‌ها
    selected_sinuses = []
    if st.session_state.sinus_maxillary: selected_sinuses.append("ماگزیلاری")
    if st.session_state.sinus_ethmoid: selected_sinuses.append("اتموئید")
    if st.session_state.sinus_frontal: selected_sinuses.append("فرونتال")
    if st.session_state.sinus_sphenoid: selected_sinuses.append("اسفنوئید")
    
    if selected_sinuses:
        sinus_text = "، ".join(selected_sinuses)
        report_lines.append(f". افزایش ضخامت مخاط در سینوس {sinus_text} مشاهده می شود.")

    # ۲. منطق انحراف سپتوم (اصلاح شده)
    if st.session_state.septum_status == "مشاهده شد": 
        clean_deviation = st.session_state.septum_deviation.split('. ')[-1]
        clean_area = st.session_state.septum_area.split('. ')[-1]
        report_lines.append(f". انحراف سپتوم بینی به سمت {clean_deviation} در ناحیه {clean_area} مشاهده می گردد.")

    # ۳. منطق Nasal Spur
    clean_spur = st.session_state.nasal_spur.split('. ')[-1]
    report_lines.append(f". در سپتوم بینی Nasal Spur {clean_spur}.")

    # ۴. منطق استئوم
    clean_osteum = st.session_state.osteum_status.split('. ')[-1]
    report_lines.append(f". استئوم سینوس ماگزیلاری {clean_osteum} می باشد.")

    # ۵. منطق Concha Bullosa
    clean_concha_occurrence = st.session_state.concha_occurrence.split('. ')[-1]
    if clean_concha_occurrence == "مشاهده میشود":
        clean_concha_side = st.session_state.concha_side.split('. ')[-1] 
        report_lines.append(f". در توربینیت میانی {clean_concha_side} Conch bullosa مشاهده میشود.")
    else:
        report_lines.append(f". Conch bullosa در توربینیت میانی مشاهده نمی شود.")

    # ۶. منطق Haller Cells
    clean_haller = st.session_state.haller_cells.split('. ')[-1]
    report_lines.append(f". در فضای تحتانی اوربیت Haller cells {clean_haller}.")
    
    # فوتر گزارش
    report_lines.append("-" * 20) 
    report_lines.append("") 
    report_lines.append("با احترام")

    # --- نمایش نتیجه نهایی ---
    final_report_text = "\n".join(report_lines)
    
    # گزارش را در حافظه ذخیره کن تا بعد از بازنشانی هم نمایش داده نشود
    st.session_state.generated_report = final_report_text
    st.success("گزارش با موفقیت تولید شد!")


# --- نمایش گزارش (فقط اگر گزارشی در حافظه موجود باشد) ---
if st.session_state.generated_report:
    st.subheader("✅ گزارش نهایی (آماده کپی کردن)")
    st.markdown(
        f"""
        <textarea style='width:100%; height:350px; direction:rtl; text-align:right;'>{st.session_state.generated_report}</textarea>
        """,
        unsafe_allow_html=True
    )
    st.caption("برای کپی کردن: روی کادر بالا کلیک کنید، (Command+A ⌘A) سپس (Command+C ⌘C)")

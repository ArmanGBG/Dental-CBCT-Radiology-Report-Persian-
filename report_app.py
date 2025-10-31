import streamlit as st

# --- تنظیمات اولیه صفحه ---
st.set_page_config(page_title="مولد گزارش CBCT", layout="wide")

# --- 🚀 اعمال استایل RTL (راست‌چین) ---
# این بخش کلیدی‌ترین بخش برای حل مشکل چیدمان است
st.markdown(
    """
    <style>
    body, .main, .stTextInput, .stTextArea, .stButton>button, .stRadio>label, .stCheckbox>label {
        direction: rtl !important;
        text-align: right !important;
    }
    /* چپ‌چین کردن دکمه‌های رادیویی برای ظاهر بهتر */
    .stRadio>div {
        flex-direction: row-reverse;
        justify-content: flex-end;
        gap: 1rem;
    }
    /* چپ‌چین کردن چک‌باکس‌ها */
    .stCheckbox {
        flex-direction: row-reverse;
        gap: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# --- پایان بخش استایل ---


# --- عنوان برنامه ---
st.title("📄 مولد گزارش رادیوگرافی CBCT")
st.info("لطفاً موارد مشاهده شده در رادیوگرافی را بر اساس فایل PDF انتخاب کنید.")

# --- فرم ورود اطلاعات ---
col1, col2 = st.columns(2)

# === ستون اول ===
with col1:
    st.subheader("بخش ۱: سینوس‌ها و سپتوم")

    # --- ۱. ضخامت مخاط سینوس ---
    with st.expander("افزایش ضخامت مخاط سینوس", expanded=True):
        st.write("کدام سینوس‌ها درگیر هستند؟")
        sinus_maxillary = st.checkbox("۱. ماگزیلاری")
        sinus_ethmoid = st.checkbox("۲. اتموئید")
        sinus_frontal = st.checkbox("۳. فرونتال")
        sinus_sphenoid = st.checkbox("۴. اسفنوئید")

    # --- ۲. انحراف سپتوم بینی ---
    with st.expander("انحراف سپتوم بینی", expanded=True):
        septum_deviation = st.radio(
            "جهت انحراف:",
            ("مشاهده نشد", "۱. راست", "۲. چپ", "۳. S-Curve"),
            horizontal=True
        )
        septum_area = None
        if septum_deviation != "مشاهده نشd":
            septum_area = st.radio(
                "ناحیه انحراف:",
                ("۱. استخوانی", "۲. غضروفی", "۳. استخوانی غضروفی"),
                horizontal=True
            )

    # --- ۳. Nasal Spur ---
    with st.expander("Nasal Spur", expanded=True):
        nasal_spur = st.radio(
            "Nasal Spur در سپتوم بینی:",
            ("۱. مشاهده میشود", "۲. مشاهده نمی شود"),
            index=1,
            horizontal=True
        )

# === ستون دوم ===
with col2:
    st.subheader("بخش ۲: یافته‌های دیگر")

    # --- ۴. استئوم سینوس ماگزیلاری ---
    with st.expander("استئوم سینوس ماگزیلاری", expanded=True):
        osteum_status = st.radio(
            "وضعیت استئوم:",
            ("۱. باز", "۲. بسته"),
            horizontal=True
        )

    # --- ۵. Concha Bullosa ---
    with st.expander("Concha Bullosa", expanded=True):
        concha_occurrence = st.radio(
            "وضعیت Concha Bullosa:",
            ("۱. مشاهده میشود", "۲. مشاهده نمی شود"),
            index=1,
            horizontal=True
        )
        concha_side = None
        if concha_occurrence == "۱. مشاهده میشود":
            concha_side = st.radio(
                "در توربینیت میانی کدام سمت؟",
                ("۱. راست", "۲. چپ", "۳. دو طرف"),
                horizontal=True
            )

    # --- ۶. Haller Cells ---
    with st.expander("Haller Cells", expanded=True):
        haller_cells = st.radio(
            "Haller cells در فضای تحتانی اوربیت:",
            ("۱. مشاهده می شود", "۲. مشاهده نمی شود"),
            index=1,
            horizontal=True
        )

st.divider()

# --- دکمه تولید گزارش ---
if st.button("🚀 تولید گزارش نهایی", type="primary", use_container_width=True):
    
    # --- منطق ساخت متن گزارش ---
    report_lines = []
    
    # هدر گزارش
    report_lines.append("با سلام و احترام")
    report_lines.append("خدمت استاد گرامی")
    report_lines.append("") 
    report_lines.append("در رادیو گرافی CBCT به عمل آمده از بیمار در مقاطع اگزیال و کرونال:")
    report_lines.append("-" * 20) 

    # ۱. منطق سینوس‌ها
    selected_sinuses = []
    if sinus_maxillary: selected_sinuses.append("ماگزیلاری")
    if sinus_ethmoid: selected_sinuses.append("اتموئید")
    if sinus_frontal: selected_sinuses.append("فرونتال")
    if sinus_sphenoid: selected_sinuses.append("اسفنوئید")
    
    if selected_sinuses:
        sinus_text = "، ".join(selected_sinuses)
        report_lines.append(f". افزایش ضخامت مخاط در سینوس {sinus_text} مشاهده می شود.")

    # ۲. منطق انحراف سپتوم
    if septum_area: 
        clean_deviation = septum_deviation.split('. ')[-1]
        clean_area = septum_area.split('. ')[-1]
        report_lines.append(f". انحراف سپتوم بینی به سمت {clean_deviation} در ناحیه {clean_area} مشاهده می گردد.")

    # --- 🚀 بخش اصلاح شده ---
    # ۳. منطق Nasal Spur
    clean_spur = nasal_spur.split('. ')[-1]
    # کلمه "مشاهده" از اینجا حذف شد
    report_lines.append(f". در سپتوم بینی Nasal Spur {clean_spur}.")
    # --- پایان اصلاح ---

    # ۴. منطق استئوم
    clean_osteum = osteum_status.split('. ')[-1]
    report_lines.append(f". استئوم سینوس ماگزیلاری {clean_osteum} می باشد.")

    # ۵. منطق Concha Bullosa
    clean_concha_occurrence = concha_occurrence.split('. ')[-1]
    if clean_concha_occurrence == "مشاهده میشود":
        clean_concha_side = concha_side.split('. ')[-1] 
        report_lines.append(f". در توربینیت میانی {clean_concha_side} Conch bullosa مشاهده میشود.")
    else:
        report_lines.append(f". Conch bullosa در توربینیت میانی مشاهده نمی شود.")

    # --- 🚀 بخش اصلاح شده ---
    # ۶. منطق Haller Cells
    clean_haller = haller_cells.split('. ')[-1]
    # کلمه "مشاهده" از اینجا حذف شد
    report_lines.append(f". در فضای تحتانی اوربیت Haller cells {clean_haller}.")
    # --- پایان اصلاح ---
    
    # فوتر گزارش
    report_lines.append("-" * 20) 
    report_lines.append("") 
    report_lines.append("با احترام")

    # --- نمایش نتیجه نهایی ---
    final_report_text = "\n".join(report_lines)
    
    st.subheader("✅ گزارش نهایی (آماده کپی کردن)")
    st.markdown(
        f"""
        <textarea style='width:100%; height:350px; direction:rtl; text-align:right;'>{final_report_text}</textarea>
        """,
        unsafe_allow_html=True
    )
    st.success("گزارش با موفقیت تولید شد!")
    st.caption("برای کپی کردن: روی کادر بالا کلیک کنید، (Command+A ⌘A) سپس (Command+C ⌘C)")
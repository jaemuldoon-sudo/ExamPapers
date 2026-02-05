import streamlit as st

st.set_page_config(
    page_title="Leaving Cert Maths Tutor",
    page_icon="📘",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------

# Hide the sidebar completely
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
        /* Expand main content to full width */
        .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
<style>

/* Remove Streamlit default padding */
.main > div {
    padding-top: 0rem;
}

/* Hero section */
.hero {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    padding: 4rem 2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 3rem;
}

.hero h1 {
    font-size: 3rem;
    font-weight: 700;
}

.hero p {
    font-size: 1.3rem;
    opacity: 0.9;
}

/* Card container */
.card {
    background: #ffffff;
    padding: 1.8rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: all 0.2s ease;
    border: 1px solid #e6e6e6;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

/* Card title */
.card h3 {
    margin-top: 0;
    font-size: 1.4rem;
    font-weight: 600;
}

/* Card text */
.card p {
    font-size: 1rem;
    color: #555;
}

/* Button styling */
.stButton>button {
    width: 100%;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    font-size: 1rem;
}

</style>
""", unsafe_allow_html=True)

# ------------------ HERO SECTION ------------------
st.markdown("""
<div class="hero">
    <h1>Leaving Cert Maths Tutor</h1>
    <p>Your personalised practice hub for Higher Level Maths</p>
</div>
""", unsafe_allow_html=True)

# ------------------ FEATURE CARDS ------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📝 Worksheets")
    st.write("Generate random, balanced, or topic‑focused worksheets.")
    st.page_link("pages/Worksheets.py", label="Go to Worksheets")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📚 Exam Papers")
    st.write("Create full Paper 1 or Paper 2 with marking schemes.")
    st.page_link("pages/Exam_Papers.py", label="Go to Exam Papers")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📊 Progress (coming soon)")
    st.write("Track your accuracy, weak topics, and improvement over time.")
    st.button("Progress Dashboard", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Built to help you master Leaving Cert Higher Level Maths.")

import streamlit as st
import json
import textwrap
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(page_title="Exam-Style Question Generator", page_icon="📘")

# Hide sidebar for a clean standalone page
st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none; }
        [data-testid="stSidebarNav"] { display: none; }
        .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)



# -----------------------------
# Exam Question Generator
# -----------------------------
def generate_exam_question(topic: str, marks: int):
   system_prompt = (
        "You are a Leaving Cert Higher Level Maths examiner."
        "Generate questions that follow the style, structure, tone, and difficulty of real LC Higher Level exam papers."
        "Requirements:"
        "- Create NEW, original questions. Never quote or reproduce past papers."
        "- Use multi-part structure (a), (b), (c) where appropriate."
        "- Use clear mathematical reasoning and LC-style progression."
        "- ALL mathematical expressions must be valid LaTeX."
        "- Do NOT use $...$ or $$...$$."
        "- Output RAW LaTeX only, suitable for st.latex()."
        "- Never output plain text maths like x^2 or 1/6."
        "- Every mathematical expression must be written in pure LaTeX, e.g.: 2x^2 - 4x - 6 = 0  \frac{1}{6}  \sqrt{x}"
        "- Return exactly 3 exam-style questions, each possibly multi-part."
        "- Do NOT include solutions."

    )

   user_prompt = textwrap.dedent(f"""
        Generate ONE exam-style question for Leaving Cert Higher Level Maths.

        Requirements:
        - Topic: {topic}
        - Total marks: {marks}
        - Structure: multi-part (a), (b), (c)
        - Difficulty: Higher Level
        - Style: similar to real LC HL exam questions but not copied
        - All maths must be valid LaTeX (no $$ or \

\[ \\]

, just the LaTeX)
        - Provide full worked solutions for each part
        - Distribute marks sensibly across parts

        Return ONLY valid JSON in this structure:

        {{
          "total_marks": <int>,
          "topic": "{topic}",
          "difficulty": "Higher Level",
          "parts": [
            {{
              "label": "a",
              "marks": <int>,
              "question": "<LaTeX>",
              "solution": "<LaTeX>"
            }},
            {{
              "label": "b",
              "marks": <int>,
              "question": "<LaTeX>",
              "solution": "<LaTeX>"
            }},
            {{
              "label": "c",
              "marks": <int>,
              "question": "<LaTeX>",
              "solution": "<LaTeX>"
            }}
          ]
        }}

        JSON only. No backticks.
    """)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned:\n{raw}") from e


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Exam-Style Question Generator")
st.write("Generate LC Higher Level exam-style questions with full worked solutions.")

col1, col2 = st.columns(2)

with col1:
    topic = st.selectbox(
        "Choose a topic:",
        [
            "Algebra",
            "Calculus",
            "Trigonometry",
            "Complex Numbers",
            "Probability",
            "Functions",
            "Geometry",
            "Sequences & Series",
            "Financial Maths",
        ],
    )

with col2:
    marks = st.selectbox("Total marks:", [25, 50, 75])

if "exam_question" not in st.session_state:
    st.session_state.exam_question = None


def render_question(data):
    st.subheader("Question")
    for part in data["parts"]:
        st.markdown(f"**({part['label']}) [{part['marks']} marks]**")
        st.latex(part["question"])


def render_solution(data):
    st.subheader("Solution")
    for part in data["parts"]:
        st.markdown(f"**Solution ({part['label']})**")
        st.latex(part["solution"])


colA, colB = st.columns([2, 1])

with colA:
    if st.button("Generate Question", use_container_width=True):
        with st.spinner("Generating exam-style question..."):
            st.session_state.exam_question = generate_exam_question(topic, marks)

with colB:
    if st.session_state.exam_question is not None:
        if st.button("More Like This", use_container_width=True):
            with st.spinner("Generating similar question..."):
                st.session_state.exam_question = generate_exam_question(topic, marks)


if st.session_state.exam_question:
    st.divider()
    render_question(st.session_state.exam_question)
    st.divider()
    render_solution(st.session_state.exam_question)





# -----------------------------
# TOPICS + SUBTOPICS
# -----------------------------
TOPICS = ["Probability", "Trigonometry", "Algebra", "Circle", "Calculus"]

SUBTOPICS = {
    "Probability": [
        "Combined events",
        "Conditional probability",
        "Expected value",
        "Permutations and combinations",
        "Binomial distribution",
        "Bernoulli Trials",
        "Normal Distribution"
    ],
    "Trigonometry": [
        "Trig identities",
        "Trig equations",
        "Graphs",
        "Radians",
        "Sine rule / Cosine rule",
        "Unit Circle"
    ],
    "Algebra": [
        "Quadratics",
        "Functions",
        "Logs",
        "Sequences & series",
        "Inequalities"
    ],
    "Circle": [
        "Center (0,0) and radius r",
        "Center (h,k) and radius r",
        "Equations of the form x^2 +y^2 + 2gx + 2gy + c = 0",
        "Points outside, inside or on the Circle",
        "Intersection of a line and circle"
    ],
    "Calculus": [
        "Differentiation",
        "Integration",
        "Rates of change",
        "Area under curves",
        "Product/Quotient/Chain rule"
    ]
}

# -----------------------------
# OPENAI CALL
# -----------------------------
def call_openai(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response.choices[0].message.content


# -----------------------------
# WORKSHEET GENERATORS
# -----------------------------
def generate_worksheet(topic, subtopics, difficulty):
    chosen = ", ".join(subtopics)

    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Generate exactly 10 unique exam‑style questions. "
        f"Difficulty level: {difficulty}. "
        f"Focus ONLY on these subtopics: {chosen}. "
        "Use LaTeX formatting for ALL mathematical expressions. "
        "Use ONLY inline LaTeX with single dollar signs: $ ... $."
        "Wrap EVERY LaTeX expression in $$ ... $$. "
        "Never use $$ ... $$ under any circumstances."
        "Never output plain text maths such as x^2, 1/6, sqrt(x), etc."
        "Every mathematical expression must be inside $ ... $."
        "Do NOT output plain text maths like x^2 or 1/6. "
        "Return the questions as a numbered list, one per line, no solutions."

    )

    user_prompt = (
        f"Create a {difficulty} worksheet on {topic}. "
        f"Subtopics: {chosen}. "
        "Ensure ALL maths is in LaTeX wrapped in $$ ... $$."
    )

    text = call_openai(system_prompt, user_prompt)
    return [q.strip() for q in text.split("\n") if q.strip()]


def generate_balanced_worksheet(topic, subtopics):
    chosen = ", ".join(subtopics)

    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Generate ONE exam‑style question for EACH selected subtopic. "
        "Use LaTeX formatting wrapped in $$ ... $$. "
        "Use ONLY inline LaTeX with single dollar signs: $ ... $."
        "Wrap EVERY LaTeX expression in $$ ... $$. "
        "Never use $$ ... $$ under any circumstances."
        "Never output plain text maths such as x^2, 1/6, sqrt(x), etc."
        "Every mathematical expression must be inside $ ... $."
        "Do NOT output plain text maths like x^2 or 1/6. "
        "Return a numbered list, no solutions."
    )

    user_prompt = f"Topic: {topic}\nSubtopics: {chosen}"

    text = call_openai(system_prompt, user_prompt)
    return [q.strip() for q in text.split("\n") if q.strip()]


def generate_answer(question, topic, difficulty):
    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Provide a full step‑by‑step worked solution. "
        "Use LaTeX formatting wrapped in $$ ... $$. "
        "Use ONLY inline LaTeX with single dollar signs: $ ... $."
        "Wrap EVERY LaTeX expression in $$ ... $$. "
        "Never use $$ ... $$ under any circumstances."
        "Never output plain text maths such as x^2, 1/6, sqrt(x), etc."
        "Every mathematical expression must be inside $ ... $."
        "Do NOT output plain text maths like x^2 or 1/6. "
        f"Match the difficulty: {difficulty}."
    )

    user_prompt = f"Topic: {topic}\nQuestion: {question}"

    return call_openai(system_prompt, user_prompt)


def generate_similar_question(question, topic, difficulty):
    system_prompt = (
        "You are a Leaving Cert Higher Level Maths tutor. "
        "Generate ONE new question similar in style and difficulty "
        "but not identical. "
        "Use LaTeX formatting wrapped in $$ ... $$. "
        "Use ONLY inline LaTeX with single dollar signs: $ ... $."
        "Wrap EVERY LaTeX expression in $$ ... $$. "
        "Never use $$ ... $$ under any circumstances."
        "Never output plain text maths such as x^2, 1/6, sqrt(x), etc."
        "Every mathematical expression must be inside $ ... $."
        "Do NOT output plain text maths like x^2 or 1/6. "
        "No solution."
    )

    user_prompt = f"Topic: {topic}\nOriginal question: {question}"

    return call_openai(system_prompt, user_prompt)


def generate_exam_style_worksheet(topic, subtopics):
    chosen = ", ".join(subtopics)

    system_prompt = (
        "You are a Leaving Cert Higher Level Maths examiner. "
        "Generate questions that follow the style, structure, tone, and difficulty "
        "of real LC Higher Level exam papers. "
        "Base your style on typical LC question formats, multi‑part structure, "
        "mark‑style progression, and the level of mathematical rigor expected. "
        "You may include multi‑part questions (a), (b), (c). "
        "You may include diagrams described in words. "
        "Do NOT quote or reproduce any past exam paper. "
        "Only create new, original questions inspired by the general LC style. "
        "Use LaTeX formatting for ALL mathematical expressions, wrapped in $$ ... $$. "
        "Use ONLY inline LaTeX with single dollar signs: $ ... $."
        "Wrap EVERY LaTeX expression in $$ ... $$. "
        "Never use $$ ... $$ under any circumstances."
        "Never output plain text maths such as x^2, 1/6, sqrt(x), etc."
        "Every mathematical expression must be inside $ ... $."
        "Do NOT output plain text maths like x^2 or 1/6. "
        "Return exactly 3 exam‑style questions, each possibly multi‑part, no solutions."
    )

    user_prompt = (
        f"Topic: {topic}\n"
        f"Subtopics: {chosen}\n"
        "Generate 3 exam‑style questions."
    )

    text = call_openai(system_prompt, user_prompt)
    return [q.strip() for q in text.split("\n") if q.strip()]




# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="LC Maths Tutor", layout="centered")

# -----------------------------
# BRAND HEADER
# -----------------------------
st.markdown(
    """
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <h1 style="margin-bottom:0;">📘 LC Maths Tutor</h1>
        <p style="color:#4a4a4a; font-size:18px; margin-top:5px;">
            Adaptive, exam‑style practice — built for students.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# TOPIC + SUBTOPICS
# -----------------------------
st.markdown("### Choose Your Topic")
topic = st.selectbox("", TOPICS)

st.markdown("### Choose Subtopics")
subtopics = st.multiselect(
    "",
    SUBTOPICS.get(topic, []),
    placeholder="Pick 1–5 subtopics"
)

st.markdown("---")

# -----------------------------
# SESSION STATE
# -----------------------------
if "questions" not in st.session_state:
    st.session_state.questions = []
if "difficulty" not in st.session_state:
    st.session_state.difficulty = []
if "similar_questions" not in st.session_state:
    st.session_state.similar_questions = {}


# -----------------------------
# WORKSHEET BUTTONS (MOBILE‑FIRST)
# -----------------------------
st.markdown("### Generate Worksheet")

# Row 1 — Difficulty
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Easy", use_container_width=True):
        st.session_state.difficulty = "Easy"
        st.session_state.questions = generate_worksheet(topic, subtopics, "Easy")

with c2:
    if st.button("Medium", use_container_width=True):
        st.session_state.difficulty = "Medium"
        st.session_state.questions = generate_worksheet(topic, subtopics, "Medium")

with c3:
    if st.button("Hard", use_container_width=True):
        st.session_state.difficulty = "Hard"
        st.session_state.questions = generate_worksheet(topic, subtopics, "Hard")

# Row 2 — Random / Balanced / Exam Style
c4, c5, c6 = st.columns(3)

with c4:
    if st.button("Random", use_container_width=True):
        import random
        diff = random.choice(["Easy", "Medium", "Hard"])
        st.session_state.difficulty = diff
        st.session_state.questions = generate_worksheet(topic, subtopics, diff)

with c5:
    if st.button("Balanced", use_container_width=True):
        # st.session_state.difficulty = "Balanced"
        st.session_state.questions = generate_balanced_worksheet(topic, subtopics)

with c6:
    if st.button("Exam Style", use_container_width=True):
        st.session_state.difficulty = "Exam Style"
        st.session_state.questions = generate_exam_style_worksheet(topic, subtopics)


st.markdown("---")

# -----------------------------
# DISPLAY WORKSHEET
# -----------------------------
questions = st.session_state.questions
difficulty = st.session_state.difficulty

if questions:
    st.markdown(
        f"""
        <h2 style="margin-bottom:0;">{topic} Worksheet</h2>
        <p style="color:#6a6a6a; margin-top:0;">
            Mode: <strong>{difficulty}</strong>
        </p>
        """,
        unsafe_allow_html=True
    )

    if subtopics:
        st.caption("Subtopics: " + ", ".join(subtopics))

    for i, q in enumerate(questions):
        st.markdown(
            f"""
            <div style="
                background:#f7f9fc;
                padding:18px;
                border-radius:10px;
                margin-bottom:15px;
                border:1px solid #e3e6eb;
            ">
                <h4 style="margin-top:0;">Question {i+1}</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(q)

        b1, b2 = st.columns(2)

        with b1:
            if st.button(f"Show Answer", key=f"ans_{i}", use_container_width=True):
                ans = generate_answer(q, topic, difficulty)
                st.markdown(ans)

        with b2:
            if st.button(f"More Like This", key=f"more_{i}", use_container_width=True):
                sim = generate_similar_question(q, topic, difficulty)
                st.markdown("**Another question like this:**")
                st.markdown(sim)

else:
    st.info("Choose a topic, pick subtopics, and select a worksheet mode to begin.")

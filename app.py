# numerology_app.py
# Complete Pythagorean Numerology Web App using Streamlit
# Author: ChatGPT (Senior Python Dev)

import streamlit as st
import pandas as pd
import re
import datetime
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib.pagesizes import A4
import os
import time
import streamlit.components.v1 as components




# --------------------------- CONFIG ---------------------------
st.set_page_config(
    page_title="Numerology Analyzer",
    layout="centered",
    initial_sidebar_state="collapsed"
)

DATA_FILE = "history.csv"

# --------------------------- PYTHAGOREAN MAPPING ---------------------------
LETTER_MAP = {
    1: list("AJS"),
    2: list("BKT"),
    3: list("CLU"),
    4: list("DMV"),
    5: list("ENW"),
    6: list("FOX"),
    7: list("GPY"),
    8: list("HQZ"),
    9: list("IR")
}

# Reverse Mapping
REVERSE_MAP = {}
for k, v in LETTER_MAP.items():
    for ch in v:
        REVERSE_MAP[ch] = k

VOWELS = "AEIOU"

# --------------------------- COMPATIBILITY CHART ---------------------------
COMPATIBILITY = {
    1: {"friends": [2, 3, 9], "enemies": [8]},
    2: {"friends": [1, 4, 7], "enemies": [8]},
    3: {"friends": [1, 5, 6], "enemies": [4]},
    4: {"friends": [2, 6, 8], "enemies": [3]},
    5: {"friends": [3, 7, 9], "enemies": [4]},
    6: {"friends": [3, 5, 9], "enemies": [1]},
    7: {"friends": [2, 5], "enemies": [8]},
    8: {"friends": [4, 6], "enemies": [1, 2]},
    9: {"friends": [1, 3, 6], "enemies": [4, 8]},
}

# --------------------------- MEANING DATABASE ---------------------------
NUMBER_MEANINGS = {
    1: {
        "title": "Leader",
        "strengths": "Independent, ambitious, confident",
        "weaknesses": "Ego, impatience",
        "career": "Entrepreneur, Manager, Politician",
        "relationship": "Dominant but loyal",
        "advice": "Learn cooperation"
    },
    2: {
        "title": "Diplomat",
        "strengths": "Sensitive, cooperative",
        "weaknesses": "Over-emotional",
        "career": "Counselor, HR",
        "relationship": "Caring and emotional",
        "advice": "Build confidence"
    },
    3: {
        "title": "Creative",
        "strengths": "Expressive, joyful",
        "weaknesses": "Scattered",
        "career": "Artist, Writer",
        "relationship": "Romantic",
        "advice": "Stay focused"
    },
    4: {
        "title": "Builder",
        "strengths": "Disciplined, loyal",
        "weaknesses": "Rigid",
        "career": "Engineer, Admin",
        "relationship": "Stable",
        "advice": "Be flexible"
    },
    5: {
        "title": "Explorer",
        "strengths": "Adaptable, energetic",
        "weaknesses": "Restless",
        "career": "Marketing, Travel",
        "relationship": "Freedom-loving",
        "advice": "Practice discipline"
    },
    6: {
        "title": "Nurturer",
        "strengths": "Responsible, loving",
        "weaknesses": "Overprotective",
        "career": "Teacher, Doctor",
        "relationship": "Family oriented",
        "advice": "Balance giving"
    },
    7: {
        "title": "Thinker",
        "strengths": "Analytical, spiritual",
        "weaknesses": "Isolated",
        "career": "Research, IT",
        "relationship": "Reserved",
        "advice": "Trust people"
    },
    8: {
        "title": "Powerhouse",
        "strengths": "Managerial, wealthy",
        "weaknesses": "Materialistic",
        "career": "Business, Finance",
        "relationship": "Strong-willed",
        "advice": "Practice humility"
    },
    9: {
        "title": "Humanitarian",
        "strengths": "Generous, wise",
        "weaknesses": "Over-sacrificing",
        "career": "NGO, Teaching",
        "relationship": "Compassionate",
        "advice": "Set boundaries"
    },
    11: {
        "title": "Master Intuitive",
        "strengths": "Visionary, spiritual",
        "weaknesses": "Anxiety",
        "career": "Guide, Healer",
        "relationship": "Deep emotional",
        "advice": "Ground yourself"
    },
    22: {
        "title": "Master Builder",
        "strengths": "Practical visionary",
        "weaknesses": "Pressure",
        "career": "Architect, Leader",
        "relationship": "Supportive",
        "advice": "Delegate"
    },
    33: {
        "title": "Master Teacher",
        "strengths": "Compassionate",
        "weaknesses": "Self-neglect",
        "career": "Mentor",
        "relationship": "Unconditional love",
        "advice": "Self-care"
    }
}

# --------------------------- REMEDY DATABASE ---------------------------
REMEDIES = {
    1: ["Leadership practice", "Morning sunlight", "Goal journaling"],
    2: ["Meditation", "Listening to music", "Moonlight walks"],
    3: ["Creative writing", "Public speaking", "Art practice"],
    4: ["Routine building", "Grounding exercises", "Yoga"],
    5: ["Travel planning", "Breathing exercises", "Nature walks"],
    6: ["Family time", "Gratitude journaling", "Volunteering"],
    7: ["Meditation", "Spiritual reading", "Silence practice"],
    8: ["Financial planning", "Discipline habits", "Charity"],
    9: ["Helping others", "Donation", "Forgiveness practice"],
    11: ["Visualization", "Prayer", "Mindfulness"],
    22: ["Long-term planning", "Mentorship", "Service"],
    33: ["Teaching", "Healing practices", "Community work"]
}

UNIVERSAL_REMEDIES = [
    "Daily meditation (10 minutes)",
    "Positive affirmations",
    "Regular charity",
    "Gratitude practice"
]


# --------------------------- UTILITIES ---------------------------

def reduce_number(num):
    """Reduce number with master number preservation (for main numerology)"""
    while num not in [11, 22, 33] and num > 9:
        num = sum(map(int, str(num)))
    return num


def reduce_to_single(num):
    """Force reduce to 1–9 (for compatibility only)"""
    while num > 9:
        num = sum(map(int, str(num)))
    return num


def clean_name(name):
    return re.sub(r"[^A-Za-z ]", "", name).upper()


def name_to_number(name, mode="all"):
    total = 0
    for ch in name.replace(" ", ""):
        if ch in REVERSE_MAP:
            if mode == "vowel" and ch not in VOWELS:
                continue
            if mode == "consonant" and ch in VOWELS:
                continue
            total += REVERSE_MAP[ch]
    return reduce_number(total)


def calculate_life_path(dob):
    s = dob.strftime("%d%m%Y")
    total = sum(map(int, s))
    return reduce_number(total)


def calculate_mobile(num):
    return reduce_number(sum(map(int, num)))


def personal_year(dob, year):
    d = sum(map(int, dob.strftime("%d%m")))
    y = sum(map(int, str(year)))
    return reduce_number(d + y)


def compatibility_status(a, b):
    """Compatibility check (force reduce to 1–9)"""

    # Force reduce (ignore master numbers here)
    a = reduce_to_single(a)
    b = reduce_to_single(b)

    if b in COMPATIBILITY[a]["friends"]:
        return "Supportive"
    elif b in COMPATIBILITY[a]["enemies"]:
        return "Conflicting"
    else:
        return "Neutral"


def suggest_name_correction(name, target):
    suggestions = []
    base = name_to_number(name)

    for letter, val in REVERSE_MAP.items():
        new_val = reduce_number(base + val)
        if new_val == target:
            suggestions.append(name + letter)

    if "H" not in name:
        suggestions.append(name + "H")

    return suggestions[:3]

# --------------------------- PDF EXPORT ---------------------------

# def generate_pdf(report_text, filename):
#     doc = SimpleDocTemplate(filename, pagesize=A4)
#     styles = getSampleStyleSheet()
#     story = []

#     for line in report_text.split("\n"):
#         story.append(Paragraph(line, styles["Normal"]))
#         story.append(Spacer(1, 10))

#     story.append(PageBreak())
#     doc.build(story)

# --------------------------- STORAGE ---------------------------

def save_history(data):
    df = pd.DataFrame([data])

    if os.path.exists(DATA_FILE):
        df_old = pd.read_csv(DATA_FILE)
        df = pd.concat([df_old, df], ignore_index=True)

    df.to_csv(DATA_FILE, index=False)

# --------------------------- UI ---------------------------
st.markdown('<div id="top"></div>', unsafe_allow_html=True)
st.title("🔢 Numerology Analysis System")

st.markdown("Professional Pythagorean Numerology Analyzer")
st.markdown("---")

# Inputs
with st.form("user_form"):

    name = st.text_input("Name (as per documents)")

    dob = st.date_input(
        "Date of Birth",
        min_value=datetime.date(1960, 1, 1),
        max_value=datetime.date.today()
    )

    mobile = st.text_input("Mobile Number (10 digits)")

    current_year = st.number_input(
        "Current Year",
        value=datetime.date.today().year,
        min_value=1900,
        max_value=2100
    )

    # save_data = st.checkbox("Can we save your data in our database?", value=True)
    st.write("FYI 👉 We Don't Store Any Data.")

    submit = st.form_submit_button("Generate Report")

# --------------------------- VALIDATION ---------------------------

if submit:

    errors = []

    if not re.match(r"^[A-Za-z ]+$", name):
        errors.append("Name must contain only letters and spaces")

    if not re.match(r"^[0-9]{10}$", mobile):
        errors.append("Mobile number must be 10 digits")

    if errors:
        for e in errors:
            st.error(e)
        st.stop()

    name = clean_name(name)
    #---------------------------- Progress BAR ---------------------------
    status = st.empty()
    bar = st.progress(0)

    steps = [
        ("Validating inputs...", 20),
        ("Calculating numbers...", 40),
        ("Analyzing compatibility...", 60),
        ("Generating report...", 80),
        ("Finalizing...", 100)
    ]

    for msg, pct in steps:
        status.info(f"🔄 {msg}")
        bar.progress(pct)
        time.sleep(0.7)

    status.success("✅ Report generated successfully")
    bar.empty()
    # --------------------------- CALCULATIONS ---------------------------

    life_path = calculate_life_path(dob)
    destiny = name_to_number(name)
    soul = name_to_number(name, "vowel")
    personality = name_to_number(name, "consonant")
    mobile_num = calculate_mobile(mobile)
    pyear = personal_year(dob, current_year)

    # Compatibility
    c1 = compatibility_status(life_path, destiny)
    c2 = compatibility_status(life_path, mobile_num)
    c3 = compatibility_status(life_path, pyear)

    # Conflict detection
    conflicts = []
    if c1 == "Conflicting":
        conflicts.append("Life Path vs Destiny")
    if c2 == "Conflicting":
        conflicts.append("Life Path vs Mobile")
    if c3 == "Conflicting":
        conflicts.append("Life Path vs Personal Year")

    # Name correction
    corrections = []
    if conflicts:
        corrections = suggest_name_correction(name, life_path)

    # --------------------------- REPORT ---------------------------

    st.header("📌 Personal Profile")

    col1, col2 = st.columns(2)

    col1.metric("Life Path", life_path, help="Calculated as: SUM(DOB)")
    col1.metric("Destiny", destiny, help="Calculated as: SUM(Name Letter -> Mapped Number)")
    col1.metric("Soul Urge", soul, help="Calculated as: SUM(Vowel Letters Only)")

    col2.metric("Personality", personality, help="Calculated as: SUM(Consonants Letters Only)")
    col2.metric("Mobile Vibration", mobile_num, help="Calculated as: SUM(Mobile number digits)")
    col2.metric("Personal Year", pyear, help="Calculated as: DOB Day + Month + Current Year")
    # col2.markdown("""
    #         <span title="DOB Day + Month + Current Year">
    #         <b>Personal Year</b> ℹ️
    #         </span>
    #         """, unsafe_allow_html=True)

    main_meaning = NUMBER_MEANINGS.get(life_path)

    st.subheader("Core Nature: " + main_meaning["title"])
    st.write("**Strengths:**", main_meaning["strengths"])
    st.write("**Weaknesses:**", main_meaning["weaknesses"])

    st.header("💼 Career & Finance")
    st.write("**Career Indication:**", main_meaning["career"])
    st.write("**Financial Tendency:** Stable with discipline")

    st.header("❤️ Relationship Pattern")
    st.write("**Traits:**", main_meaning["relationship"])

    st.header("⚖️ Compatibility Analysis")

    st.write(f"Life Path vs Destiny: {c1}")
    st.write(f"Life Path vs Mobile: {c2}")
    st.write(f"Life Path vs Personal Year: {c3}")

    if conflicts:
        st.error("Conflicts Found: " + ", ".join(conflicts))
    else:
        st.success("No major conflicts detected")

    if corrections:
        st.header("✏️ Name Correction Suggestions")
        for s in corrections:
            st.write("👉", s)

    st.header("📅 Current Year Guidance")
    st.write("Personal Year Advice:", NUMBER_MEANINGS[pyear]["advice"] if pyear in NUMBER_MEANINGS else "Focus and grow")

    # --------------------------- DYNAMIC REMEDIES ---------------------------

    st.header("🌿 Remedies")

    problem_numbers = []
    reasons = []

    if c1 == "Conflicting":
        problem_numbers.append(destiny)
        reasons.append(f"Destiny ({destiny}) conflicts with Life Path ({life_path})")

    if c2 == "Conflicting":
        problem_numbers.append(mobile_num)
        reasons.append(f"Mobile ({mobile_num}) conflicts with Life Path ({life_path})")

    if pyear in [4, 7, 8]:
        problem_numbers.append(pyear)
        reasons.append(f"Personal Year ({pyear}) is challenging")

    def get_remedies(nums):
        result = set()
        for n in nums:
            result.update(REMEDIES.get(n, []))
        return list(result)[:5]

    dynamic_remedies = get_remedies(problem_numbers)
    final_remedies = dynamic_remedies + UNIVERSAL_REMEDIES

    if reasons:
        for r in reasons:
            st.write("🔍", r)

    if final_remedies:
        for r in final_remedies:
            st.write("✅", r)
    else:
        st.write("✅ Maintain your positive lifestyle")

    st.markdown("---")

    st.info("Disclaimer:This app is for self-reflection and educational purposes. It does not guarantee future outcomes.")
    st.markdown("---")
    
    st.info("Thank You! Please Do subscribe our YouTube Channel." )
    st.markdown(" <a href="https://youtube.com/@pyshaala">https://youtubeoutube/@Pyshaala</a> ", unsafe_allow_html=True)

    # --------------------------- TEXT REPORT ---------------------------

    report_text = f"""
    Numerology Report
    -----------------------------
    Name: {name}
    DOB: {dob}

    Life Path: {life_path}
    Destiny: {destiny}
    Soul Urge: {soul}
    Personality: {personality}
    Mobile: {mobile_num}
    Personal Year: {pyear}

    Core Nature: {main_meaning['title']}
    Strengths: {main_meaning['strengths']}
    Weaknesses: {main_meaning['weaknesses']}

    Career: {main_meaning['career']}
    Relationship: {main_meaning['relationship']}

    Compatibility: {c1}, {c2}, {c3}

    Conflicts: {', '.join(conflicts) if conflicts else 'None'}

    Advice: {main_meaning['advice']}

    Disclaimer: {"This app is for self-reflection and educational purposes. It does not guarantee future outcomes."}

    App Developed By: {"@Pyshaala | 2026 V1 | Please Subscribe us on youtube." }
    """

    # --------------------------- PDF EXPORT ---------------------------

    # pdf_file = "numerology_report.pdf"
    # generate_pdf(report_text, pdf_file)

    # with open(pdf_file, "rb") as f:
    #     st.download_button("📄 Download PDF Report", f, file_name=pdf_file)
        

    # --------------------------- SAVE HISTORY ---------------------------
    save_data = False
    if save_data:
        data = {
            "Name": name,
            "DOB": dob,
            "Mobile": mobile,
            "LifePath": life_path,
            "Destiny": destiny,
            "Soul": soul,
            "Personality": personality,
            "MobileNum": mobile_num,
            "PersonalYear": pyear,
            "Conflicts": ",".join(conflicts)
        }

        save_history(data)
        # st.success("Data saved successfully")
st.markdown("---")
# --------------------------- HISTORY VIEW ---------------------------
# st.subheader("📊 Previous Reports")

# if os.path.exists(DATA_FILE):
#     df = pd.read_csv(DATA_FILE)
#     st.dataframe(df, use_container_width=True)
# else:
#     st.write("No history available yet")


st.markdown("""
<style>
.go-top-btn {
    position: fixed;
    bottom: 75px;
    right: 20px;
    background: #ff4b4b;
    color: white;
    padding: 10px 14px;
    border-radius: 50%;
    text-decoration: none;
    font-size: 18px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.go-top-btn:hover {
    background: #ff2b2b;
}
</style>

<a href="#top" class="go-top-btn">⬆️</a>
""", unsafe_allow_html=True)



######FOOTER###########
def show_footer():

    footer = """
    <style>

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #ffffff;
        text-align: center;
        padding: 12px 10px;
        font-size: 14px;
        z-index: 1000;
        border-top: 1px solid #333;
    }

    .footer a {
        color: #4da6ff;
        text-decoration: none;
        margin: 0 10px;
        font-weight: 500;
    }

    .footer a:hover {
        text-decoration: underline;
        color: #66ccff;
    }

    </style>

    <div class="footer">
        © 2026 Numerology Analysis System | Developed by <b>PyShaala</b> 🚀 |
        <!--<a href="https://linkedin.com" target="_blank">LinkedIn</a>
        <a href="https://github.com" target="_blank">GitHub</a>-->
        <a href="https://instagram.com/pyshaala" target="_blank">Instagram</a> 
        <a href="https://youtube.com/@pyshaala">Youtube</a>
    </div>
    """

    st.markdown(footer, unsafe_allow_html=True)






#calliing footer
show_footer()
st.markdown(
    "<div style='margin-bottom:70px;'></div>",
    unsafe_allow_html=True

)



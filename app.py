import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------------
# Basic App Config
# ----------------------------
st.set_page_config(
    page_title="Vote-Xpress Web",
    page_icon="🗳️",
    layout="centered",
)

APP_TITLE = "Vote-Xpress: Online Voting System"
DEVELOPER_NAME = "Aditya Raj"
DEVELOPER_LINKEDIN = "https://www.linkedin.com/in/aditya-raj-a73319282/"

CANDIDATES = ["Candidate A", "Candidate B", "Candidate C"]

# ----------------------------
# Initialize Session State
# ----------------------------
if "votes" not in st.session_state:
    st.session_state.votes = {c: 0 for c in CANDIDATES}

if "voted_users" not in st.session_state:
    # store (name, voter_id) tuples to avoid duplicate votes
    st.session_state.voted_users = set()

if "feedback_list" not in st.session_state:
    st.session_state.feedback_list = []

if "registered_users" not in st.session_state:
    # dict: voter_id -> name
    st.session_state.registered_users = {}

# ----------------------------
# Helper: Nice Title
# ----------------------------
def app_header():
    st.markdown(
        f"<h1 style='text-align:center;color:#0055A4;'>{APP_TITLE}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center;font-size:16px;'>Digital, simple, and demo-ready for projects & CV 🚀</p>",
        unsafe_allow_html=True,
    )
    st.write("---")

# ----------------------------
# PAGES
# ----------------------------

def page_home():
    app_header()
    st.subheader("🏠 Home")

    st.write(
        """
        Welcome to **Vote-Xpress Web Edition** – an online demo of your voting system.

        This version is built using **Streamlit** so it can run in a web browser and be
        shared as a link on your **CV**, **LinkedIn**, or **GitHub**.
        """
    )

    total_votes = sum(st.session_state.votes.values())
    st.metric("Total Votes Cast", total_votes)

    st.write("### Current Vote Distribution")
    df = pd.DataFrame(
        {"Candidate": list(st.session_state.votes.keys()),
         "Votes": list(st.session_state.votes.values())}
    )
    st.bar_chart(df.set_index("Candidate"))

    st.info(
        "Use the sidebar on the left to **Register**, **Vote**, view **Live Results**, "
        "take the **Quiz**, give **Feedback**, or see **Developer Info**."
    )


def page_register():
    app_header()
    st.subheader("📝 Voter Registration")

    st.write("Fill in your details to register as a voter (demo only, stored in session).")

    with st.form("register_form"):
        name = st.text_input("Full Name")
        voter_id = st.text_input("Voter ID")
        submit = st.form_submit_button("Register")

    if submit:
        if not name.strip() or not voter_id.strip():
            st.warning("Please fill in both Name and Voter ID.")
        else:
            st.session_state.registered_users[voter_id.strip()] = name.strip()
            st.success(f"✅ {name} registered successfully with Voter ID: {voter_id}.")


def page_vote():
    app_header()
    st.subheader("🗳️ Cast Your Vote")

    st.write("Please enter your details and cast your vote.")

    name = st.text_input("Full Name")
    voter_id = st.text_input("Voter ID")

    candidate = st.radio("Select Candidate", CANDIDATES)

    if st.button("Submit Vote"):
        name_clean = name.strip()
        voter_id_clean = voter_id.strip()

        if not name_clean or not voter_id_clean:
            st.warning("Please fill in both Name and Voter ID before voting.")
            return

        key = (name_clean, voter_id_clean)
        if key in st.session_state.voted_users:
            st.error("❌ You have already voted. Duplicate votes are not allowed.")
            return

        # Optional: Check if voter is registered
        # if voter_id_clean not in st.session_state.registered_users:
        #     st.warning("This Voter ID is not registered. Please register first.")
        #     return

        st.session_state.voted_users.add(key)
        st.session_state.votes[candidate] += 1

        st.success(f"✅ Thank you, {name_clean}! Your vote for **{candidate}** has been recorded.")

        with st.expander("View Vote Receipt"):
            st.write(f"**Voter Name:** {name_clean}")
            st.write(f"**Voter ID:** {voter_id_clean}")
            st.write(f"**Voted For:** {candidate}")
            st.write("🇮🇳 *Your participation strengthens our democracy.*")


def page_results():
    app_header()
    st.subheader("📊 Live Voting Results")

    votes = st.session_state.votes
    total_votes = sum(votes.values())

    if total_votes == 0:
        st.info("No votes have been cast yet. Encourage some users to vote first!")
        return

    df = pd.DataFrame(
        {"Candidate": list(votes.keys()),
         "Votes": list(votes.values())}
    )

    st.write("### Vote Chart")
    st.bar_chart(df.set_index("Candidate"))

    st.write("### Detailed Counts")
    st.table(df)

    # Determine winner
    winner = max(votes.items(), key=lambda x: x[1])
    st.success(f"🏆 Leading Candidate: **{winner[0]}** with **{winner[1]}** votes.")

    st.caption(f"Last updated at: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")


# ----------------------------
# Simple Quiz
# ----------------------------
QUIZ_QUESTIONS = [
    {
        "q": "What is the minimum age to vote in India?",
        "options": ["16 years", "18 years", "21 years", "25 years"],
        "answer": "18 years",
    },
    {
        "q": "Who conducts elections in India?",
        "options": [
            "Supreme Court",
            "Election Commission of India",
            "Parliament",
            "Prime Minister Office",
        ],
        "answer": "Election Commission of India",
    },
    {
        "q": "What does NOTA stand for?",
        "options": [
            "None Of The Above",
            "National Online Tracking Authority",
            "New Order of Transparent Administration",
            "National Organization for Transparent Actions",
        ],
        "answer": "None Of The Above",
    },
]


def page_quiz():
    app_header()
    st.subheader("🧠 VoteSmart Quiz Challenge")

    st.write(
        "Test your basic knowledge about elections and democracy. "
        "Good for showing extra features on your CV 😉"
    )

    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}

    with st.form("quiz_form"):
        for i, q in enumerate(QUIZ_QUESTIONS):
            st.markdown(f"**Q{i+1}. {q['q']}**")
            choice = st.radio(
                "Your answer:",
                q["options"],
                key=f"quiz_q_{i}",
            )
            st.session_state.quiz_answers[i] = choice
            st.write("---")

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        score = 0
        for i, q in enumerate(QUIZ_QUESTIONS):
            if st.session_state.quiz_answers.get(i) == q["answer"]:
                score += 1

        st.success(f"Your Score: {score} / {len(QUIZ_QUESTIONS)}")

        if score == len(QUIZ_QUESTIONS):
            st.balloons()
            st.info("🏅 Badge: Voting Champion!")
        elif score >= 2:
            st.info("🎖 Badge: Democracy Defender!")
        else:
            st.info("📚 Badge: Civic Learner – Keep improving!")


def page_feedback():
    app_header()
    st.subheader("💬 Feedback")

    st.write("Share your thoughts about Vote-Xpress Web Demo.")

    name = st.text_input("Your Name (optional)")
    feedback_text = st.text_area("Your Feedback")

    if st.button("Submit Feedback"):
        fb = {
            "name": name.strip() if name.strip() else "Anonymous",
            "feedback": feedback_text.strip(),
            "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
        if not feedback_text.strip():
            st.warning("Please write some feedback before submitting.")
        else:
            st.session_state.feedback_list.append(fb)
            st.success("✅ Thank you for your feedback!")

    if st.session_state.feedback_list:
        st.write("### Previous Feedback")
        for fb in reversed(st.session_state.feedback_list[-10:]):
            st.markdown(f"**{fb['name']}**  \n_{fb['time']}_")
            st.write(f"💭 {fb['feedback']}")
            st.write("---")


def page_developer():
    app_header()
    st.subheader("👨‍💻 Developer Information")

    st.write(
        f"""
        **Developer:** {DEVELOPER_NAME}  
        **Role:** B.Tech CSE Student | Python & Java Enthusiast  
        """
    )

    st.markdown(
        f"[🔗 Connect on LinkedIn]({DEVELOPER_LINKEDIN})",
        unsafe_allow_html=True,
    )

    st.write("---")
    st.write(
        """
        This web version of **Vote-Xpress** is built using:
        - 🐍 Python  
        - 🌐 Streamlit (for web UI)  

        You can add this project to your:
        - ✅ CV / Resume  
        - ✅ GitHub Portfolio  
        - ✅ LinkedIn Projects section
        """
    )


# ----------------------------
# MAIN APP ROUTER
# ----------------------------
PAGES = {
    "🏠 Home": page_home,
    "📝 Register": page_register,
    "🗳️ Vote": page_vote,
    "📊 Live Results": page_results,
    "🧠 Quiz": page_quiz,
    "💬 Feedback": page_feedback,
    "👨‍💻 Developer Info": page_developer,
}

def main():
    with st.sidebar:
        st.image("https://static.streamlit.io/examples/dice.jpg", width=120)
        st.markdown("## Vote-Xpress Navigation")
        choice = st.radio("Go to:", list(PAGES.keys()))
        st.markdown("---")
        st.markdown(f"**Developer:** {DEVELOPER_NAME}")

    # Call the selected page
    PAGES[choice]()


if __name__ == "__main__":
    main()

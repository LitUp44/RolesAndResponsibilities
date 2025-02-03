import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------
# Helper Functions for Header & Subheader
# -----------------------------

def app_header():
    """Display a persistent header with the logo and main title."""
    st.image("Aligned White.png", width=200)  # Adjust width as needed.
    st.markdown(
        """
        <div style="background-color: #f5724b; padding: 10px; text-align: center; border-radius: 8px;">
            <h1 style="color: #ffeae6; margin: 0;">Money Roles!</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def quiz_subheader():
    """Display the sub-header for the landing page only."""
    st.markdown(
        """
        <div style="background-color: #8f4e52; padding: 10px; text-align: center; border-radius: 8px;">
            <p style="color: #ffeae6; margin: 5px 0 0 0; font-size: 32px;">
                Which money roles do you like to take? Take the quiz and find out!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Session State Initialization
# -----------------------------

# Phase values: "landing", "quiz", "results"
if "phase" not in st.session_state:
    st.session_state.phase = "landing"  # Start at the landing page.

# Initialize quiz state variables (only needed for quiz phase and beyond).
if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "scores" not in st.session_state:
    # Example categories (adjust based on your quiz).
    all_categories = {"Travel", "Experiences", "Convenience", "Luxury", 
                      "Relationships", "SelfImprovement", "Health", 
                      "Generosity", "Freedom"}
    st.session_state.scores = {cat: 0 for cat in all_categories}

# Dummy question list (replace with your full 13 questions)
questions = [
    ("1. When it comes to lunch, what’s your preference?", [
        ("Convenience", "Grab something quick and easy to save time"),
        ("Experiences", "Try out a new restaurant or café every time"),
        ("Health", "Meal-prep at home so I know it’s healthy"),
        ("Relationships", "Meet a friend or family member for lunch")
    ]),
    ("2. It’s Saturday night! How do you like to spend it?", [
        ("Generosity", "I love to host my friends or family."),
        ("Experiences", "Plan a special experience like a concert."),
        ("SelfImprovement", "Work on a personal project."),
        ("Freedom", "I like not having a set plan.")
    ])
    # ... add additional questions as needed ...
]

# -----------------------------
# Page Functions
# -----------------------------

def show_landing_page():
    """Display the landing page with header, subheader, and a 'Start Now' button."""
    app_header()      # Always show the header.
    quiz_subheader()  # Show the subheader.
    
    # Add extra padding between subheader and button.
    st.markdown("<div style='padding-bottom: 20px;'></div>", unsafe_allow_html=True)
    
    if st.button("Start Now"):
        st.session_state.phase = "quiz"
        st.rerun()

def show_quiz():
    """Display the quiz questions.
    
    In this phase, only the persistent header is shown (the subheader is hidden).
    """
    app_header()  # Only display the persistent header.
    
    # Check if there are still questions to show.
    if st.session_state.current_question < len(questions):
        question_text, answers = questions[st.session_state.current_question]
        st.markdown(f"### {question_text}")
        
        # Prepare answer options.
        options = [answer_text for _, answer_text in answers]
        choice = st.radio("Select your answer:", options, key=f"question_{st.session_state.current_question}")
        
        if st.button("Next"):
            # Update the score for the selected answer.
            for cat, answer_text in answers:
                if answer_text == choice:
                    st.session_state.scores[cat] += 1
                    break
            st.session_state.current_question += 1
            st.rerun()
    else:
        # If no more questions, move to results.
        st.session_state.phase = "results"
        st.rerun()

def show_quiz_results():
    """Display the quiz results.
    
    For demonstration, this page displays the scores as a horizontal bar chart.
    """
    app_header()  # Only the persistent header.
    st.title("Quiz Results")
    
    # Retrieve scores.
    scores = st.session_state.get("scores", {})
    if not scores:
        st.write("No scores found. You may not have completed the quiz.")
        return

    # Create a DataFrame from the scores dictionary.
    data = pd.DataFrame(list(scores.items()), columns=["Money Dial", "Score"])
    
    # Create a horizontal bar chart.
    chart = alt.Chart(data).mark_bar(color="#682d24").encode(
        x=alt.X("Score:Q", title="Points", axis=alt.Axis(grid=False, format="d", tickMinStep=1)),
        y=alt.Y("Money Dial:N", title="Money Dial", sort="-x", axis=alt.Axis(grid=False))
    ).properties(
        width=600,
        height=400,
        title="Money Dial Scores"
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Optionally, a button to restart.
    if st.button("Restart Quiz"):
        # Reset quiz-related session state variables.
        for key in ["phase", "current_question", "scores"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.phase = "landing"
        st.rerun()

# -----------------------------
# Main App Logic
# -----------------------------

if st.session_state.phase == "landing":
    show_landing_page()
elif st.session_state.phase == "quiz":
    show_quiz()
elif st.session_state.phase == "results":
    show_quiz_results()



import streamlit as st
import random
import plotly.express as px

# -----------------------------
# Header & Sub-header Functions
# -----------------------------
def app_header():
    """Display a persistent header with the logo and main title."""
    st.image("Aligned White.png", width=200)  # Adjust the path and width as needed.
    st.markdown(
        """
        <div style="background-color: #f5724b; padding: 10px; text-align: center; border-radius: 8px;">
            <h1 style="color: #ffeae6; margin: 0;">Money Roles!</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

def quiz_subheader():
    """Display the sub-header for the quiz only on the landing page."""
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
# Custom CSS to display radio options horizontally
# -----------------------------
st.markdown(
    """
    <style>
    /* This CSS targets the container for radio buttons and displays the labels inline */
    div[role="radiogroup"] > label {
        display: inline-flex;
        margin-right: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Define the quiz questions
# -----------------------------
day_to_day_questions = [
    {"question": "Who pays most of the bills? (Even if you split the cost, who actually pays them?)", "category": "Day-to-day"},
    {"question": "Who monitors your monthly budget if you have one?", "category": "Day-to-day"},
    {"question": "Who predominantly determines how much you can afford for your rent or mortgage payment?", "category": "Day-to-day"},
    {"question": "Who predominantly sets the bar for how much is acceptable to spend on groceries?", "category": "Day-to-day"},
    {"question": "Who would normally decide how much you could spend on a vacation?", "category": "Day-to-day"},
]

long_term_questions = [
    {"question": "Who decides what your long-term financial strategy will be?", "category": "Long-term"},
    {"question": "In your couple, who decides which investments you’re going to make and how much you’re going to invest every month or every year?", "category": "Long-term"},
    {"question": "Most often, who thinks about how much you need to be setting aside for retirement / how much you should have when you retire?", "category": "Long-term"},
    {"question": "If you have debt, who keeps an eye on your debt payback date?", "category": "Long-term"},
    {"question": "If you have debt, who decides what your debt payments will be?", "category": "Long-term"},
]

# -----------------------------
# Updated options list with emojis
# -----------------------------
options = ["Me! 🕺", "My partner 😁", "Neither of us really 🙇", "Both of us 👯"]

# -----------------------------
# Session State Initialization
# -----------------------------
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "responses" not in st.session_state:
    st.session_state.responses = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Store the shuffled questions only once
if "questions" not in st.session_state:
    all_questions = day_to_day_questions + long_term_questions
    # Randomly shuffle and store the list of questions.
    st.session_state.questions = random.sample(all_questions, len(all_questions))

# -----------------------------
# Main App Logic
# -----------------------------

# Always display the header (logo and title)
app_header()

# Landing Page: Before quiz starts and before submission.
if not st.session_state.quiz_started and not st.session_state.submitted:
    quiz_subheader()
    st.write("Welcome! Ready to find out which money roles suit you best?")
    if st.button("Start Now"):
        st.session_state.quiz_started = True
        st.rerun()

# Quiz Question Pages: Display one question per page.
if st.session_state.quiz_started and not st.session_state.submitted:
    questions = st.session_state.questions  # use our pre-shuffled list
    current = st.session_state.current_question
    total = len(questions)
    question_data = questions[current]

    st.markdown(f"### Question {current + 1} of {total}")
    st.markdown(f"**{question_data['question']}**")

    # Provide radio options for the question.
    answer = st.radio(
        label="",
        options=options,
        key=f"q_{current}",
        horizontal=True
    )

    # Navigation buttons.
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if current > 0:
            if st.button("Previous"):
                st.session_state.current_question -= 1
                st.rerun()
    with col3:
        # On the final question, change button text to "Submit".
        if current == total - 1:
            if st.button("Submit"):
                # Save the answer for the current question.
                st.session_state.responses[f"q_{current}"] = answer
                st.session_state.submitted = True
                st.rerun()
        else:
            if st.button("Next"):
                # Save the answer and move to the next question.
                st.session_state.responses[f"q_{current}"] = answer
                st.session_state.current_question += 1
                st.rerun()

# Results Page: After quiz submission.
if st.session_state.submitted:
    st.title("Quiz Results")
    
    questions = st.session_state.questions  # our pre-shuffled list
    # Process responses by category for insights.
    results = {"Day-to-day": [], "Long-term": []}
    for idx, item in enumerate(questions):
        key = f"q_{idx}"
        category = item["category"]
        # We assume every question was answered.
        answer = st.session_state.responses.get(key, None)
        if answer is not None:
            results[category].append(answer)
    
    def compute_percentages(answers):
        counts = {option: 0 for option in options}
        total_answers = len(answers)
        for ans in answers:
            counts[ans] += 1
        percentages = {opt: (counts[opt] / total_answers * 100) for opt in counts}
        return percentages

    # Display results for each category with pie charts and insights.
    for category in results:
        st.header(f"{category} Expenses")
        percentages = compute_percentages(results[category])
        
        fig = px.pie(
            names=list(percentages.keys()),
            values=list(percentages.values()),
            title=f"",
            color=list(percentages.keys()),
            color_discrete_map={
                "Me! 🕺": "#233c64",
                "My partner 😁": "#8f4e52",
                "Neither of us really 🙇": "#f5724b",
                "Both of us 👯": "#ffeae6"
            }
          )
        fig.update_layout(
            legend=dict(
                font=dict(
                    size=18  # change this value to your desired font size
                    )
                )    
            )
        
        st.plotly_chart(fig)
        
        st.subheader("Insights:")
        both_pct = percentages["Both of us 👯"]
        me_pct = percentages["Me! 🕺"]
        partner_pct = percentages["My partner 😁"]
        neither_pct = percentages["Neither of us really 🙇"]
        
        if both_pct > 60:
            st.info(f"Awesome! It looks like you and your partner are working together to manage your {category.lower()} expenses!")
        else:
            if me_pct >= 40:
                st.info(f"It looks like you do a lot of the work with {category.lower()} expenses! It's great that you're taking the time to look after this and it's not going by the wayside. This is the perfect place to start the conversations with your partner and help bring them into the finances so you feel that you have a partner and don't become resentful!")
            elif partner_pct >= 40:
                st.info(f"It looks like your partner does a lot of the work with {category.lower()} expenses! It's great that they're taking the time to look after this and it's not going by the wayside. If you're up for it, it might be a great time to tell your partner you would like to take a more active role. Your best chance for success is both of you being an active part of the conversation, making decisions as a team!")
            elif neither_pct >= 40:
                st.info(f"Hmm, it looks like you've got a bit of a gap in your {category.lower()} expenses. This should be the first thing to address as you want to make sure that you're making active decisions with your money - because not making a decision is a decision in itself, and it just doesn't tend to lead to the outcomes we want.")
            else:
                st.info("The results indicate a balanced mix of responsibilities. Consider discussing ways to further optimize your expense management together!")

    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


import streamlit as st
import random
import plotly.express as px

st.markdown(
    """
    <style>
    /* This CSS rule overrides the background color of info messages.
       Note: The class name used by Streamlit might change in future versions.
       Inspect your app in the browser to confirm the class name if needed. */
    .stAlert {  
        background-color: #ffeae6 !important;  
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header & Sub-header Functions
# -----------------------------
def app_header():
    """Display a persistent header with the logo and main title."""
    st.image("Aligned White.png", width=200)  # Adjust the path and width as needed.
    st.markdown(
        """
        <div style="background-color: #f5724b; padding: 10px; text-align: center; border-radius: 8px;">
            <h1 style="color: #ffeae6; margin: 0;">Understanding Money Roles!</h1>
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
    {"question": "Who decided how much you can afford for your rent or mortgage payment?", "category": "Day-to-day"},
    {"question": "Who usually decides how much is acceptable to spend on groceries?", "category": "Day-to-day"},
    {"question": "Who would normally decide how much you can afford to spend on a vacation?", "category": "Day-to-day"},
]

long_term_questions = [
    {"question": "Who thinks about what your long-term financial strategy will be?", "category": "Long-term"},
    {"question": "Who decides which investments you’re going to make? Ie. properties, stocks, mostly cash in savings etc.", "category": "Long-term"},
    {"question": "Who thinks about how much you need to be setting aside for retirement / how much you should have when you retire?", "category": "Long-term"},
    {"question": "Who decides how much you're going to save / invest per month?", "category": "Long-term"},
    {"question": "Who keeps an eye on your debt payback and decides how much your debt payments will be? (If you have debt, otherwise not applicable)", "category": "Long-term"},
]

# -----------------------------
# Updated options list with emojis
# -----------------------------
options = ["Me! 🕺", "My partner 😁", "Neither of us really 🙇", "Both of us 👯", "Not really applicable"]

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
    st.write("Welcome! Let's find out how you and your partner divy up thinking about finances!")
    if st.button("Start Now"):
        st.session_state.quiz_started = True
        st.rerun()

# Quiz Question Pages: Display one question per page.
if st.session_state.quiz_started and not st.session_state.submitted:
    questions = st.session_state.questions  # our pre-shuffled list
    current = st.session_state.current_question
    total = len(questions)
    question_data = questions[current]

    st.markdown(f"### Question {current + 1} of {total}")
    st.markdown("<p style='font-size: 16px; color: #555;'>In your couple:</p>", unsafe_allow_html=True)
    st.markdown(f"**{question_data['question']}**")

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
    
    # Move the image right after the header
    st.image("FinancesInfographic.png", width=700)
    
    # Add some explanatory text before the results sections
    st.markdown(
        """
        <div style="padding: 10px; background-color: #f0f0f0; border-radius: 8px;">
            <p style="font-size: 18px; color: #333;">
                <p style="font-size: 18px; color: #333;">
                Thank you for completing the quiz! This aims to help you see how you and your partner divide financial roles.<br><br>
                It's a bit of a trick question because ultimately you want to make your decisions together even if you execute different things.<br><br>
                <strong>Day-to-day finances  </strong> are the financial decisions that happen daily or monthly. Paying bills on time, deciding what kind of vacation you can afford.<br><br>
                <strong>Long-term financial decisions </strong> are the decisions that govern your long-term thinking; how you want to save and invest your money, what kind of retirement you hope to have.<br><br>
                The goal is to have most of these roles be a strong <strong>'BOTH'</strong> as you progress on your financial journey! Check out your results below.
            </p>
                 </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
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
        st.markdown(
            f"<h3 style='font-size:40px;'>{category} Expenses</h3>",
            unsafe_allow_html=True
        )
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
        
        st.markdown(
            f"<h3 style='font-size:20px;'>Insights:</h3>",
            unsafe_allow_html=True
        )
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
                st.info(f"It looks like your partner does a lot of the work with {category.lower()} expenses! It's great that they're taking the time to look after this and it's not going by the wayside. If you're up for it, it might be the perfect time to tell your partner you would like to take a more active role. Your best chance for success is both of you being an active part of the conversation, making decisions as a team!")
            elif neither_pct >= 40:
                st.info(f"Hmm, it looks like you've got a bit of missing gap in your {category.lower()} expenses. This should be the first thing to address on your financial journey as you want to make sure that you and your partner are making active decisions with your money!")
            else:
                st.info("Your roles are quite the mix! This is a great moment to have a conversation with your partner and take on some of the roles together!")


    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


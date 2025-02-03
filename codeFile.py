import streamlit as st
import random
import plotly.express as px

# --- Custom CSS to display radio options horizontally ---
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

# --- Define the quiz questions ---
# Each question is a dict with a text and category tag.
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

# Combine and shuffle the questions
all_questions = day_to_day_questions + long_term_questions
random.shuffle(all_questions)

# Options for each question
options = ["me", "my partner", "neither of us really", "both of us"]

# --- Quiz Form ---
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    st.title("Financial Responsibilities Quiz")
    st.write("For each question, please select who is responsible:")

    with st.form(key="quiz_form"):
        responses = {}
        for idx, item in enumerate(all_questions):
            q_key = f"q_{idx}"
            # Display question text with its category as a subheader
            st.markdown(f"**({item['category']}) {item['question']}**")
            # The radio button is rendered with our custom CSS making the options display inline.
            responses[q_key] = st.radio(
                label="",
                options=options,
                key=q_key,
                horizontal=True  # Although Streamlit doesn’t officially support horizontal layout, our CSS hack helps.
            )
            st.markdown("---")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.submitted = True
            st.session_state.responses = responses
            st.session_state.questions = all_questions
            st.experimental_rerun()

# --- Results Page ---
if st.session_state.submitted:
    st.title("Quiz Results")
    
    # Separate responses by category
    results = {"Day-to-day": [], "Long-term": []}
    for idx, item in enumerate(st.session_state.questions):
        key = f"q_{idx}"
        category = item["category"]
        answer = st.session_state.responses[key]
        results[category].append(answer)
    
    # Function to compute percentages
    def compute_percentages(answers):
        counts = {option: 0 for option in options}
        total = len(answers)
        for ans in answers:
            counts[ans] += 1
        percentages = {opt: (counts[opt] / total * 100) for opt in counts}
        return percentages

    # Display results for each category
    for category in results:
        st.header(f"{category} Expenses")
        percentages = compute_percentages(results[category])
        
        # Create a pie chart using Plotly
        fig = px.pie(
            names=list(percentages.keys()),
            values=list(percentages.values()),
            title=f"{category} Responsibilities Distribution",
            color=list(percentages.keys()),
            color_discrete_map={
                "me": "lightblue",
                "my partner": "lightgreen",
                "neither of us really": "lightgray",
                "both of us": "orange"
            }
        )
        st.plotly_chart(fig)
        
        # --- Insights ---
        st.subheader("Insights:")
        both_pct = percentages["both of us"]
        me_pct = percentages["me"]
        partner_pct = percentages["my partner"]
        neither_pct = percentages["neither of us really"]
        
        if both_pct > 60:
            st.info(f"Awesome! It looks like you and your partner are working together to manage your {category.lower()} expenses!")
        else:
            if me_pct > 40:
                st.info(f"It looks like you do a lot of the work with {category.lower()} expenses! It's great that you're taking the time to look after this and it's not going by the wayside. This is the perfect place to start the conversations with your partner and help bring them into the finances so you feel that you have a partner and don't become resentful!")
            elif partner_pct > 40:
                st.info(f"It looks like your partner does a lot of the work with {category.lower()} expenses! It's great that they're taking the time to look after this and it's not going by the wayside. If you're up for it, it might be a great time to tell your partner you would like to take a more active role. Your best chance for success is both of you being an active part of the conversation, making decisions as a team!")
            elif neither_pct > 40:
                st.info(f"Hmm, it looks like you've got a bit of a gap in your {category.lower()} expenses. This should be the first thing to address as you want to make sure that you're making active decisions with your money - because not making a decision is a decision in itself, and it just doesn't tend to lead to the outcomes we want.")
            else:
                st.info("The results indicate a balanced mix of responsibilities. Consider discussing ways to further optimize your expense management together!")

    # Option to restart the quiz
    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

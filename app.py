import streamlit as st

# ============================================================
# HOTEL ENQUIRY CHATBOT — INTERACTIVE STREAMLIT APP
# Backend: Hotel_Enquiry_Chatbot.py
# ============================================================

st.set_page_config(
    page_title="Hotel Enquiry Assistant",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# SAFE BACKEND IMPORT
# ------------------------------------------------------------
try:
    import Hotel_Enquiry_Chatbot as bot
    BACKEND_OK = hasattr(bot, "chatbot_response")
except Exception as e:
    bot = None
    BACKEND_OK = False
    BACKEND_ERROR = str(e)

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "enquiry_count" not in st.session_state:
    st.session_state.enquiry_count = 0

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None

# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #f7f9fc 0%,
        #eef4ff 100%
    );
}

.hero {
    padding: 28px 32px;
    border-radius: 22px;
    background:
        linear-gradient(
            120deg,
            rgba(18,43,76,.97),
            rgba(43,91,151,.94)
        ),
        url("https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1400&q=75");

    background-size: cover;
    background-position: center;

    color: white;
    margin-bottom: 20px;

    box-shadow:
        0 10px 30px rgba(31,55,90,.18);
}

.hero h1 {
    font-size: 38px;
    margin-bottom: 6px;
}

.hero p {
    font-size: 17px;
    opacity: .92;
    margin-bottom: 0;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #e4e9f2;

    box-shadow:
        0 5px 18px rgba(30,50,80,.08);

    height: 100%;
}

.card h3 {
    margin-top: 5px;
    color: #183153;
}

.topic {
    text-align: center;
    padding: 14px 8px;
    border-radius: 15px;
    background: white;
    border: 1px solid #e5eaf2;

    box-shadow:
        0 4px 12px rgba(30,50,80,.06);
}

.topic-icon {
    font-size: 27px;
}

.topic-text {
    font-weight: 600;
    color: #27364d;
    margin-top: 5px;
}

.status {
    padding: 10px 14px;
    border-radius: 12px;
    background: #edf8f0;
    color: #196b35;
    font-weight: 600;
    margin-bottom: 14px;
}

.info-box {
    padding: 16px;
    border-radius: 15px;
    background: #f2f6ff;

    border-left:
        5px solid #3b70c4;

    margin: 12px 0;
}

.footer {
    text-align: center;
    color: #718096;
    padding: 25px 0 10px 0;
    font-size: 13px;
}

div[data-testid="stMetric"] {
    background: white;
    padding: 12px;
    border-radius: 14px;
    border: 1px solid #e4e9f2;
}

.stButton > button {
    border-radius: 12px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def ask_bot(question):
    """
    Send the question to the student's existing
    Hotel_Enquiry_Chatbot.py backend.
    """

    if not BACKEND_OK:

        return (
            "⚠️ The hotel chatbot backend is not connected. "
            "Please keep `Hotel_Enquiry_Chatbot.py` in the same "
            "folder as `app.py` and make sure it contains "
            "`chatbot_response(user_input)`."
        )

    try:

        answer = bot.chatbot_response(question)

        if answer is None:
            return (
                "I could not generate a response "
                "for that enquiry."
            )

        return str(answer)

    except Exception as e:

        return (
            "⚠️ I encountered an issue while processing "
            f"your enquiry: {e}"
        )


def process_question(question):
    """
    Add user question and chatbot response
    to the conversation history.
    """

    question = question.strip()

    if not question:
        return

    response = ask_bot(question)

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.session_state.enquiry_count += 1


def clear_chat():

    st.session_state.messages = []

    st.session_state.enquiry_count = 0

    st.session_state.selected_topic = None


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero">

    <h1>
        🏨 Hotel Enquiry Assistant
    </h1>

    <p>
        Your smart virtual assistant for hotel information,
        rooms, pricing, facilities, location, check-in
        and cancellation enquiries.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# BACKEND STATUS
# ============================================================

if BACKEND_OK:

    st.markdown(
        """
        <div class="status">
            🟢 Hotel Assistant is ready —
            ask your enquiry below.
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.warning(
        """
        The Streamlit interface is ready, but the chatbot
        backend is not connected.

        Please place `Hotel_Enquiry_Chatbot.py`
        in the same folder as this `app.py`.
        """
    )


# ============================================================
# METRICS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(
        "🏨 Service",
        "Hotel Enquiry"
    )

with m2:

    st.metric(
        "💬 Enquiries",
        st.session_state.enquiry_count
    )

with m3:

    st.metric(
        "⚡ Response",
        "Instant"
    )

with m4:

    st.metric(
        "🤖 Assistant",
        "Online" if BACKEND_OK else "Offline"
    )


st.markdown("---")


# ============================================================
# MAIN LAYOUT
# ============================================================

left, right = st.columns(
    [2.15, 1],
    gap="large"
)


# ============================================================
# LEFT COLUMN — CHAT
# ============================================================

with left:

    st.subheader(
        "💬 Chat with the Hotel Assistant"
    )

    # --------------------------------------------------------
    # WELCOME SCREEN
    # --------------------------------------------------------

    if not st.session_state.messages:

        st.markdown(
            """
            <div class="info-box">

                <strong>👋 Welcome!</strong>
                <br><br>

                Start by choosing a quick enquiry below
                or type your own question.

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "### 🔎 Popular Enquiries"
        )

        q1, q2, q3 = st.columns(3)

        # COLUMN 1
        with q1:

            if st.button(
                "🏨 Hotel Information",
                use_container_width=True
            ):

                process_question(
                    "Tell me about the hotel"
                )

                st.rerun()

            if st.button(
                "🛏️ Room Types",
                use_container_width=True
            ):

                process_question(
                    "What room types are available?"
                )

                st.rerun()

        # COLUMN 2
        with q2:

            if st.button(
                "💰 Room Prices",
                use_container_width=True
            ):

                process_question(
                    "What are the room prices?"
                )

                st.rerun()

            if st.button(
                "✨ Facilities",
                use_container_width=True
            ):

                process_question(
                    "What facilities does the hotel provide?"
                )

                st.rerun()

        # COLUMN 3
        with q3:

            if st.button(
                "📍 Location",
                use_container_width=True
            ):

                process_question(
                    "Where is the hotel located?"
                )

                st.rerun()

            if st.button(
                "🕐 Check-in",
                use_container_width=True
            ):

                process_question(
                    "What are the check-in timings?"
                )

                st.rerun()


    # --------------------------------------------------------
    # DISPLAY CHAT HISTORY
    # --------------------------------------------------------

    for message in st.session_state.messages:

        if message["role"] == "user":

            avatar = "🧑"

        else:

            avatar = "🏨"

        with st.chat_message(
            message["role"],
            avatar=avatar
        ):

            st.markdown(
                message["content"]
            )


    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    user_input = st.chat_input(
        "Ask about rooms, prices, facilities, "
        "location, check-in or cancellation..."
    )

    if user_input:

        process_question(
            user_input
        )

        st.rerun()


# ============================================================
# RIGHT COLUMN — HOTEL INFORMATION
# ============================================================

with right:

    st.subheader(
        "🌟 Explore"
    )

    st.markdown(
        """
        <div class="card">

            <h3>
                🏨 Hotel Services
            </h3>

            <p>
                Use the assistant to quickly enquire about:
            </p>

            <ul>

                <li>🛏️ Room types</li>

                <li>💰 Room prices</li>

                <li>✨ Facilities</li>

                <li>📍 Hotel location</li>

                <li>🕐 Check-in information</li>

                <li>❌ Cancellation policies</li>

                <li>ℹ️ General hotel information</li>

            </ul>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # HOTEL IMAGE
    # --------------------------------------------------------

    st.markdown(
        "### 🖼️ Hotel Experience"
    )

    st.image(
        "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=700&q=75",
        use_container_width=True,
        caption="Comfort • Convenience • Hospitality"
    )


    # --------------------------------------------------------
    # QUICK QUESTIONS
    # --------------------------------------------------------

    st.markdown(
        "### ⚡ Quick Questions"
    )

    quick_questions = {

        "🛏️ Ask about rooms":
            "What rooms are available?",

        "💰 Ask about price":
            "What is the price of the rooms?",

        "✨ Ask about facilities":
            "What facilities are available?",

        "📍 Ask about location":
            "Where is the hotel located?",

        "❌ Ask about cancellation":
            "What is the cancellation policy?"

    }


    for label, question in quick_questions.items():

        if st.button(
            label,
            use_container_width=True
        ):

            process_question(
                question
            )

            st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## 🏨 Hotel Assistant"
    )

    st.markdown(
        """
        A simple interactive interface for handling
        common hotel enquiries.
        """
    )

    st.markdown("---")


    # --------------------------------------------------------
    # TOPICS
    # --------------------------------------------------------

    st.markdown(
        "### 💡 You can ask"
    )

    sidebar_topics = [

        "🏨 Hotel information",

        "🛏️ Room types",

        "💰 Room prices",

        "✨ Facilities",

        "📍 Location",

        "🕐 Check-in",

        "❌ Cancellation"

    ]


    for topic in sidebar_topics:

        st.write(topic)


    st.markdown("---")


    # --------------------------------------------------------
    # EXAMPLE QUESTIONS
    # --------------------------------------------------------

    st.markdown(
        "### 🎯 Try asking"
    )

    examples = [

        "What rooms are available?",

        "How much does a room cost?",

        "What facilities are provided?",

        "Where is the hotel?",

        "What time is check-in?",

        "Can I cancel my booking?"

    ]


    selected_example = st.selectbox(
        "Choose a question",
        examples,
        label_visibility="collapsed"
    )


    if st.button(
        "Ask Selected Question",
        use_container_width=True
    ):

        process_question(
            selected_example
        )

        st.rerun()


    st.markdown("---")


    # --------------------------------------------------------
    # CLEAR CHAT
    # --------------------------------------------------------

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        clear_chat()

        st.rerun()


    st.markdown("---")


    # --------------------------------------------------------
    # BACKEND STATUS
    # --------------------------------------------------------

    if BACKEND_OK:

        st.success(
            "Backend connected"
        )

    else:

        st.error(
            "Backend not connected"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        🏨 Hotel Enquiry Chatbot
        • Interactive Streamlit Interface

        <br>

        Designed for conversational hotel
        information support

    </div>
    """,
    unsafe_allow_html=True
)

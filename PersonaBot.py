from  langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

model = ChatGroq(model = "llama-3.3-70b-versatile",temperature = 0.7,max_tokens = 2048)

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="AI Assistant Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 PersonaBot")
st.caption("Switch between Professional, Friendly, Humorous, and Expert modes")


# ---------------- MODE SELECTION ----------------
mode_choice = st.radio(
    "Choose Response Style:",
    ["💼 Professional", "😊 Friendly", "😂 Humorous", "🎓 Expert"],
    horizontal=True
)

# Map mode
if mode_choice == "💼 Professional":
    mode = (
        "You are a professional AI assistant. "
        "Provide clear, concise, and well-structured responses."
    )

elif mode_choice == "😊 Friendly":
    mode = (
        "You are a friendly AI assistant. "
        "Be warm, approachable, and helpful while answering questions."
    )

elif mode_choice == "😂 Humorous":
    mode = (
        "You are a humorous AI assistant. "
        "Add light jokes and witty remarks while still providing useful answers."
    )

else:  # Expert
    mode = (
        "You are an expert AI assistant. "
        "Provide detailed, accurate, and insightful explanations with examples when appropriate."
    )

# ---------------- SESSION MEMORY ----------------
if "messages" not in st.session_state or st.session_state.get("current_mode") != mode:
    st.session_state.current_mode = mode
    st.session_state.messages = [SystemMessage(content=mode)]


# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)


# ---------------- USER INPUT ----------------
user_input = st.chat_input("Say something...")

if user_input:

    if user_input == "Exit":
        st.warning("Conversation ended. Refresh page to start again.")
        st.stop()

    # Add user message
    st.session_state.messages.append(HumanMessage(content=user_input))
    with st.chat_message("user"):
        st.write(user_input)

    # Get AI response
    response = model.invoke(st.session_state.messages)

    # Add AI message
    st.session_state.messages.append(AIMessage(content=response.content))

    with st.chat_message("assistant"):
        st.write(response.content)


# ---------------- CLEAR BUTTON ----------------
st.divider()
if st.button("🔄 Reset Chat"):
    st.session_state.messages = [SystemMessage(content=mode)]
    st.rerun()

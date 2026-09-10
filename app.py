import streamlit as st


st.set_page_config(
    page_title="AI Banking Query Assistant",
    page_icon="🏦"
)

st.title("🏦 AI Banking Query Assistant")

st.write(
    "Ask questions about common banking products and services."
)

question = st.chat_input("Ask your banking question...")


if question:

    st.write("✅ Question received:")
    st.write(question)

    with st.spinner("Loading AI Banking Assistant..."):

        try:
            from src.chatbot import ask_banking_assistant

          

            answer = ask_banking_assistant(question)

          

            st.subheader("🤖 AI Assistant")

            st.write(answer)

        except Exception as e:

            st.error("❌ An error occurred")

            st.exception(e)
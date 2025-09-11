import streamlit as st
import ollama

current_model = "qwen2:0.5b"
st.title("The Vault 🔒")
st.write("Your Private, Offline AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # This is the magic - talking to the LOCAL model
        stream = ollama.chat(
            model= current_model, # Start with the small, fast model
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in stream:
            full_response += chunk['message']['content']
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
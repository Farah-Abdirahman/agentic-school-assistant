import streamlit as st

from assistant import create_agent

st.set_page_config(page_title="KCA University Assistant", page_icon="🎓")
st.title("🎓 KCA University Academic Assistant")
st.caption("Ask questions about academic calendars, policies, graduation, and campus services.")


@st.cache_resource
def get_agent():
    return create_agent()


agent = get_agent()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi! I can help with KCA University academic info. "
                "Ask about calendars, fees, registration, or campus services."
            ),
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a question about KCA University…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent(prompt)
            content = str(response)
            st.markdown(content)
    st.session_state.messages.append({"role": "assistant", "content": content})

import streamlit as st
import asyncio
import websockets
import json

async def websocket_communicate(message):
    uri = "ws://127.0.0.1:8001/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        return response

st.title("Risk AI")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

message = st.text_input("Type a message:")
if st.button("Send"):
    if message:
        response = asyncio.run(websocket_communicate(message))
        st.session_state.chat_history.append({"user": message, "ai": response})
        st.write(f"You: {message}")
        st.write(f"AI: {response}")
    else:
        st.write("Please enter a message.")

# st.sidebar.header("Chat History")
# for chat in st.session_state.chat_history:
#     st.sidebar.markdown(f"<span style='color: blue;'>You: {chat['user']}</span>", unsafe_allow_html=True)
#     st.sidebar.markdown(f"<span style='color: green;'>AI: {chat['ai']}</span>", unsafe_allow_html=True)

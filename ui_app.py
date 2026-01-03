import streamlit as st
import os
from reflection import build_graph
from langchain_core.messages import HumanMessage, AIMessage
from PIL import Image

st.set_page_config(page_title="LinkedIn Post Reflector", page_icon="📝", layout="wide")

st.title("📝 LinkedIn Post Reflector")
st.markdown("""
This app uses **LangGraph** to generate and refine LinkedIn posts. 
An **Agent** creates a post, and a **Critic** provides feedback for multiple rounds of improvement.
""")

with st.sidebar:
    st.header("Settings")
    topic = st.text_area("What is your LinkedIn post about?", 
                         placeholder="e.g., Getting a software developer job at IBM",
                         height=150)
    
    recursion_limit = st.slider("Max Refinement Rounds", 2, 10, 3)
    
    start_button = st.button("Generate Post", type="primary", use_container_width=True)

if start_button and topic:
    workflow = build_graph()
    inputs = HumanMessage(content=topic)
    
    st.subheader("🚀 Workflow Progress")
    
    message_container = st.container()
    final_post = ""
    
    with st.spinner("Agent and Critic are collaborating..."):
        events = workflow.stream(inputs)
        
        for event in events:
            for node_name, messages in event.items():
                with message_container:
                    if node_name == "generate":
                        with st.chat_message("assistant", avatar="🤖"):
                            st.write(f"**Agent (Generation)**")
                            st.write(messages[0].content)
                            final_post = messages[0].content
                    elif node_name == "reflect":
                        with st.chat_message("user", avatar="🧐"):
                            st.write(f"**Critic (Reflection)**")
                            st.write(messages[0].content)
                
    st.success("✅ Post refinement complete!")
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("✨ Final LinkedIn Post")
        st.code(final_post, language="text")
        st.button("Copy to Clipboard", on_click=lambda: st.write("Copying functionality would go here!")) # Simplified
        

elif start_button and not topic:
    st.warning("Please enter a topic first!")
else:
    st.info("Enter a topic in the sidebar and click 'Generate Post' to begin.")

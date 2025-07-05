import streamlit as st


# APP Configuration and Local User Interface Setup

st.set_page_config(page_title="Dormitory AI Assistant", layout="centered")
st.title("Dormitory AI Agent")
st.markdown("Ask questions about dorm rooms, AC units, temperature trends, and occupancy predictions.")

# Query functions from both_files, throw an error if you can't
try:
    from slice_json import query_graph_nlp
    model_loaded = True
    st.success("Model interface loaded successfully.")
except Exception as e:
    model_loaded = False
    st.error(f"Failed to load model interface: {e}")

# Have the client ask a question. 
user_input = st.text_input("Ask a question about the dormitory system:")

# If the question is valid, it can create and send the JSON files to the API.
# Otherwise, the program ran into a problem either creating those scripts or accessing the llm. 
if user_input and model_loaded:
    with st.spinner("Analyzing your question..."):
        try:
            result = query_graph_nlp(user_input)
            st.success("Response:")
            # Show the result to the user
            st.markdown(f"```\n{result}\n```")
        except Exception as err:
            st.error(f"⚠️ An error occurred while processing your question:\n{err}")

#Sample questions to help guide the user
with st.expander("Example questions"):
    st.markdown("""
    - What rooms are serviced by AC Unit 1?
    - When is Dorm_102 usually hottest?
    - Which rooms are hot in the afternoon?
    - Can I forecast when Dorm_105 is occupied?
    - What sensors are in Dorm_103?
    - What is the average temperature by hour for Dorm_106?
    """)

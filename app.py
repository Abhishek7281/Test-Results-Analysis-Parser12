import streamlit as st
import pandas as pd
import os
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt

# --- Streamlit UI setup ---
st.set_page_config(layout="centered")
st.title("🧠 Test Results Agent (Powered by OpenRouter)")
st.markdown("Upload a test results Excel file and ask questions in plain English.")

# --- Upload file ---
uploaded_file = st.file_uploader("📁 Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="Test Results")
        st.success("✅ File loaded successfully.")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ Error reading Excel file: {e}")
    else:
        # --- Prompt box ---
        prompt = st.text_area("💬 Ask a question about the data:",
                              placeholder="Example: Show failed test cases by RequirementName")

        if prompt:
            with st.spinner("🤖 Thinking..."):
                try:
                    # --- OpenRouter LLM via PandasAI ---
                    llm = OpenAI(
                        api_token="your-openrouter-key",  # 🔑 Replace this with your OpenRouter API key
                        api_base="https://openrouter.ai/api/v1",
                        model="mistralai/mistral-7b-instruct"  # ✅ Fast, free model
                    )

                    sdf = SmartDataframe(df, config={"llm": llm, "enable_cache": False})

                    # --- Get response ---
                    result = sdf.chat(prompt)

                    # --- Show response ---
                    if isinstance(result, pd.DataFrame):
                        st.dataframe(result)
                    elif isinstance(result, plt.Figure):
                        st.pyplot(result)
                    else:
                        st.markdown(f"**💡 Answer:** {result}")
                except Exception as e:
                    st.error(f"⚠️ Agent failed: {e}")
else:
    st.info("Please upload an Excel file with a 'Test Results' sheet.")

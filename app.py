# import streamlit as st
# import pandas as pd
# import os
# from pandasai import SmartDataframe
# from pandasai.llm.openai import OpenAI
# import matplotlib.pyplot as plt

# # --- Streamlit UI setup ---
# st.set_page_config(layout="centered")
# st.title("🧠 Test Results Agent (Powered by OpenRouter)")
# st.markdown("Upload a test results Excel file and ask questions in plain English.")

# # --- Upload file ---
# uploaded_file = st.file_uploader("📁 Upload Excel File", type=["xlsx"])

# if uploaded_file:
#     try:
#         df = pd.read_excel(uploaded_file, sheet_name="Test Results")
#         st.success("✅ File loaded successfully.")
#         st.dataframe(df.head())
#     except Exception as e:
#         st.error(f"❌ Error reading Excel file: {e}")
#     else:
#         # --- Prompt box ---
#         prompt = st.text_area("💬 Ask a question about the data:",
#                               placeholder="Example: Show failed test cases by RequirementName")

#         if prompt:
#             with st.spinner("🤖 Thinking..."):
#                 try:
#                     # --- OpenRouter LLM via PandasAI ---
#                     llm = OpenAI(
#                         api_token="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",  
#                         api_base="https://openrouter.ai/api/v1",
#                         model="mistralai/mistral-7b-instruct"  # ✅ Fast, free model
#                     )

#                     sdf = SmartDataframe(df, config={"llm": llm, "enable_cache": False})

#                     # --- Get response ---
#                     result = sdf.chat(prompt)

#                     # --- Show response ---
#                     if isinstance(result, pd.DataFrame):
#                         st.dataframe(result)
#                     elif isinstance(result, plt.Figure):
#                         st.pyplot(result)
#                     else:
#                         st.markdown(f"**💡 Answer:** {result}")
#                 except Exception as e:
#                     st.error(f"⚠️ Agent failed: {e}")
# else:
#     st.info("Please upload an Excel file with a 'Test Results' sheet.")


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pandasai import SmartDataframe
from pandasai.llm.huggingface import HuggingFace
import traceback

# --- Streamlit UI setup ---
st.set_page_config(layout="centered")
st.title("🤗 Test Results Agent (Powered by Hugging Face)")
st.markdown("Upload a test results Excel file and ask questions in plain English.")

# --- Get Hugging Face token from secrets ---
hf_token = st.secrets.get("huggingface_api_token", None)
if not hf_token:
    st.error("❌ Missing Hugging Face API key. Please set it in Streamlit Cloud secrets.")
    st.stop()

# --- Upload Excel file ---
uploaded_file = st.file_uploader("📁 Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)
        if "Test Results" not in xls.sheet_names:
            st.error("❌ Sheet 'Test Results' not found in Excel file.")
            st.stop()

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
                    llm = HuggingFace(
                        api_token=hf_token,
                        model="mistralai/Mistral-7B-Instruct-v0.1"  # You can change to another HF-supported model
                    )

                    sdf = SmartDataframe(df, config={"llm": llm, "enable_cache": False})
                    result = sdf.chat(prompt)

                    # --- Show response ---
                    if isinstance(result, pd.DataFrame):
                        st.dataframe(result)
                    elif isinstance(result, plt.Figure):
                        st.pyplot(result)
                    else:
                        st.markdown(f"**💡 Answer:** {result}")
                except Exception as e:
                    st.error("⚠️ Agent failed. See traceback:")
                    st.code(traceback.format_exc())
else:
    st.info("📤 Please upload an Excel file with a 'Test Results' sheet.")

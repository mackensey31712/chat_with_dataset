# import streamlit as st
# import pandas as pd
# from openai import OpenAI
# import io
# import PyPDF2

# def parse_file(uploaded_file):
#     file_type = uploaded_file.type
#     if file_type == "text/csv":
#         return pd.read_csv(uploaded_file)
#     elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
#         return pd.read_excel(uploaded_file)
#     elif file_type == "application/pdf":
#         return extract_text_from_pdf(uploaded_file)
#     elif file_type.startswith("text/"):
#         return uploaded_file.getvalue().decode("utf-8")
#     elif file_type.startswith("image/"):
#         return f"Image uploaded: {uploaded_file.name}"
#     else:
#         return f"File uploaded: {uploaded_file.name}, Size: {uploaded_file.size} bytes"

# def extract_text_from_pdf(file):
#     pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
#     text = ""
#     for page in pdf_reader.pages:
#         text += page.extract_text() + "\n"
#     return text

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

#     uploaded_file = st.file_uploader("Upload any file")
#     if uploaded_file is not None:
#         file_content = parse_file(uploaded_file)
#         if isinstance(file_content, pd.DataFrame):
#             st.session_state["uploaded_data"] = file_content
#             st.success("File uploaded successfully!")
#             st.write(file_content.head())
#         else:
#             st.session_state["uploaded_data"] = file_content
#             st.success("File uploaded successfully!")
#             st.write(file_content[:1000] + "..." if len(file_content) > 1000 else file_content)

# st.title("💬 Chatdata - Talk To Your Data")
# st.caption("🚀 A chatbot powered by OpenAI")

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     if "uploaded_data" in st.session_state:
#         if isinstance(st.session_state["uploaded_data"], pd.DataFrame):
#             data_info = st.session_state["uploaded_data"].to_string()
#         else:
#             data_info = str(st.session_state["uploaded_data"])
#         hidden_prompt = f"The user has uploaded a file with the following data:\n{data_info[:1000]}...\n\nQuestion: {prompt}"
#     else:
#         hidden_prompt = prompt
    
#     client = OpenAI(api_key=openai_api_key)
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": hidden_prompt}])
#     msg = response.choices[0].message.content
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)

import streamlit as st
import pandas as pd
from openai import OpenAI
import io
import PyPDF2

def parse_file(uploaded_file):
    file_type = uploaded_file.type
    if file_type == "text/csv":
        return pd.read_csv(uploaded_file, delimiter=",", engine="python")
    elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        # Handle multiple sheets in the Excel file
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        sheet_names = list(excel_data.keys())
        st.write(f"Available sheets: {sheet_names}")
        selected_sheet = st.selectbox("Select a sheet to load", options=sheet_names)
        return pd.read_excel(uploaded_file, sheet_name=selected_sheet)
    elif file_type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type.startswith("text/"):
        return uploaded_file.getvalue().decode("utf-8")
    elif file_type.startswith("image/"):
        return f"Image uploaded: {uploaded_file.name}"
    else:
        return f"File uploaded: {uploaded_file.name}, Size: {uploaded_file.size} bytes"

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    uploaded_file = st.file_uploader("Upload any file")
    if uploaded_file is not None:
        file_content = parse_file(uploaded_file)
        if isinstance(file_content, pd.DataFrame):
            st.session_state["uploaded_data"] = file_content
            st.success("File uploaded successfully!")
            
            # Display column names and first few rows
            st.write(f"Columns: {file_content.columns.tolist()}")
            st.write(file_content.head())
        else:
            st.session_state["uploaded_data"] = file_content
            st.success("File uploaded successfully!")
            st.write(file_content[:1000] + "..." if len(file_content) > 1000 else file_content)

st.title("💬 Chatdata - Talk To Your Data")
st.caption("🚀 A chatbot powered by OpenAI")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    # Prepare hidden prompt with dataset details
    if "uploaded_data" in st.session_state:
        if isinstance(st.session_state["uploaded_data"], pd.DataFrame):
            column_names = st.session_state["uploaded_data"].columns.tolist()
            data_info = f"Columns: {column_names}\nSample data:\n{st.session_state['uploaded_data'].head().to_string()}"
        else:
            data_info = str(st.session_state["uploaded_data"])
        hidden_prompt = f"The user has uploaded a file with the following data:\n{data_info[:1000]}...\n\nQuestion: {prompt}"
    else:
        hidden_prompt = prompt
    
    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "system", "content": hidden_prompt}]
    )
    
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

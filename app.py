# basic streamlit app
import streamlit as st
import google.generativeai as genai

gemini_api_key = "AIzaSyCge-pqfJMS9RUr_9wJT99kyeJlvGr-L3k"
genai.configure(api_key = gemini_api_key)

# Title
st.title("Usecase of GenAI : Saving developer's time in Documentation")

# Header
st.subheader('This usecase demonstrates how GenAI can be used to automatically generate documentation for the code.')

# Define the dropdown options
options = ['Python', 'C++', 'Java', 'JavaScript', 'Go', 'Rust']

# Create the dropdown
selected_option = st.selectbox('Programming Language:', options)

# User input
code = st.text_area(label='Enter your code here:')

# Display the entered code
st.write('Entered code:')
if selected_option == 'Python':
    st.code(code, language='python')
elif selected_option == 'C++':
    st.code(code, language='cpp')
elif selected_option == 'Java':
    st.code(code, language='java')
elif selected_option == 'JavaScript':
    st.code(code, language='javascript')
elif selected_option == 'Go':
    st.code(code, language='go')
elif selected_option == 'Rust':
    st.code(code, language='rust')

# Generate documentation
def generate_docs(program, lang, existing_docs="None"):
    try:
        prompt = f"""
        You are an excellent developer who knows {lang} in depth.
        Your task is to document the given code efficiently but not too
        lengthy : {program}.
        For the above program I have some documentation already written in {existing_docs}. 
        If its none then you have to generate a new one and should give that documentation
        in response else update the existing documentation 
        and only give the updated documentation in response.
        """

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    

def isWithBug(program, lang):
    try:
        prompt = f"""
        You are an excellent developer who knows {lang} in depth.
        Your task is to identify the errors in the given code if any : {program}.
        If there are no errors then you have to respond as "False" else you have to
        respond as "True".
        """

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        if response.text == 'False':
            return "No errors found in the code."
        else:
            return "Errors found in the code."
    except Exception as e:
        return f"Error: {str(e)}"
    


# Load existing documentation from README
existing_docs = ''
try:
    with open('README.md', 'r') as f:
        existing_docs = f.read()
except FileNotFoundError:
    existing_docs = 'None'

# Save documentation into a README file
def save_to_readme(docs):
    with open('README.md', 'w') as f:
        f.write(docs)

readme = st.button('Generate Documentation')

if readme:
    if code:
        # Pass text from existing_docs to the function
        flag = isWithBug(code, selected_option)
        docs = generate_docs(code, selected_option, existing_docs)
        st.write(docs)
        if flag == "No errors found in the code.":
            st.success('Documentation generated successfully')
            save_to_readme(docs)
            st.success('Documentation saved to README.md')
        else:
            st.error('Errors found in the code. Please fix them and try again.')
    else:
        st.write('Please enter the code to generate documentation')
import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI


template = """
    Hier bekommst Du unterschiedliche Kundenrezensionen: {input}
    Bitte fasse diese kurz zusammen. 
    Berücksichtige hierbei:
    
    Übersetze die Antwort in folgende Sprache: {sprache}
    Berücksichtige bei Deiner Antwort, was für ein Fußballfan der Nutzer ist: {fan}
"""

#PromptTemplate variables definition
prompt = PromptTemplate(
    input_variables=["input", "sprache", "fan"],
    template=template,
)


#LLM and key loading function
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.9, openai_api_key=openai_api_key)
    return llm


#Page title and header
st.set_page_config(page_title="hurra")
st.header("Erste Demo")


#Intro: instructions
col1, col2 = st.columns(2)

with col1:
    st.markdown("bla bla")

with col2:
    st.write("Contact with [AI Accelera](https://aiaccelera.com) to build your AI Projects")


#Input OpenAI API Key
st.markdown("## Enter Your OpenAI API Key")

def get_openai_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input", type="password")
    return input_text

openai_api_key = get_openai_api_key()


# Input
st.markdown("## Hier die Rezension reinballern")

def get_draft():
    draft_text = st.text_area(label="Text", label_visibility='collapsed', placeholder="Your Text...", key="draft_input")
    return draft_text

draft_input = get_draft()

if len(draft_input.split(" ")) > 700:
    st.write("Please enter a shorter text. The maximum length is 700 words.")
    st.stop()

# Prompt template tunning options
col1, col2 = st.columns(2)
with col1:
    option_sprache = st.selectbox(
        'Welche Sprache möchtest Du',
        ('Schwedisch', 'Französisch'))
    
with col2:
    option_fan = st.selectbox(
        'Was für ein Fußballfan bist Du',
        ('Borussia Dortmund', 'VFL Bochum'))
    
    
# Output
st.markdown("### Your Re-written text:")

if draft_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. \
            Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', 
            icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_draft = prompt.format(
        sprache=option_sprache, 
        fan=option_fan, 
        input=draft_input
    )

    improved_redaction = llm(prompt_with_draft)

    st.write(improved_redaction)
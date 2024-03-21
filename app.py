import streamlit as st
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_openai import ChatOpenAI

#session state 
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "sotred_session" not in st.session_state:
    st.session_state["sotred_session"] = []

#define a function to get user input 
def get_text():
    """
    Get user input text.
    Return:
        (str): the text entered by the user
    """
    input_text = st.text_input("You:", st.session_state["input"],key="input", 
                               placeholder="Your AI assistant is here for your help",
                               label_visibility='hidden')
    return input_text
st.title("Chatbot")

api = st.sidebar.text_input("API-KEY",type="password")

if api:
    #create OpenAI instance
    # chat = ChatOpenAI(temperature=0, openai_api_key="YOUR_API_KEY", openai_organization="YOUR_ORGANIZATION_ID")
    llm = ChatOpenAI(
        temperature=0.57,
        openai_api_key = api,
        model_name = 'gpt-3.5-turbo',
        verbose= False
    )
    # Create conversational memory
    if 'entity_memory' not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm= llm, k=10)

    #create conversational chain
    Conversation = ConversationChain(
        llm= llm,
        prompt= ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=st.session_state.entity_memory
    )
else:
    st.error('No api found')    
#get the user input 
user_input = get_text()

#Generate output using conversationchain and the user
if user_input:
    output = Conversation.predict(input=user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

download_str = []
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="🧐")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append(st.session_state["past"][i])
        download_str.append(st.session_state["generated"][i])
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- Page Configuration ---
st.set_page_config(
    page_title="Custom ChatGPT Pro", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Custom CSS Styling for Colors & Visual Polish ---
st.markdown("""
    <style>
    /* Global background tint */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
    }
    
    /* Custom Header Gradient Title */
    .main-title {
        background: linear-gradient(90deg, #4f46e5, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
    }

    /* Modern Card Container for Login */
    .login-card {
        background: white;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
    }

    /* Style buttons with smooth transition */
    .stButton button {
        border-radius: 10px;
        font-weight: 600;
        background: linear-gradient(90deg, #4f46e5, #6366f1);
        color: white;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #4338ca, #4f46e5);
        color: white;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }

    /* Chat bubble spacing */
    .stChatMessage {
        border-radius: 14px;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'model_name' not in st.session_state:
    st.session_state.model_name = "gpt-4o-mini"
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.5

# --- 1. LOGIN / CONFIGURATION SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown('<h1 class="main-title" style="text-align: center;">Custom ChatGPT</h1>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6b7280;'>Unlock your personalized AI workspace with your OpenAI API Key.</p><br>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            api_key = st.text_input("🔑 OpenAI API Key", type="password", placeholder="sk-...")
            system_role = st.text_area("🧠 System Persona / Instructions", value="You are a helpful, creative, and smart AI assistant.")
            
            selected_model = st.selectbox(
                "⚡ Choose Model", 
                ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
            )
            
            submit = st.form_submit_button("🚀 Launch Workspace", use_container_width=True)
            
            if submit:
                if not api_key.strip():
                    st.warning("⚠️ Please enter a valid API key to proceed!")
                else:
                    st.session_state.api_key = api_key.strip()
                    st.session_state.model_name = selected_model
                    st.session_state.messages = [SystemMessage(content=system_role)]
                    st.session_state.logged_in = True
                    st.rerun()

# --- 2. MAIN CHAT SCREEN ---
else:
    # --- Sidebar Configuration Dashboard ---
    with st.sidebar:
        st.markdown("### 🤖 Control Panel")
        st.info(f"Active Model:\n`{st.session_state.model_name}`")
        
        st.session_state.temperature = st.slider(
            "🎨 Creativity (Temperature)", 
            min_value=0.0, 
            max_value=1.0, 
            value=st.session_state.temperature, 
            step=0.1
        )
        
        st.divider()
        
        # Session Analytics
        msg_count = max(0, len(st.session_state.messages) - 1)
        st.metric(label="💬 Messages Exchanged", value=msg_count)
        
        st.divider()
        
        if st.button("🧹 Clear Conversation", use_container_width=True):
            system_msg = st.session_state.messages[0]
            st.session_state.messages = [system_msg]
            st.rerun()
            
        if st.button("🚪 Logout / Switch Key", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.messages = []
            st.rerun()

    # --- Header Banner ---
    st.markdown('<h1 class="main-title">🤖 Custom ChatGPT Pro</h1>', unsafe_allow_html=True)
    st.caption("Interactive AI Chat Workspace • Styled with Custom CSS & Real-time Streaming")
    st.divider()

    # --- Initialize LLM ---
    chat = ChatOpenAI(
        model_name=st.session_state.model_name, 
        temperature=st.session_state.temperature,
        openai_api_key=st.session_state.api_key
    )

    # --- Quick Starter Chips (Shown only when chat is fresh) ---
    if len(st.session_state.messages) == 1:
        st.markdown("### ✨ Quick Starters")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            if st.button("🐍 Python Tricks", use_container_width=True):
                st.session_state.messages.append(HumanMessage(content="Give me 3 advanced Python code optimization tips."))
                st.rerun()
        with sc2:
            if st.button("🚀 Startup Idea", use_container_width=True):
                st.session_state.messages.append(HumanMessage(content="Suggest a unique AI-powered SaaS startup concept."))
                st.rerun()
        with sc3:
            if st.button("📊 Data Science", use_container_width=True):
                st.session_state.messages.append(HumanMessage(content="Explain how random forests work in machine learning."))
                st.rerun()
        st.divider()

    # --- Render Chat History ---
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="👤"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar="🤖"):
                st.write(msg.content)

    # --- New Message Input & Streaming Response ---
    if user_prompt := st.chat_input("Type your message here..."):
        # Display user message immediately
        st.session_state.messages.append(HumanMessage(content=user_prompt))
        with st.chat_message("user", avatar="👤"):
            st.write(user_prompt)

        # Stream assistant response in real time
        with st.chat_message("assistant", avatar="🤖"):
            try:
                def response_generator():
                    for chunk in chat.stream(st.session_state.messages):
                        yield chunk.content
                
                full_response = st.write_stream(response_generator())
                st.session_state.messages.append(AIMessage(content=full_response))
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
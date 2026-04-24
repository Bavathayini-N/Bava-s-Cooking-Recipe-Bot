# """
# app.py — Bava's Recipe Bot 🍳  Streamlit Interface
# ─────────────────────────────────────────
# A beautiful, interactive cooking-recipe chatbot powered by RAG + Groq.
# """

# import streamlit as st
# import os
# import sys
# import time

# # ━━━━━━━━━━━━━━━━━━━━━━━━  PAGE CONFIG  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# # Must be the VERY FIRST streamlit command
# st.set_page_config(
#     page_title="Bava's Recipe Bot 🍳",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ── project root on path ─────────────────────────────────────────────
# sys.path.insert(0, os.path.dirname(__file__))

# from ask_ai.chain import get_rag_chain

# # ━━━━━━━━━━━━━━━━━━━━━━━━  CUSTOM CSS  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# st.markdown("""
# <style>
# /* ── import Google Font ─────────────────────────────────── */
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

# /* ── global overrides ───────────────────────────────────── */
# html, body, [class*="css"] {
#     font-family: 'Inter', sans-serif;
# }

# .stApp {
#     background: linear-gradient(145deg, #0f0f1a 0%, #1a1a2e 40%, #16213e 100%);
# }

# /* ── sidebar styling ────────────────────────────────────── */
# section[data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
#     border-right: 1px solid rgba(255,255,255,0.06);
# }

# section[data-testid="stSidebar"] .stMarkdown p,
# section[data-testid="stSidebar"] .stMarkdown li {
#     color: #c0c0d0;
#     font-size: 0.9rem;
# }

# /* ── hero header ────────────────────────────────────────── */
# .hero-container {
#     text-align: center;
#     padding: 2rem 1rem 1.5rem;
# }
# .hero-title {
#     font-size: 3rem;
#     font-weight: 800;
#     background: linear-gradient(135deg, #f97316 0%, #f59e0b 50%, #ef4444 100%);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     margin-bottom: 0.3rem;
#     letter-spacing: -1px;
# }
# .hero-sub {
#     color: #a0a0b8;
#     font-size: 1.1rem;
#     font-weight: 400;
# }

# /* ── glass card ─────────────────────────────────────────── */
# .glass-card {
#     background: rgba(255, 255, 255, 0.04);
#     border: 1px solid rgba(255, 255, 255, 0.08);
#     border-radius: 16px;
#     padding: 1.8rem 2rem;
#     backdrop-filter: blur(12px);
#     -webkit-backdrop-filter: blur(12px);
#     margin-bottom: 1.2rem;
#     transition: border-color 0.3s ease;
# }
# .glass-card:hover {
#     border-color: rgba(249, 115, 22, 0.25);
# }

# /* ── chat bubbles ───────────────────────────────────────── */
# .user-bubble {
#     background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
#     color: #fff;
#     padding: 1rem 1.4rem;
#     border-radius: 18px 18px 4px 18px;
#     margin: 0.6rem 0;
#     max-width: 75%;
#     margin-left: auto;
#     font-size: 0.95rem;
#     box-shadow: 0 4px 20px rgba(249,115,22,0.25);
#     word-wrap: break-word;
# }

# .bot-bubble {
#     background: rgba(255,255,255,0.06);
#     border: 1px solid rgba(255,255,255,0.1);
#     color: #e0e0f0;
#     padding: 1.2rem 1.5rem;
#     border-radius: 18px 18px 18px 4px;
#     margin: 0.6rem 0;
#     max-width: 85%;
#     font-size: 0.95rem;
#     line-height: 1.7;
#     box-shadow: 0 4px 20px rgba(0,0,0,0.2);
#     word-wrap: break-word;
# }

# /* ── pulse animation for loading ────────────────────────── */
# @keyframes pulse {
#     0%, 100% { opacity: 0.4; }
#     50%      { opacity: 1;   }
# }
# .loading-dot {
#     display: inline-block;
#     width: 8px; height: 8px;
#     border-radius: 50%;
#     background: #f97316;
#     margin: 0 3px;
#     animation: pulse 1.2s infinite;
# }
# .loading-dot:nth-child(2) { animation-delay: 0.2s; }
# .loading-dot:nth-child(3) { animation-delay: 0.4s; }

# /* ── quick-chip buttons ─────────────────────────────────── */
# .chip {
#     display: inline-block;
#     background: rgba(249,115,22,0.12);
#     border: 1px solid rgba(249,115,22,0.3);
#     color: #f9a825;
#     padding: 0.45rem 1rem;
#     border-radius: 999px;
#     font-size: 0.82rem;
#     margin: 0.25rem 0.3rem;
#     cursor: pointer;
#     transition: all 0.25s ease;
# }
# .chip:hover {
#     background: rgba(249,115,22,0.25);
#     transform: translateY(-1px);
# }

# /* ── stat pill ──────────────────────────────────────────── */
# .stat-pill {
#     display: inline-flex;
#     align-items: center;
#     gap: 6px;
#     background: rgba(249,115,22,0.1);
#     border: 1px solid rgba(249,115,22,0.2);
#     padding: 0.35rem 0.9rem;
#     border-radius: 999px;
#     color: #f9a825;
#     font-size: 0.8rem;
#     font-weight: 500;
# }

# /* ── scrollbar ──────────────────────────────────────────── */
# ::-webkit-scrollbar { width: 6px; }
# ::-webkit-scrollbar-track { background: transparent; }
# ::-webkit-scrollbar-thumb {
#     background: rgba(249,115,22,0.3);
#     border-radius: 3px;
# }

# /* ── input field ────────────────────────────────────────── */
# .stTextInput > div > div > input {
#     background: rgba(255,255,255,0.06) !important;
#     border: 1px solid rgba(255,255,255,0.12) !important;
#     border-radius: 12px !important;
#     color: #e0e0f0 !important;
#     font-size: 1rem !important;
#     padding: 0.75rem 1rem !important;
# }
# .stTextInput > div > div > input:focus {
#     border-color: #f97316 !important;
#     box-shadow: 0 0 0 2px rgba(249,115,22,0.2) !important;
# }
# .stTextInput > div > div > input::placeholder {
#     color: rgba(255,255,255,0.35) !important;
# }

# /* ── FIX: Keep sidebar arrow visible ── */
# #MainMenu, footer { visibility: hidden; }
# header { background: transparent !important; }
# button[kind="headerNoContext"] { 
#     visibility: visible !important; 
#     color: #f97316 !important; 
# }
# </style>
# """, unsafe_allow_html=True)


# # ━━━━━━━━━━━━━━━━━━━━━━━━  SIDEBAR  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# with st.sidebar:
#     st.markdown("## 🍳 Bava's Recipe Bot")
#     st.markdown("---")
#     st.markdown("""
#     **How it works**
#     1. 🥕 Type your available ingredients
#     2. 🤖 AI gives you the best recipes and the instruction to make it
    
#     ---
#     **Powered by**
#     - 🧠 Groq — Llama 3.3 
#     - 🔗 LangChain RAG
#     - 📦 ChromaDB
#     ---
#     """)

#     if st.button("🗑️  Clear Chat", use_container_width=True):
#         st.session_state.messages = []
#         st.rerun()

#     st.markdown("""
#     <div style='text-align:center; margin-top:2rem;'>
#         <span class='stat-pill'>📚 5,000 recipes indexed</span>
#     </div>
#     """, unsafe_allow_html=True)


# # ━━━━━━━━━━━━━━━━━━━━━━  LOAD CHAIN (cached)  ━━━━━━━━━━━━━━━━━━━━━━
# @st.cache_resource(show_spinner=False)
# def load_chain():
#     with st.spinner("🔧 Loading recipe database & AI model …"):
#         return get_rag_chain()

# chain = load_chain()

# # ━━━━━━━━━━━━━━━━━━━━━━━━  HERO HEADER  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# st.markdown("""
# <div class="hero-container">
#     <div class="hero-title">Bava's Recipe Bot 🍳</div>
#     <div class="hero-sub">Tell me what's in your kitchen — I'll find the perfect recipe</div>
# </div>
# """, unsafe_allow_html=True)

# # ━━━━━━━━━━━━━━━━━━━━━━  SESSION STATE  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # ━━━━━━━━━━━━━━━━━━━━━━  QUICK SUGGESTIONS  ━━━━━━━━━━━━━━━━━━━━━━━━━
# if not st.session_state.messages:
#     # Adding a button here to help user find sidebar if it's closed
#     col1, col2, col3 = st.columns([1,2,1])
#     with col2:
#         if st.button("⬅️ Open Menu for Settings & Clear Chat", use_container_width=True):
#             st.info("The menu is in the top-left corner!")

#     st.markdown("""
#     <div class="glass-card" style="text-align:center;">
#         <p style="color:#c0c0d0; margin-bottom:0.8rem; font-size:0.95rem;">
#             ✨ Try one of these to get started
#         </p>
#         <div>
#             <span class="chip">🍗 chicken, garlic, butter</span>
#             <span class="chip">🍝 pasta, tomato, basil</span>
#             <span class="chip">🥚 eggs, cheese, spinach</span>
#             <span class="chip">🥩 beef, potatoes, onion</span>
#             <span class="chip">🐟 salmon, lemon, dill</span>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


# # ━━━━━━━━━━━━━━━━━━━━━━━━  CHAT HISTORY  ━━━━━━━━━━━━━━━━━━━━━━━━━━━
# for msg in st.session_state.messages:
#     if msg["role"] == "user":
#         st.markdown(f'<div class="user-bubble">🧑‍🍳 {msg["content"]}</div>',
#                     unsafe_allow_html=True)
#     else:
#         st.markdown(f'<div class="bot-bubble">🍳 {msg["content"]}</div>',
#                     unsafe_allow_html=True)


# # ━━━━━━━━━━━━━━━━━━━━━━━━  INPUT  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# user_input = st.chat_input("Enter your ingredients (e.g. chicken, garlic, lemon) …")

# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     st.markdown(f'<div class="user-bubble">🧑‍🍳 {user_input}</div>',
#                 unsafe_allow_html=True)

#     with st.spinner(""):
#         placeholder = st.empty()
#         placeholder.markdown("""
#         <div class="bot-bubble" style="max-width:180px;">
#             <span class="loading-dot"></span>
#             <span class="loading-dot"></span>
#             <span class="loading-dot"></span>
#             <span style="color:#888; margin-left:6px; font-size:0.85rem;">cooking up ideas …</span>
#         </div>
#         """, unsafe_allow_html=True)

#         response = chain.invoke(user_input)
#         placeholder.empty()

#     st.session_state.messages.append({"role": "assistant", "content": response})
#     st.markdown(f'<div class="bot-bubble">🍳 {response}</div>',
#                 unsafe_allow_html=True)
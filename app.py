"""
Roorkee Help AI Agent - Streamlit Application
Interactive city guide, emergency helper, directory explorer, and Fetch.ai agent hub.
"""

import streamlit as st
import os
import urllib.parse
from typing import List, Dict, Any

from knowledge_base import (
    ROORKEE_CATEGORIES,
    ROORKEE_PLACES,
    EMERGENCY_NUMBERS,
    ROORKEE_FACTS,
    search_roorkee_places,
    get_emergency_info,
    get_category_counts
)
from agent import RoorkeeAIAgent
from fetchai_service import FetchAIAgentBridge

# --- PAGE CONFIGURATION ---
st.set_page_state = None
st.set_page_config(
    page_title="Roorkee Help AI Agent",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Main container styling */
    .main-header {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    .main-header p {
        color: #e0f2fe;
        font-size: 1.05rem;
        margin-bottom: 0;
    }
    
    /* Place Card Styling */
    .place-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .place-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        font-size: 0.8rem;
        font-weight: 600;
        border-radius: 9999px;
        margin-bottom: 0.5rem;
    }
    .badge-emergency { background-color: #fee2e2; color: #991b1b; }
    .badge-education { background-color: #e0e7ff; color: #3730a3; }
    .badge-heritage { background-color: #fef3c7; color: #92400e; }
    .badge-food { background-color: #ffedd5; color: #9a3412; }
    .badge-transport { background-color: #e0f2fe; color: #075985; }
    .badge-markets { background-color: #f3e8ff; color: #6b21a8; }
    .badge-civic { background-color: #dcfce7; color: #166534; }
    .badge-student { background-color: #f1f5f9; color: #334155; }
    
    /* Emergency Speed Dial Cards */
    .dial-card {
        background: #fff1f2;
        border-left: 5px solid #e11d48;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.8rem;
    }
    .dial-num {
        font-size: 1.4rem;
        font-weight: 700;
        color: #be123c;
    }
    
    /* Info chips */
    .info-chip {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 0.4rem 0.8rem;
        font-size: 0.85rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)


# --- INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 **Namaste! Welcome to Roorkee Help AI Agent.**\n\n"
                "I am your dedicated digital companion for everything about **Roorkee, Uttarakhand**.\n"
                "Ask me about:\n"
                "- 🚨 **Emergency & Hospitals** (Civil Hospital, 24/7 doctors, Police, Fire)\n"
                "- 🎓 **IIT Roorkee** (Thomason College history, departments, fests like Thomso)\n"
                "- 🏰 **Heritage & Tourism** (Solani Aqueduct, Piran Kaliyar Dargah, Canal)\n"
                "- 🍛 **Food & Sweets** (Prakash Sweets, Prem Sweets, Bedmi Puri, Civil Lines)\n"
                "- 🚂 **Transport & Travel** (Trains from RK, buses to Delhi/Haridwar, distances)\n"
                "- 🏠 **Student Living** (PGs in Solani Puram, Awas Vikas, weather & tips)\n\n"
                "You can also click any of the quick suggestions below to start!"
            ),
            "envelope": None
        }
    ]

if "api_provider" not in st.session_state:
    st.session_state.api_provider = "local"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "last_query" not in st.session_state:
    st.session_state.last_query = ""


# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.markdown("### 🤖 Agent & Model Settings")

    api_choice = st.selectbox(
        "AI Reasoning Mode:",
        [
            "Built-in Roorkee Knowledge Engine (Offline & Fast)",
            "Fetch.ai Agentverse REST API",
            "Google Gemini API"
        ],
        index=0
    )

    if "Fetch.ai" in api_choice:
        st.session_state.api_provider = "agentverse"
        user_key = st.text_input(
            "Fetch.ai / Agentverse API Key:",
            value=st.session_state.api_key,
            type="password",
            help="Get your key at https://agentverse.ai under Profile -> API Keys"
        )
        st.session_state.api_key = user_key
        st.caption("ℹ️ Connects to Fetch.ai Agentverse network for agent search and chat.")
    elif "Gemini" in api_choice:
        st.session_state.api_provider = "gemini"
        user_key = st.text_input(
            "Google Gemini API Key:",
            value=st.session_state.api_key,
            type="password",
            help="Get your free Gemini API key at https://aistudio.google.com"
        )
        st.session_state.api_key = user_key
        st.caption("ℹ️ Enhances grounded Roorkee knowledge with Gemini natural language generation.")
    else:
        st.session_state.api_provider = "local"
        st.caption("⚡ **100% Offline Mode Active:** Powered by curated, verified Roorkee knowledge base.")

    st.divider()

    # Fetch.ai Node Identity Card
    bridge = FetchAIAgentBridge(api_key=st.session_state.api_key)
    node_id = bridge.get_agent_identity()

    st.markdown("#### 🌐 Fetch.ai Agent Identity")
    st.markdown(f"**Name:** `{node_id['name']}`")
    st.markdown(f"**Protocol:** `{node_id['protocol']}`")
    st.markdown(f"**Address:**")
    st.code(node_id['address'], language="text")
    st.markdown(f"**Status:** 🟢 `{node_id['status']}`")

    st.divider()

    # City Quick Metrics
    st.markdown("#### 📍 Roorkee Quick Facts")
    st.markdown(f"- **PIN Code:** `{ROORKEE_FACTS['pin_code']}`")
    st.markdown(f"- **STD Code:** `{ROORKEE_FACTS['std_code']}`")
    st.markdown(f"- **Railway Code:** `{ROORKEE_FACTS['major_station']}`")
    st.markdown(f"- **District:** `{ROORKEE_FACTS['district']}`")
    st.markdown(f"- **State:** `{ROORKEE_FACTS['state']}`")

    st.divider()
    st.caption("Made with ❤️ for students, residents, and visitors of Roorkee.")


# --- MAIN HEADER ---
st.markdown("""
<div class="main-header">
    <h1>🏛️ Roorkee Help AI Agent</h1>
    <p>Your intelligent, all-in-one assistant for Roorkee, Uttarakhand — IIT Roorkee, Solani Aqueduct, Emergency Services, Food, Transport & City Guide.</p>
</div>
""", unsafe_allow_html=True)


# --- TABS NAVIGATION ---
tab_chat, tab_directory, tab_emergency, tab_fetchai, tab_guide = st.tabs([
    "💬 AI Chat Assistant",
    "🔎 Explore Roorkee Directory",
    "🚨 Emergency & Helplines",
    "🌐 Fetch.ai Agent Network",
    "🗺️ Travel & Distances"
])


# Initialize Agent
agent = RoorkeeAIAgent(
    api_key=st.session_state.api_key if st.session_state.api_provider != "local" else None,
    api_provider=st.session_state.api_provider
)


# ==============================================================================
# TAB 1: AI CHAT ASSISTANT
# ==============================================================================
with tab_chat:
    st.markdown("##### 💡 Suggested Questions (Click any to ask immediately):")
    
    col1, col2, col3 = st.columns(3)
    quick_queries = [
        ("🚨 Emergency Helplines & Hospitals", "What are the emergency contact numbers and hospitals in Roorkee?"),
        ("🎓 IIT Roorkee & Thomason History", "Tell me about IIT Roorkee history, fests, and campus landmarks."),
        ("🍛 Best Street Food & Sweets", "What are the famous sweets, kachoris, and food places in Roorkee?"),
        ("🏰 Solani Aqueduct & Piran Kaliyar", "Tell me about Solani Aqueduct and Piran Kaliyar Dargah."),
        ("🚂 How to Reach Roorkee (Trains/Buses)", "How can I travel to Roorkee from Delhi and Haridwar?"),
        ("🏠 Student PG & Accommodation Areas", "Where can students find PGs, hostels, or flats in Roorkee?")
    ]
    
    selected_quick_prompt = None
    with col1:
        if st.button(quick_queries[0][0], use_container_width=True):
            selected_quick_prompt = quick_queries[0][1]
        if st.button(quick_queries[1][0], use_container_width=True):
            selected_quick_prompt = quick_queries[1][1]
    with col2:
        if st.button(quick_queries[2][0], use_container_width=True):
            selected_quick_prompt = quick_queries[2][1]
        if st.button(quick_queries[3][0], use_container_width=True):
            selected_quick_prompt = quick_queries[3][1]
    with col3:
        if st.button(quick_queries[4][0], use_container_width=True):
            selected_quick_prompt = quick_queries[4][1]
        if st.button(quick_queries[5][0], use_container_width=True):
            selected_quick_prompt = quick_queries[5][1]

    st.divider()

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("envelope"):
                with st.expander("🔍 View Fetch.ai Protocol Message Envelope", expanded=False):
                    st.json(msg["envelope"])

    # Handle Input (Chat Box or Quick Prompt)
    user_query = st.chat_input("Ask anything about Roorkee (e.g., 'Hospital near me', 'Best sweets', 'How to reach IIT')")
    
    active_prompt = user_query or selected_quick_prompt

    if active_prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": active_prompt})
        with st.chat_message("user"):
            st.markdown(active_prompt)

        # Generate response using Roorkee AI Agent
        with st.spinner("🤖 Roorkee AI Agent is analyzing knowledge base & routing..."):
            result = agent.generate_response(active_prompt)
            bot_reply = result["answer"]
            envelope = result.get("agent_envelope")

        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_reply,
            "envelope": envelope
        })
        
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
            if envelope:
                with st.expander("🔍 View Fetch.ai Protocol Message Envelope", expanded=False):
                    st.json(envelope)

        st.rerun()


# ==============================================================================
# TAB 2: EXPLORE DIRECTORY
# ==============================================================================
with tab_directory:
    st.markdown("### 🔎 Roorkee Places & Directory Explorer")
    st.caption("Search across institutions, hospitals, restaurants, markets, and tourist spots.")

    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        search_kw = st.text_input("🔍 Search by name, keyword or service:", placeholder="e.g. hospital, sweets, library, train, hostel, pizza")
    with f_col2:
        cat_options = ["all"] + list(ROORKEE_CATEGORIES.keys())
        cat_labels = ["All Categories"] + [ROORKEE_CATEGORIES[k] for k in ROORKEE_CATEGORIES.keys()]
        selected_cat_idx = st.selectbox(
            "Filter Category:",
            range(len(cat_options)),
            format_func=lambda i: cat_labels[i]
        )
        selected_cat = cat_options[selected_cat_idx]

    # Query Knowledge Base
    results = search_roorkee_places(search_kw or "", category=selected_cat)

    st.markdown(f"**Showing {len(results)} verified places in Roorkee:**")

    badge_classes = {
        "emergency": "badge-emergency",
        "education": "badge-education",
        "heritage": "badge-heritage",
        "food": "badge-food",
        "transport": "badge-transport",
        "markets": "badge-markets",
        "civic": "badge-civic",
        "student_living": "badge-student"
    }

    # Render Cards in 2 Columns
    cols = st.columns(2)
    for i, place in enumerate(results):
        col = cols[i % 2]
        with col:
            category_label = ROORKEE_CATEGORIES.get(place['category'], place['category'].title())
            b_class = badge_classes.get(place['category'], "badge-student")
            
            maps_query = urllib.parse.quote(f"{place['name']} Roorkee Uttarakhand")
            maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"

            st.markdown(f"""
            <div class="place-card">
                <span class="badge {b_class}">{category_label}</span>
                <h4 style="margin: 0.2rem 0; color: #1e293b;">{place['name']}</h4>
                <p style="color: #64748b; font-size: 0.88rem; margin-bottom: 0.5rem;">
                    📍 <b>Address:</b> {place['address']}
                </p>
                <div style="font-size: 0.9rem; margin-bottom: 0.5rem;">
                    <b>📞 Contact:</b> <code>{place.get('contact', 'N/A')}</code><br>
                    <b>⏰ Timings:</b> {place.get('timing', 'N/A')}<br>
                    <b>🏷️ Type:</b> {place.get('type', 'Public')}
                </div>
                <p style="font-size: 0.92rem; color: #334155; line-height: 1.45;">
                    {place['highlights']}
                </p>
                <a href="{maps_url}" target="_blank" style="text-decoration: none; color: #2563eb; font-size: 0.85rem; font-weight: 600;">
                    🗺️ Open in Google Maps ↗
                </a>
            </div>
            """, unsafe_allow_html=True)


# ==============================================================================
# TAB 3: EMERGENCY SPEED DIAL
# ==============================================================================
with tab_emergency:
    st.markdown("### 🚨 Roorkee Emergency Helplines & Rapid Assistance")
    st.warning("⚠️ For life-threatening emergencies, dial **112** (Universal Emergency Response) or **108** (Ambulance) immediately.")

    dial_cols = st.columns(2)
    for idx, item in enumerate(EMERGENCY_NUMBERS):
        c = dial_cols[idx % 2]
        with c:
            st.markdown(f"""
            <div class="dial-card">
                <div class="dial-num">📞 {item['number']}</div>
                <h4 style="margin: 0.3rem 0; color: #1e293b;">{item['service']}</h4>
                <p style="margin: 0; color: #475569; font-size: 0.9rem;">{item['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🏥 24/7 Hospitals in Roorkee")
    hospitals = [p for p in ROORKEE_PLACES if p["category"] == "emergency" and "hospital" in p["id"]]
    h_cols = st.columns(len(hospitals))
    for idx, h in enumerate(hospitals):
        with h_cols[idx]:
            st.info(f"**{h['name']}**\n\n📍 {h['address']}\n\n📞 `{h['contact']}`\n\n⏰ {h['timing']}")

    st.markdown("#### 🩸 Blood Banks & Pharmacy Tips")
    st.markdown("""
    - **Civil Hospital Blood Centre:** Located inside Civil Hospital premises, open 24/7 for emergency blood supply.
    - **Rotary Blood Bank Roorkee:** Dedicated community blood service (`+91-9837055522`).
    - **24-Hour Medical Stores:** Aggarwal Medicos (Civil Lines), Apollo Pharmacy, Sanjeevani Medical Store near Boat Club.
    """)


# ==============================================================================
# TAB 4: FETCH.AI AGENT NETWORK
# ==============================================================================
with tab_fetchai:
    st.markdown("### 🌐 Fetch.ai Agentverse & Autonomous Agent Hub")
    st.markdown("""
    This application integrates with the **Fetch.ai / ASI Alliance** autonomous agent architecture.
    Each query to Roorkee Help can be signed and formatted into an autonomous **uAgent communication envelope**.
    """)

    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.markdown("#### 🆔 Local Roorkee Agent Node")
        st.json(node_id)
        
        st.markdown("#### 📡 Agent Protocol Capabilities")
        for cap in node_id["capabilities"]:
            st.markdown(f"- ✅ {cap}")

    with c_right:
        st.markdown("#### 🔍 Test Fetch.ai Agent Discovery")
        st.caption("Search Agentverse marketplace for peer agents (e.g. 'transit', 'weather', 'hotel'):")
        agent_search_query = st.text_input("Search Agentverse Query:", value="transit")
        
        if st.button("🚀 Search Agent Network", use_container_width=True):
            with st.spinner("Querying Fetch.ai network..."):
                search_res = bridge.search_agentverse_agents(agent_search_query)
                if search_res.get("success"):
                    st.success(f"Discovered Agents ({search_res.get('source')}):")
                    st.json(search_res.get("data"))
                else:
                    st.error(f"Error: {search_res.get('error')}")

        st.markdown("#### 📬 Simulate uAgent Envelope Transmission")
        test_msg = st.text_input("Test message to Roorkee Agent:", value="Where is Civil Hospital?")
        if st.button("📨 Dispatch Fetch.ai Envelope", use_container_width=True):
            test_envelope = bridge.send_agent_envelope("client_tester", test_msg)
            st.success("Envelope delivered to local agent queue!")
            st.json(test_envelope)


# ==============================================================================
# TAB 5: TRAVEL, DISTANCES & LIVING GUIDE
# ==============================================================================
with tab_guide:
    st.markdown("### 🗺️ City Travel, Connectivity & Distances")
    
    g_col1, g_col2 = st.columns([1, 1])

    with g_col1:
        st.markdown("#### 🚗 Road Distances from Roorkee")
        dist_data = [{"Destination City": k, "Distance": v} for k, v in ROORKEE_FACTS["key_distance"].items()]
        st.table(dist_data)

    with g_col2:
        st.markdown("#### 🚆 Train Travel Tips (Roorkee RK)")
        st.markdown("""
        - **To New Delhi (NDLS):**
          - *Dehradun Shatabdi (12018):* Departs ~18:15, reaches NDLS ~21:50.
          - *Vande Bharat Express:* Fast, premium connectivity.
          - *Jan Shatabdi Express (12056):* Economical morning & evening connectivity.
        - **To Haridwar / Dehradun:**
          - Frequent local express trains and Shatabdi run every 1-2 hours.
        - **Station Facilities:** Cloak room, computerized reservation counter, IRCTC food stalls, pre-paid auto stand.
        """)

    st.markdown("---")
    st.markdown("#### 🌤️ Weather, Climate & When to Visit")
    st.markdown("""
    | Season | Months | Temperature | Recommended Activities |
    | :--- | :--- | :--- | :--- |
    | **Winter** | Oct - Mar | 7°C - 24°C | **Best time to visit!** Solani Aqueduct walks, Piran Kaliyar, campus tours. |
    | **Summer** | Apr - Jun | 24°C - 40°C | Early morning walks along the canal, Crystal World Water Park. |
    | **Monsoon** | Jul - Sep | 22°C - 32°C | Scenic lush canal views; carry rain gear. |
    """)

    st.markdown("#### 🎓 Guide for New IIT Roorkee & College Students")
    st.markdown("""
    1. **Campus Gates:** The **Century Gate** leads straight to Civil Lines market and food street. The **Main Gate** faces the highway towards Haridwar.
    2. **Station to Campus:** Takes only 10 minutes by e-rickshaw (fares approx Rs 15-20 shared, or Rs 60-80 reserved).
    3. **Academic Essentials:** Printing and stationery shops are plentiful along Century Gate lane and BSM Chowk.
    4. **Hostel & Bhawan Deliveries:** Amazon, Flipkart, Swiggy, and Zomato deliver to all main IIT gates and hostel pickup points.
    """)

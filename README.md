# 🏛️ Roorkee Help AI Agent

An intelligent, full-stack AI Assistant and directory for **Roorkee, Uttarakhand (India)**. Built with **Streamlit**, **Fetch.ai uAgents Protocol Bridge**, and a curated **Roorkee Local Knowledge Engine**.

Designed for students (IIT Roorkee, COER, RIT, Quantum), residents, and tourists visiting the historic city of Roorkee.

---

## 🌟 Features

### 1. 💬 AI Chat Assistant (Tab 1)
- **Natural Language Answers:** Ask questions about hospitals, tourist attractions, food, fests, hostels, and commute.
- **Quick Action Chips:** One-click prompts for immediate answers:
  - *Emergency Helplines & Hospitals*
  - *IIT Roorkee & Thomason College History*
  - *Best Street Food & Sweets*
  - *Solani Aqueduct & Piran Kaliyar Dargah*
  - *Trains & Buses to Delhi / Haridwar*
  - *Student PG & Living Localities*
- **Fetch.ai Protocol Envelope:** Each query creates a structured, cryptographic message envelope compatible with the Fetch.ai autonomous agent network.

### 2. 🔎 Explore Roorkee Directory (Tab 2)
- **Interactive Search & Category Filter:**
  - 🚨 Emergency & Healthcare (Civil Hospital, Aarogyam, Vinay Vishal, IIT Hospital, 24/7 Blood Banks)
  - 🎓 Education & Research (IIT Roorkee, CSIR-CBRI, NIH, BEG Bengal Sappers, COER, RIT, Montfort)
  - 🏰 Heritage & Tourism (Solani Aqueduct 1854, Piran Kaliyar Sharif, Upper Ganges Canal, Crystal World)
  - 🍛 Food & Sweets (Prakash Sweets, Prem Sweets, Bedmi Puri & Kachori, Civil Lines Food Street)
  - 🚂 Transport & Connectivity (Roorkee Railway Station RK, Bus Stand, e-rickshaws, airports)
  - 🛍️ Markets & Shopping (Civil Lines Market, Main Bazaar, BSM Chowk)
  - 🏛️ Civic & Utilities (Nagar Nigam, UPCL Electricity 1912, Head Post Office 247667)
  - 🏠 Student Living & PG Guide (Solani Puram, Awas Vikas, Ramnagar, rental estimates)
- **Direct Navigation:** Every place card has a 1-click **Open in Google Maps ↗** link.

### 3. 🚨 Emergency Speed Dial (Tab 3)
- Instant high-visibility emergency cards for **112 (Universal)**, **108 (Ambulance)**, **101 (Fire Station)**, **01332-265100 (Civil Hospital)**, **1090 (Women Helpline)**, and **1912 (Electricity)**.
- Hospital casualty desks, blood banks, and 24-hour pharmacies.

### 4. 🌐 Fetch.ai Agentverse Hub (Tab 4)
- **Local Agent Node Details:** Agent address (`agent1q...`), protocol (`roorkee.civic.help.v1`), and live status.
- **Agentverse Marketplace Search:** Test discovery of peer agents across the network.
- **uAgent Message Simulation:** Test sending and inspecting protocol message envelopes.

### 5. 🗺️ Travel & Distances Guide (Tab 5)
- Road distance matrix: Haridwar (30 km), Rishikesh (55 km), Dehradun (70 km), Delhi (170 km), Mussoorie (98 km).
- Train schedules and tips for Shatabdi, Vande Bharat, and Jan Shatabdi.
- Seasonal weather guide and tips for new college students.

---

## 🚀 How to Run

### Step 1: Open Terminal in VS Code
Ensure you are in the project folder:
```powershell
cd "c:\Users\suraj\OneDrive\Documents\ROORKEE HELP"
```

### Step 2: Launch the Streamlit App
Run:
```powershell
python -m streamlit run app.py
```
*(Or double-click `run.bat` / run `.\run.ps1`)*

The web app will automatically open in your browser at `http://localhost:8501`.

---

## 💻 Terminal CLI Mode
You can also chat with the Roorkee AI Agent directly inside your VS Code terminal without launching a browser:
```powershell
python cli.py
```

---

## ⚙️ AI Models & API Setup (Optional)
The agent works **100% offline out-of-the-box** using its verified local database.

If you wish to enable external AI cloud models:
1. **Fetch.ai / Agentverse:**
   - Get a free API key at [agentverse.ai](https://agentverse.ai) (under *Profile → API Keys*).
   - Enter it in the app's sidebar under *AI Reasoning Mode → Fetch.ai Agentverse*.
2. **Google Gemini:**
   - Get a free API key at [aistudio.google.com](https://aistudio.google.com).
   - Enter it in the app's sidebar under *AI Reasoning Mode → Google Gemini API*.

---

## 📁 File Structure
```
ROORKEE HELP/
│
├── app.py                  # Main Streamlit web application & UI
├── agent.py                # AI Agent reasoning engine & intent router
├── knowledge_base.py       # Comprehensive Roorkee database & search engine
├── fetchai_service.py      # Fetch.ai Agentverse REST client & protocol bridge
├── cli.py                  # Terminal CLI chat interface
├── requirements.txt        # Python library dependencies
├── .env.example            # Environment variables template
├── run.bat                 # Windows batch launcher
├── run.ps1                 # PowerShell launcher
└── README.md               # Documentation and guide
```

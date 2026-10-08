# 🚀 Guide: Deploying Roorkee Help AI Agent to Agentverse (Fetch.ai)

This step-by-step guide walks you through deploying your **Roorkee Help Autonomous AI Agent** onto **Agentverse** ([agentverse.ai](https://agentverse.ai)).

Once deployed, your agent will run **24/7 in the Fetch.ai cloud**, completely free, without needing your computer to be turned on!

---

## 📋 Prerequisites
1. A web browser.
2. The code file ready: [`agentverse_agent.py`](agentverse_agent.py) (created in your folder).

---

## 🛠️ Step-by-Step Deployment Instructions

### Step 1: Log in to Agentverse
1. Go to **[https://agentverse.ai](https://agentverse.ai)**
2. Click **Log In** / **Sign Up** (You can sign in with your Google account or Web3 wallet).

---

### Step 2: Create a New Agent
1. In the left navigation menu, click on **"My Agents"** (or **"Agents"**).
2. Click the blue **"+ New Agent"** button in the top right.
3. Select **"Blank Agent"** (or Custom Agent).
4. Give your agent a name: `Roorkee Help AI Agent`

---

### Step 3: Paste the Agent Code
1. In VS Code, open the file: **[`agentverse_agent.py`](agentverse_agent.py)**
2. Press `Ctrl + A` to select all code, then `Ctrl + C` to copy it.
3. In your browser on the Agentverse code editor, select and delete any existing template code.
4. Paste the copied code into the Agentverse editor (`Ctrl + V`).

---

### Step 4: Start Your Cloud Agent
1. Click the **"Start"** (or **"Run"**) button at the top right of the Agentverse editor.
2. In the bottom **Log Console**, you will see your agent start up:
   ```text
   INFO: 🏛️ Roorkee Help Agent is ONLINE on Fetch.ai network!
   INFO: Agent Address: agent1q...
   INFO: Serving information for Roorkee, Uttarakhand (Emergency, IIT, Heritage, Food, Transport).
   ```
3. Copy your unique **Agent Address** (it begins with `agent1q...`). This is your agent's cryptographic public identity on the Fetch.ai Almanac network!

---

### Step 5: Test Your Agent in Agentverse
1. In the Agentverse agent panel, click on the **"Chat"** or **"Test"** tab.
2. Type any message to test it:
   - *"What are the emergency numbers in Roorkee?"*
   - *"Tell me about IIT Roorkee and its history."*
   - *"Where can I get the best sweets and kachoris?"*
   - *"How can I reach Roorkee by train?"*
   - *"Tell me about Solani Aqueduct."*
3. Your agent will respond instantly with verified, grounded Roorkee information!

---

### Step 6: (Optional) Connect Local Streamlit App to Agentverse
If you want your local Streamlit app to interact with your Agentverse account:
1. In Agentverse, click your **Profile icon** (top right) → **API Keys**.
2. Click **Create API Key** and copy the generated key.
3. Open your Streamlit app at `http://localhost:8501`.
4. In the left sidebar under **AI Reasoning Mode**, choose **Fetch.ai Agentverse REST API** and paste your API key!

---

## 🌟 Congratulations!
Your Roorkee Help AI Agent is now an autonomous, decentralized AI entity live on the global Fetch.ai / ASI Alliance network! 🌐

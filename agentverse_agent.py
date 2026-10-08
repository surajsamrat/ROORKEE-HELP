"""
Roorkee Help AI Agent for Agentverse (agentverse.ai)
===================================================
PASTE THIS ENTIRE FILE INTO THE AGENTVERSE CODE EDITOR (agent.py).
This script is fully optimized for Agentverse hosted containers:
- Zero external package dependencies (pure uAgents).
- Standard Agent() constructor for cloud runners.
- Direct @agent decorators without complex protocols.
- No agent.run() block (Agentverse manages lifecycle automatically).
"""

from uagents import Agent, Context, Model

# ==============================================================================
# 1. MESSAGE SCHEMAS
# ==============================================================================
class Request(Model):
    text: str

class Response(Model):
    text: str

class Message(Model):
    message: str


# ==============================================================================
# 2. ROORKEE KNOWLEDGE BASE & SEARCH ENGINE
# ==============================================================================
def get_roorkee_info(query: str) -> str:
    q = query.lower()

    # 1. EMERGENCY & HOSPITALS
    if any(k in q for k in ["emergency", "hospital", "doctor", "ambulance", "police", "kotwali", "fire", "blood"]):
        return (
            "🚨 **Roorkee Emergency Helplines & Hospitals**:\n\n"
            "• **Universal Police/Fire/Ambulance:** 112\n"
            "• **Civil Hospital Roorkee (24/7 Casualty):** 01332-265100 / 102\n"
            "• **Ambulance Service:** 108\n"
            "• **Roorkee Fire Station:** 101 / 01332-272101\n"
            "• **Civil Lines Police Kotwali:** 01332-264100\n"
            "• **Women Helpline Uttarakhand:** 1090\n"
            "• **UPCL Electricity Breakdown:** 1912\n\n"
            "🏥 **Prominent Hospitals:**\n"
            "- **Civil Hospital Roorkee:** Near Boat Club, Civil Lines (Ayushman Bharat cashless, 24/7 emergency)\n"
            "- **Aarogyam Medical College & Hospital:** Roorkee-Haridwar Highway (Multi-speciality, ICU)\n"
            "- **Vinay Vishal Healthcare:** Civil Lines (Trauma & surgery)\n"
            "- **IIT Roorkee Hospital:** Dedicated student and staff health centre"
        )

    # 2. IIT ROORKEE & EDUCATION
    if any(k in q for k in ["iit", "thomason", "thomso", "cognizance", "cbri", "nih", "college", "school", "engineering"]):
        return (
            "🎓 **IIT Roorkee & National Research Institutions**:\n\n"
            "• **IIT Roorkee (Est. 1847):** Asia's oldest technical institution! Founded as Thomason College of Civil Engineering. Granted university status in 1949 and IIT status in 2001.\n"
            "• **Key Campus Spots:** James Thomason Main Building, Mahatma Gandhi Central Library, Senate House, Convocation Hall, MAC (Multi Activity Centre).\n"
            "• **Annual Festivals:** Thomso (Cultural Fest in autumn, one of North India's biggest) & Cognizance (Technical festival in spring).\n"
            "• **CSIR-CBRI:** Central Building Research Institute — premier national lab for building science and earthquake-resistant structures.\n"
            "• **NIH:** National Institute of Hydrology under Ministry of Jal Shakti.\n"
            "• **BEG & Centre (Bengal Sappers):** Historic Indian Army combat engineering cantonment and War Memorial."
        )

    # 3. HERITAGE & TOURISM
    if any(k in q for k in ["solani", "aqueduct", "kaliyar", "dargah", "canal", "gang nahar", "history", "visit", "tourist"]):
        return (
            "🏰 **Roorkee Heritage & Tourist Spots**:\n\n"
            "1. **Solani Aqueduct (1854):** An engineering wonder built by Sir Proby Cautley to carry the Upper Ganges Canal across the Solani river valley. Features 15 masonry arches with famous carved stone lions.\n"
            "2. **Piran Kaliyar Sharif (Dargah):** Revered 13th-century Sufi shrine of Hazrat Sabir Piya (~7 km from Roorkee), symbol of spiritual peace and unity. Millions visit during the annual Urs.\n"
            "3. **Upper Ganges Canal (Gang Nahar):** Scenic canal splitting Roorkee with morning walk and jogging tracks.\n"
            "4. **Crystal World Water & Theme Park:** 29-acre amusement park on NH-58 near Roorkee."
        )

    # 4. FOOD, SWEETS & RESTAURANTS
    if any(k in q for k in ["food", "sweet", "mithai", "prakash", "prem", "kachori", "eat", "restaurant", "cafe", "dhaba"]):
        return (
            "🍛 **Famous Food & Sweets in Roorkee**:\n\n"
            "• **Prakash Sweets (Civil Lines & Main Bazaar):** Legendary Balushahi, Rasmalai, Ghewar, Desi Ghee Jalebi, and morning Bedmi Puri & Chole Bhature.\n"
            "• **Prem Sweets (Civil Lines):** Famous for Kaju Katli, Bengali sweets, and evening hot Samosas.\n"
            "• **Morning Kachoris:** Spicy urad dal kachoris with aloo-methi sabzi near Nehru Stadium.\n"
            "• **Civil Lines Food Street:** Domino's, Pizza Hut, Subway, Cafe Coffee Day, kathi rolls, and momo corners."
        )

    # 5. TRAVEL, TRAINS & BUSES
    if any(k in q for k in ["train", "railway", "station", "bus", "transport", "reach", "travel", "airport", "distance"]):
        return (
            "🚂 **Transport & Travel Guide for Roorkee**:\n\n"
            "• **Railway Station (Code: RK):** Direct Shatabdi (12017/18), Vande Bharat, and Jan Shatabdi to New Delhi (3 - 3.5 hrs). Direct trains to Haridwar, Dehradun, Lucknow, Kolkata, and Mumbai.\n"
            "• **Roadways Bus Stand (BSM Chowk):** Frequent UTC buses to Delhi ISBT Kashmere Gate (every 30 mins), Haridwar (45 mins), Dehradun (2 hrs).\n"
            "• **Nearest Airports:** Jolly Grant Airport, Dehradun (DED, ~68 km) & Delhi IGI Airport (DEL, ~185 km).\n\n"
            "📍 **Road Distances:**\n"
            "- Haridwar: 30 km\n"
            "- Rishikesh: 55 km\n"
            "- Dehradun: 70 km\n"
            "- New Delhi: 170 km\n"
            "- Mussoorie: 98 km"
        )

    # 6. DEFAULT CITY OVERVIEW
    return (
        "🏛️ **Roorkee Help Autonomous AI Agent (Uttarakhand)**\n\n"
        "I am your 24/7 cloud guide for Roorkee (PIN Code: 247667).\n\n"
        "Ask me about:\n"
        "• 🚨 **Emergency:** Police, Fire, Ambulance, Civil Hospital contacts\n"
        "• 🎓 **IIT Roorkee:** History (Thomason College 1847), campus landmarks & fests\n"
        "• 🏰 **Heritage:** Solani Aqueduct, Piran Kaliyar Dargah, Ganges Canal\n"
        "• 🍛 **Food:** Prakash Sweets, Prem Sweets, Bedmi Puri, Kachori\n"
        "• 🚂 **Transport:** Trains from RK, buses to Delhi/Haridwar, road distances"
    )


# ==============================================================================
# 3. AGENT DEFINITION (For Agentverse Cloud)
# ==============================================================================
# In Agentverse, use Agent() with no parameters so the cloud manages credentials.
agent = Agent()


# ==============================================================================
# 4. EVENT & MESSAGE HANDLERS
# ==============================================================================
@agent.on_event("startup")
async def startup_handler(ctx: Context):
    ctx.logger.info("==================================================")
    ctx.logger.info("🏛️ ROORKEE HELP AI AGENT IS ONLINE ON AGENTVERSE!")
    ctx.logger.info(f"Agent Address: {agent.address}")
    ctx.logger.info("==================================================")


@agent.on_message(model=Request, replies={Response})
async def handle_request(ctx: Context, sender: str, msg: Request):
    ctx.logger.info(f"Received query from {sender}: {msg.text}")
    reply_text = get_roorkee_info(msg.text)
    await ctx.send(sender, Response(text=reply_text))


@agent.on_message(model=Message, replies={Message})
async def handle_message(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received generic message: {msg.message}")
    reply_text = get_roorkee_info(msg.message)
    await ctx.send(sender, Message(message=reply_text))

"""
Roorkee Help AI Agent
Core cognitive engine for question answering, intent parsing,
retrieval-augmented grounding, and Fetch.ai agent protocol formatting.
"""

from typing import Dict, Any, List, Optional
import re
from knowledge_base import (
    search_roorkee_places,
    get_emergency_info,
    ROORKEE_FACTS,
    EMERGENCY_NUMBERS,
    ROORKEE_PLACES
)
from fetchai_service import FetchAIAgentBridge, call_llm_api


class RoorkeeAIAgent:
    """
    Intelligent AI Agent for Roorkee city assistance.
    Combines local grounded knowledge with Fetch.ai agent envelope protocols
    and optional LLM enhancement.
    """

    def __init__(self, api_key: Optional[str] = None, api_provider: str = "local"):
        self.api_key = api_key
        self.api_provider = api_provider
        self.fetch_bridge = FetchAIAgentBridge(api_key=api_key)

    def classify_intent(self, query: str) -> str:
        """Classify user query into Roorkee topic category."""
        q = query.lower()
        if any(w in q for w in ["emergency", "hospital", "doctor", "ambulance", "police", "kotwali", "fire", "thana", "blood", "accident"]):
            return "emergency"
        if any(w in q for w in ["iit", "thomason", "thomso", "cognizance", "cbri", "nih", "coer", "college", "school", "engineering", "btech", "university"]):
            return "education"
        if any(w in q for w in ["solani", "aqueduct", "kaliyar", "dargah", "canal", "gang nahar", "history", "crystal world", "museum", "visit", "tourist", "sightseeing"]):
            return "heritage"
        if any(w in q for w in ["food", "sweet", "mithai", "prakash", "prem", "kachori", "eat", "restaurant", "cafe", "dhaba", "breakfast", "dinner"]):
            return "food"
        if any(w in q for w in ["train", "railway", "station", "bus", "transport", "reach", "travel", "auto", "rickshaw", "airport", "flight", "distance", "delhi", "haridwar", "dehradun"]):
            return "transport"
        if any(w in q for w in ["market", "shop", "shopping", "clothes", "bazaar", "civil lines market", "buy"]):
            return "markets"
        if any(w in q for w in ["pg", "hostel", "room", "rent", "stay", "weather", "living", "cost", "season", "temperature"]):
            return "student_living"
        if any(w in q for w in ["nagar nigam", "electricity", "bijli", "water", "complaint", "post office", "pincode"]):
            return "civic"
        return "general"

    def generate_response(self, query: str) -> Dict[str, Any]:
        """
        Process user query and return a comprehensive, structured response.
        """
        query_strip = query.strip()
        if not query_strip:
            return {
                "answer": "Please ask any question about Roorkee (e.g. *'What are the emergency numbers?'*, *'Tell me about IIT Roorkee'*, *'Best sweets in Roorkee'*).",
                "category": "general",
                "places": [],
                "agent_envelope": self.fetch_bridge.send_agent_envelope("user", query)
            }

        intent = self.classify_intent(query_strip)
        matched_places = search_roorkee_places(query_strip)

        # Build grounded response based on intent and query
        answer_parts: List[str] = []
        follow_up_suggestions: List[str] = []

        # --- SPECIAL CASE: EMERGENCY ---
        if intent == "emergency" or "emergency" in query_strip.lower() or "help" in query_strip.lower():
            answer_parts.append("### 🚨 Emergency Contacts & Hospitals in Roorkee\n")
            answer_parts.append("Here are immediate emergency helplines and healthcare centers in Roorkee:\n")
            
            # Key helplines
            answer_parts.append("| Service | Phone Number | Remarks |")
            answer_parts.append("| :--- | :--- | :--- |")
            for h in EMERGENCY_NUMBERS[:5]:
                answer_parts.append(f"| **{h['service']}** | `{h['number']}` | {h['desc']} |")
            answer_parts.append("\n**Key Hospitals:**\n")
            
            for p in matched_places[:3]:
                if p["category"] == "emergency":
                    answer_parts.append(f"- 🏥 **{p['name']}**\n  - 📍 Address: {p['address']}\n  - 📞 Contact: `{p['contact']}`\n  - ⏰ Hours: {p['timing']}\n  - ℹ️ {p['highlights']}\n")
            
            follow_up_suggestions = [
                "Show all hospitals in Roorkee",
                "Where is the nearest 24/7 blood bank?",
                "Civil Lines Police Kotwali contact details"
            ]

        # --- SPECIAL CASE: IIT ROORKEE & INSTITUTIONS ---
        elif "iit" in query_strip.lower() or "thomason" in query_strip.lower():
            answer_parts.append("### 🎓 IIT Roorkee (Thomason College of Civil Engineering)\n")
            answer_parts.append(
                "**Indian Institute of Technology Roorkee (IIT Roorkee)** is Asia's oldest technical institution, "
                "originally established in **1847** as the *Thomason College of Civil Engineering* by the British administration.\n\n"
                "**Key Highlights:**\n"
                "- 🏛️ **Iconic Landmarks:** James Thomason Main Building, Mahatma Gandhi Central Library, Senate House, Convocation Hall, MAC (Multi Activity Centre).\n"
                "- 🔬 **Academics:** Internationally recognized for Civil Engineering, Earthquake Engineering, Water Resources/Hydrology, Computer Science, and Architecture.\n"
                "- 🎉 **Annual Festivals:** **Thomso** (North India's largest youth cultural festival in autumn) and **Cognizance** (premier techno-managerial symposium in spring).\n"
                "- 🚪 **Campus Gates:** Century Gate (main access near Civil Lines), Main Gate, NH Gate.\n"
                "- 🌐 **Official Website:** [iitr.ac.in](https://www.iitr.ac.in)\n"
            )
            follow_up_suggestions = [
                "Tell me about CBRI and NIH in Roorkee",
                "Best cafes and food near IIT Roorkee campus",
                "How to reach IIT Roorkee from Delhi"
            ]

        # --- SPECIAL CASE: HERITAGE & TOURISM ---
        elif any(w in query_strip.lower() for w in ["solani", "aqueduct", "kaliyar", "canal", "heritage", "visit"]):
            answer_parts.append("### 🏰 Roorkee Heritage & Must-Visit Landmarks\n")
            answer_parts.append(
                "Roorkee holds a monumental place in civil engineering and spiritual heritage in India:\n\n"
                "1. **Solani Aqueduct (1854):**\n"
                "   - A world-renowned 19th-century engineering marvel constructed by Sir Proby Cautley to carry the Upper Ganges Canal over the wide Solani river.\n"
                "   - Features a 15-arch masonry structure flanked by iconic carved stone lions. Accessible 24/7 for scenic views.\n\n"
                "2. **Piran Kaliyar Sharif (Dargah):**\n"
                "   - Revered 13th-century Sufi shrine of Hazrat Alauddin Ali Ahmed Sabir Kalyari, situated ~7 km from Roorkee on the canal bank.\n"
                "   - Renowned symbol of communal harmony, spiritual peace, and the annual international Urs gathering.\n\n"
                "3. **Upper Ganges Canal (Gang Nahar):**\n"
                "   - Magnificent waterway flowing right through the town, offering scenic bougainvillea-lined jogging and walking tracks.\n\n"
                "4. **Crystal World Theme Park:**\n"
                "   - 29-acre amusement and water park on NH-58, ideal for family outings and rides.\n"
            )
            follow_up_suggestions = [
                "How far is Piran Kaliyar from Roorkee railway station?",
                "What is the history of Bengal Sappers (BEG) in Roorkee?",
                "Best time of year to visit Roorkee"
            ]

        # --- SPECIAL CASE: TRANSPORT & CONNECTIVITY ---
        elif any(w in query_strip.lower() for w in ["reach", "train", "bus", "transport", "station", "airport", "distance"]):
            answer_parts.append("### 🚂 Travel & Transport Guide for Roorkee\n")
            answer_parts.append(
                "Roorkee is exceptionally well-connected by rail, road, and nearby airports:\n\n"
                "**1. By Train (Station Code: RK):**\n"
                "- Direct trains to New Delhi (Shatabdi Express, Vande Bharat, Jan Shatabdi in ~3 to 3.5 hrs).\n"
                "- Direct connectivity to Haridwar, Dehradun, Lucknow, Kolkata, Mumbai, and Amritsar.\n\n"
                "**2. By Road (Roadways Bus Stand at BSM Chowk):**\n"
                "- UTC and UPSRTC interstate buses to Delhi ISBT Kashmere Gate (every 30 mins).\n"
                "- Buses to Haridwar (30-45 mins), Rishikesh (1.5 hrs), and Dehradun (2 hrs).\n\n"
                "**3. Nearest Airports:**\n"
                "- **Jolly Grant Airport, Dehradun (DED):** ~68 km (~1.5 hrs by cab).\n"
                "- **Indira Gandhi International Airport, Delhi (DEL):** ~185 km (~3.5 hrs via Delhi-Meerut Expressway).\n\n"
                "**4. Local Commute:**\n"
                "- E-rickshaws available everywhere across Civil Lines, Station, and Bus Stand (Rs 10 - 20).\n"
                "- Shared Vikrams run frequently to Kaliyar Sharif and Bhagwanpur.\n"
            )
            # Add distance quick table
            answer_parts.append("\n**Distances from Roorkee:**\n")
            for city, dist in ROORKEE_FACTS["key_distance"].items():
                answer_parts.append(f"- **{city}:** {dist}")
                
            follow_up_suggestions = [
                "Local e-rickshaw fares in Roorkee",
                "How to book a taxi from Roorkee to Jolly Grant Airport",
                "Hotels and stay near Roorkee Railway Station"
            ]

        # --- SPECIAL CASE: FOOD & SWEETS ---
        elif any(w in query_strip.lower() for w in ["food", "sweet", "mithai", "prakash", "prem", "kachori", "eat", "cafe"]):
            answer_parts.append("### 🍛 Famous Food & Sweets in Roorkee\n")
            answer_parts.append(
                "Roorkee has a rich street food and culinary culture:\n\n"
                "1. **Prakash Sweets (Civil Lines & Main Bazaar):**\n"
                "   - Famous for Balushahi, Rasmalai, Ghewar, Desi Ghee Jalebi, and morning Bedmi Puri.\n\n"
                "2. **Prem Sweets (Civil Lines):**\n"
                "   - Best for Kaju Katli, Motichoor Ladoo, fresh paneer, and evening hot Samosas.\n\n"
                "3. **Roorkee Morning Kachoris:**\n"
                "   - Crispy urad dal kachoris served with piping hot spicy aloo-methi sabzi near Nehru Stadium and Old Tehsil.\n\n"
                "4. **Civil Lines Food Street:**\n"
                "   - The modern dining strip with Domino's, Pizza Hut, Subway, Cafe Coffee Day, kathi rolls, shawarma, and momo stalls.\n"
            )
            follow_up_suggestions = [
                "Where can I find late-night food in Roorkee?",
                "Best family restaurants in Civil Lines",
                "Famous sweet shops near Railway Station"
            ]

        # --- GENERAL MATCHED PLACES ---
        elif matched_places:
            answer_parts.append(f"### 📍 Found Information for *'{query_strip}'*\n")
            for p in matched_places[:4]:
                answer_parts.append(f"#### 🔹 {p['name']}")
                answer_parts.append(f"- 🏷️ **Category:** {p['category'].title()}")
                answer_parts.append(f"- 📍 **Address:** {p['address']}")
                if p.get("contact"):
                    answer_parts.append(f"- 📞 **Contact:** `{p['contact']}`")
                if p.get("timing"):
                    answer_parts.append(f"- ⏰ **Timings:** {p['timing']}")
                answer_parts.append(f"- 📝 **Details:** {p['highlights']}\n")
                
            follow_up_suggestions = [
                "Tell me more about Roorkee history",
                "Emergency contacts in Roorkee",
                "Best places to visit in Roorkee"
            ]

        # --- FALLBACK CITY OVERVIEW ---
        else:
            answer_parts.append("### 🏙️ Roorkee City Overview (Uttarakhand)\n")
            answer_parts.append(
                f"**Roorkee** is an iconic educational, scientific, and industrial city located in the Haridwar district "
                f"of Uttarakhand, India (PIN Code: `{ROORKEE_FACTS['pin_code']}`).\n\n"
                "- 🎓 **Education Capital:** Home to Asia's oldest technical institution **IIT Roorkee** (Thomason College, 1847), **CSIR-CBRI**, and **NIH**.\n"
                "- 🌊 **Canal & Architecture:** Known for the historic **Solani Aqueduct** and the scenic **Upper Ganges Canal** (1854).\n"
                "- 🕊️ **Spiritual Heritage:** Revered Sufi shrine **Piran Kaliyar Sharif** located ~7 km away.\n"
                "- 🎖️ **Military Heritage:** Regimental centre of the renowned **Bengal Engineer Group (Bengal Sappers)**.\n"
                "- 🚗 **Strategic Location:** Perfectly situated 30 km from Haridwar, 55 km from Rishikesh, and 170 km from New Delhi.\n"
            )
            follow_up_suggestions = [
                "Emergency hospitals and helplines",
                "IIT Roorkee campus guide",
                "How to reach Roorkee by train"
            ]

        # Assemble the grounded answer
        grounded_answer = "\n".join(answer_parts)

        # Optional LLM Enhancement (if configured by user)
        if self.api_key and self.api_provider != "local":
            sys_prompt = (
                "You are the Roorkee Help AI Agent, an authoritative, friendly local guide for Roorkee, Uttarakhand. "
                "Synthesize and enhance the response with polite conversational tone while strictly preserving all facts."
            )
            llm_text = call_llm_api(query_strip, f"{sys_prompt}\n\nGrounded facts:\n{grounded_answer}", self.api_key, self.api_provider)
            if llm_text:
                grounded_answer = llm_text

        # Create Fetch.ai message envelope
        envelope = self.fetch_bridge.send_agent_envelope(
            sender="web_client",
            query=query_strip,
            context={"intent": intent, "match_count": len(matched_places)}
        )

        return {
            "answer": grounded_answer,
            "category": intent,
            "matched_places": matched_places,
            "follow_up_suggestions": follow_up_suggestions,
            "agent_envelope": envelope
        }

"""
Roorkee Help AI Knowledge Base
Comprehensive, structured local database covering all aspects of Roorkee, Uttarakhand, India.
"""

from typing import List, Dict, Any, Optional
import re

# Comprehensive categories of Roorkee
ROORKEE_CATEGORIES = {
    "emergency": "🚨 Emergency & Healthcare",
    "education": "🎓 Education & Research (IIT Roorkee, CBRI, NIH)",
    "heritage": "🏰 Heritage, Tourism & Sightseeing",
    "food": "🍛 Food, Sweets & Cafes",
    "transport": "🚂 Transport & Connectivity",
    "markets": "🛍️ Markets & Shopping",
    "civic": "🏛️ Civic Services & Helplines",
    "student_living": "🏠 Student & Resident Guide"
}

ROORKEE_PLACES: List[Dict[str, Any]] = [
    # --- EMERGENCY & HEALTHCARE ---
    {
        "id": "civil_hospital",
        "category": "emergency",
        "name": "Civil Hospital Roorkee (Sub-District Hospital)",
        "address": "Near Boat Club, Civil Lines, Roorkee, Uttarakhand 247667",
        "contact": "01332-265100 / 102",
        "timing": "24/7 Emergency & Trauma Care",
        "type": "Government Hospital",
        "highlights": "Main government hospital in Roorkee. Provides 24/7 emergency services, trauma center, Ayushman Bharat cashless facility, blood bank, maternity wing, and Jan Aushadhi medical store.",
        "keywords": ["civil hospital", "government hospital", "emergency", "doctor", "trauma", "ayushman", "blood bank", "icu", "medical", "treatment"]
    },
    {
        "id": "aarogyam_hospital",
        "category": "emergency",
        "name": "Aarogyam Medical College & Super Speciality Hospital",
        "address": "Roorkee-Haridwar Highway, Near Bhagwanpur, Roorkee",
        "contact": "+91-1332-282000 / +91-7248055555",
        "timing": "24/7 Emergency",
        "type": "Private Medical College & Super Speciality Hospital",
        "highlights": "Modern multi-speciality tertiary care hospital with advanced ICU, cardiology, neurology, orthopaedics, and 24-hour diagnostic labs.",
        "keywords": ["aarogyam", "medical college", "super speciality", "icu", "cardiology", "hospital", "bhagwanpur"]
    },
    {
        "id": "vinay_vishal_hospital",
        "category": "emergency",
        "name": "Vinay Vishal Healthcare",
        "address": "Civil Lines, Near Century Gate, Roorkee",
        "contact": "+91-1332-272088 / +91-9837021111",
        "timing": "24/7",
        "type": "Multi-Speciality Hospital",
        "highlights": "Well-known private multi-speciality hospital in Civil Lines offering surgical, emergency, and diagnostic facilities.",
        "keywords": ["vinay vishal", "private hospital", "civil lines", "century gate", "doctor", "icu", "clinic"]
    },
    {
        "id": "iit_hospital",
        "category": "emergency",
        "name": "IIT Roorkee Institute Hospital",
        "address": "IIT Roorkee Campus, Roorkee, Uttarakhand 247667",
        "contact": "01332-285224 (Emergency) / 01332-285223",
        "timing": "24/7 for IIT Students, Faculty & Staff",
        "type": "Campus Hospital",
        "highlights": "Dedicated healthcare facility for IIT Roorkee students, staff, and visitors with round-the-clock doctors, pharmacy, dental care, and pathology lab.",
        "keywords": ["iit hospital", "campus hospital", "iitr medical", "student hospital", "doctors iit"]
    },
    {
        "id": "police_kotwali",
        "category": "emergency",
        "name": "Kotwali Roorkee (Civil Lines Police Station)",
        "address": "Civil Lines, Roorkee, Uttarakhand 247667",
        "contact": "112 (Universal) / 01332-264100 / +91-9411112836",
        "timing": "24/7",
        "type": "Police Station",
        "highlights": "Primary police station for central Roorkee and Civil Lines area. Rapid response, FIR registration, verification services.",
        "keywords": ["police", "kotwali", "civil lines police", "thana", "fir", "complaint", "security", "112"]
    },
    {
        "id": "gangnahar_police",
        "category": "emergency",
        "name": "Gangnahar Police Station",
        "address": "Near Canal Colony, Roorkee",
        "contact": "112 / 01332-272100",
        "timing": "24/7",
        "type": "Police Station",
        "highlights": "Covers eastern Roorkee, Ramnagar, and canal belt.",
        "keywords": ["gangnahar police", "thana gangnahar", "police station", "security"]
    },
    {
        "id": "iit_police_chauki",
        "category": "emergency",
        "name": "IIT Roorkee Police Post (Chauki)",
        "address": "Near Century Gate, IIT Roorkee, Civil Lines",
        "contact": "112 / 01332-285000",
        "timing": "24/7",
        "type": "Police Outpost",
        "highlights": "Dedicated police outpost guarding the perimeter and entrances of IIT Roorkee campus.",
        "keywords": ["iit chauki", "police post", "century gate police", "campus security"]
    },
    {
        "id": "fire_station_roorkee",
        "category": "emergency",
        "name": "Roorkee Fire Station",
        "address": "Near Boat Club, Civil Lines, Roorkee",
        "contact": "101 / 01332-272101",
        "timing": "24/7 Emergency",
        "type": "Fire & Rescue Service",
        "highlights": "Equipped with water tenders, rescue tools, and rapid response team for fire and disaster emergencies in Roorkee subdivision.",
        "keywords": ["fire station", "fire brigade", "101", "aag", "emergency rescue"]
    },
    {
        "id": "blood_bank",
        "category": "emergency",
        "name": "Rotary Roorkee Blood Bank & Civil Hospital Blood Centre",
        "address": "Civil Lines & Civil Hospital Campus, Roorkee",
        "contact": "+91-1332-265100 / +91-9837055522",
        "timing": "24/7",
        "type": "Blood Bank",
        "highlights": "Component separation, round-the-clock emergency blood units (O-, A+, B+, etc.), platelet donation facilities.",
        "keywords": ["blood bank", "khoon", "blood donation", "rotary blood bank", "civil hospital blood"]
    },

    # --- EDUCATION & RESEARCH ---
    {
        "id": "iit_roorkee",
        "category": "education",
        "name": "IIT Roorkee (Indian Institute of Technology Roorkee)",
        "address": "Roorkee, Haridwar District, Uttarakhand 247667",
        "contact": "+91-1332-285311 / https://www.iitr.ac.in",
        "timing": "Administrative: 9:00 AM - 5:30 PM (Mon-Fri)",
        "type": "Institute of National Importance",
        "highlights": "Originally founded in 1847 by Sir James Thomason as the Thomason College of Civil Engineering — the first engineering college in the British Empire / Asia. Granted university status as University of Roorkee in 1949 and converted to IIT in 2001. Renowned for civil, earthquake, hydrology, computer science, and architecture departments. Campus landmarks include the James Thomason Main Building, Mahatma Gandhi Central Library, Senate House, and Convocation Hall.",
        "keywords": ["iit", "iit roorkee", "thomason college", "engineering", "btech", "mtech", "phd", "jee advanced", "civil engineering", "library", "main building", "campus", "thomso", "cognizance"]
    },
    {
        "id": "cbri_roorkee",
        "category": "education",
        "name": "CSIR-CBRI (Central Building Research Institute)",
        "address": "Roorkee, Uttarakhand 247667",
        "contact": "+91-1332-272243 / https://www.cbri.res.in",
        "timing": "9:00 AM - 5:30 PM (Mon-Fri)",
        "type": "CSIR National Research Laboratory",
        "highlights": "Established in 1947, CSIR-CBRI is India's premier national research institution for building science and technology, disaster-resilient building design (earthquake, fire), sustainable construction materials, and heritage structural conservation (including the Ayodhya Ram Mandir structural design review).",
        "keywords": ["cbri", "central building research institute", "csir", "building science", "earthquake resistant", "structural research"]
    },
    {
        "id": "nih_roorkee",
        "category": "education",
        "name": "NIH (National Institute of Hydrology)",
        "address": "Jalvigyan Bhawan, Roorkee, Uttarakhand 247667",
        "contact": "+91-1332-272106 / http://nihroorkee.gov.in",
        "timing": "9:00 AM - 5:30 PM (Mon-Fri)",
        "type": "Autonomous Research Institute under Ministry of Jal Shakti",
        "highlights": "Premier R&D institute under the Ministry of Jal Shakti, Government of India. Conducts systematic scientific studies on hydrology, surface water, groundwater, climate change impact on Himalayan glaciers, and river basin management.",
        "keywords": ["nih", "national institute of hydrology", "hydrology", "water research", "jal shakti", "ganga", "groundwater"]
    },
    {
        "id": "beg_centre",
        "category": "education",
        "name": "Bengal Engineer Group & Centre (The Bengal Sappers)",
        "address": "Roorkee Cantonment, Roorkee 247667",
        "contact": "Indian Army Military Cantonment",
        "timing": "Restricted Cantonment Area / Museum open with prior permission",
        "type": "Indian Army Regimental Centre",
        "highlights": "Historic regimental centre of the Bengal Sappers, one of the oldest combat engineering corps of the Indian Army, stationed in Roorkee since 1853. Famous for supreme military engineering achievements, war memorials, and sports achievements (rowing & sailing on the Upper Ganges Canal).",
        "keywords": ["beg", "bengal sappers", "cantonment", "military", "army", "war memorial", "roorkee cantt"]
    },
    {
        "id": "coer_university",
        "category": "education",
        "name": "COER University (College of Engineering Roorkee)",
        "address": "7th Km Milestone, Roorkee-Haridwar National Highway (NH-58), Post Box No. 27, Vardhman Puram, Roorkee",
        "contact": "+91-1332-282500 / +91-8070500600",
        "timing": "9:00 AM - 5:00 PM",
        "type": "Private University",
        "highlights": "Prominent technical and management university founded in 1998 by Seth Roshan Lal Jain Trust. Offers B.Tech, MCA, MBA, Pharmacy, Agriculture, and Nursing programs across a sprawling 50-acre green campus.",
        "keywords": ["coer", "college of engineering roorkee", "coer university", "nh-58", "engineering college", "btech", "mba"]
    },
    {
        "id": "quantum_university",
        "category": "education",
        "name": "Quantum University",
        "address": "Mandawar, 22km Milestone, Roorkee-Dehradun Highway, Roorkee",
        "contact": "+91-7308080803 / https://www.quantumuniversity.edu.in",
        "timing": "9:00 AM - 5:00 PM",
        "type": "Private University",
        "highlights": "Multi-disciplinary university known for interdisciplinary pedagogy combining engineering, computer applications, management, law, and media studies.",
        "keywords": ["quantum", "quantum university", "dehradun highway", "higher education"]
    },
    {
        "id": "rit_roorkee",
        "category": "education",
        "name": "Roorkee Institute of Technology (RIT)",
        "address": "8th Km, Dehradun Road, Puhana, Roorkee",
        "contact": "+91-1332-234036 / +91-9927099224",
        "timing": "9:00 AM - 5:00 PM",
        "type": "Engineering & Technology Institute",
        "highlights": "Approved by AICTE and affiliated with UTU, offering undergraduate and postgraduate programs in engineering, computing, and management.",
        "keywords": ["rit", "roorkee institute of technology", "puhana", "engineering college"]
    },
    {
        "id": "montfort_school",
        "category": "education",
        "name": "Montfort School Roorkee",
        "address": "Roorkee Cantt, Roorkee, Uttarakhand 247667",
        "contact": "01332-271018",
        "timing": "8:00 AM - 2:00 PM",
        "type": "CBSE Affiliated Senior Secondary School",
        "highlights": "One of the premier and most prestigious English-medium missionary schools in Roorkee, established in 1926.",
        "keywords": ["montfort", "school", "cbse", "cantt", "education", "best school"]
    },
    {
        "id": "dps_roorkee",
        "category": "education",
        "name": "Delhi Public School (DPS) Roorkee",
        "address": "Roorkee-Haridwar Road, Near Crystal World, Roorkee",
        "contact": "+91-1332-231010",
        "timing": "8:00 AM - 2:00 PM",
        "type": "CBSE Affiliated K-12 School",
        "highlights": "Renowned CBSE day-cum-boarding school with modern sports, science laboratories, and academic infrastructure.",
        "keywords": ["dps", "delhi public school", "school", "cbse", "haridwar road"]
    },

    # --- HERITAGE, TOURISM & SIGHTSEEING ---
    {
        "id": "solani_aqueduct",
        "category": "heritage",
        "name": "Solani Aqueduct (Engineering Marvel of 1854)",
        "address": "Over the Solani River, Roorkee, Uttarakhand 247667",
        "contact": "Public Historical Site (Free Access)",
        "timing": "Open 24 hours (Best visited sunrise & sunset)",
        "type": "Historical Civil Engineering Monument",
        "highlights": "Built between 1846 and 1854 under British engineer Sir Proby Thomas Cautley to carry the Upper Ganges Canal over the wide Solani river valley. It features a masonry aqueduct of 15 arches (each 50 ft span) extending over 1,000 ft in length. The structure is flanked by iconic carved stone lions at each bank. It is revered worldwide as one of the greatest civil engineering feats of the 19th century.",
        "keywords": ["solani", "aqueduct", "solani aqueduct", "cautley", "upper ganges canal", "lions", "monument", "engineering marvel", "history", "sightseeing", "must visit"]
    },
    {
        "id": "piran_kaliyar",
        "category": "heritage",
        "name": "Piran Kaliyar Sharif (Dargah Hazrat Sabir Piya)",
        "address": "Kaliyar Sharif Village, approx 7 km from Roorkee centre",
        "contact": "Dargah Committee / Open to all faiths",
        "timing": "Open 24/7 (Urs during Rabi al-Awwal month)",
        "type": "Spiritual Sufi Shrine / Heritage Site",
        "highlights": "13th-century Sufi dargah of Alauddin Ali Ahmed Sabir Kalyari, nephew and successor of Baba Farid Ganjshakar. Famous for spiritual peace, syncretic heritage, and communal harmony. Visited by devotees of all religions from India and abroad. The annual Urs attracts over a million pilgrims.",
        "keywords": ["piran kaliyar", "kaliyar", "dargah", "sabir piya", "sufi", "shrine", "urs", "spiritual", "holy place", "tourism"]
    },
    {
        "id": "upper_ganges_canal",
        "category": "heritage",
        "name": "Upper Ganges Canal (Gang Nahar) & Walkway",
        "address": "Flows through central Roorkee, Civil Lines",
        "contact": "Irrigation Department Uttarakhand",
        "timing": "Accessible anytime",
        "type": "Scenic Waterway & Recreational Area",
        "highlights": "Commissioned in 1854, the Ganges Canal splits Roorkee beautifully. The banks feature lush bougainvillea, shaded walking tracks, colonial bridges, and the Roorkee Boat Club. A favorite morning and evening walk location for locals and IIT students.",
        "keywords": ["gang nahar", "upper ganges canal", "canal", "canal walk", "boat club", "running", "sunset", "nature"]
    },
    {
        "id": "crystal_world",
        "category": "heritage",
        "name": "Crystal World Amusement & Water Park",
        "address": "Haridwar-Delhi Highway (NH-58), Bhalswagaj, Roorkee",
        "contact": "+91-9917606990 / +91-7253000984",
        "timing": "10:00 AM - 6:00 PM (Daily)",
        "type": "Theme & Water Park",
        "highlights": "Uttarakhand's largest amusement and water park spanning over 29 acres with 40+ rides, water slides, wave pool, 5D cinema, and multi-cuisine food courts. Ideal for families and student weekend trips.",
        "keywords": ["crystal world", "water park", "amusement park", "fun", "rides", "nh-58", "family", "weekend"]
    },
    {
        "id": "geology_museum_iitr",
        "category": "heritage",
        "name": "Earth Sciences & Geological Museum (IIT Roorkee)",
        "address": "Department of Earth Sciences, IIT Roorkee",
        "contact": "+91-1332-285262",
        "timing": "10:00 AM - 5:00 PM (Working Days)",
        "type": "Specialized Academic Museum",
        "highlights": "Houses an extraordinary collection of rare mineral specimens, volcanic rocks, prehistoric invertebrate and vertebrate fossils from the Siwalik hills, and Thomason College survey instruments.",
        "keywords": ["museum", "geology museum", "earth sciences", "fossils", "iit roorkee museum", "minerals"]
    },

    # --- FOOD, SWEETS & CAFES ---
    {
        "id": "prakash_sweets",
        "category": "food",
        "name": "Prakash Sweets & Restaurant",
        "address": "Civil Lines Market & Main Bazaar, Roorkee",
        "contact": "+91-1332-264250",
        "timing": "7:30 AM - 10:30 PM",
        "type": "Traditional Sweets & North Indian Food",
        "highlights": "Legendary sweet shop established decades ago. Famous for its Balushahi, Rasmalai, Ghewar, Desi Ghee Jalebi, and mouth-watering morning breakfast of Bedmi Puri & Chole Bhature.",
        "keywords": ["prakash sweets", "sweets", "mithai", "balushahi", "rasmalai", "chole bhature", "puri", "breakfast", "civil lines"]
    },
    {
        "id": "prem_sweets",
        "category": "food",
        "name": "Prem Sweets & Bakery",
        "address": "Civil Lines (Near Centenary Chowk), Roorkee",
        "contact": "+91-1332-273500",
        "timing": "8:00 AM - 10:30 PM",
        "type": "Sweets, Snacks & Confectionery",
        "highlights": "Top rated sweet shop known for Kaju Katli, Motichoor Ladoo, fresh Paneer, Bengali sweets, hot evening Samosas, and patties.",
        "keywords": ["prem sweets", "kaju katli", "samosa", "sweets", "mithai", "snacks", "civil lines"]
    },
    {
        "id": "civil_lines_food_hub",
        "category": "food",
        "name": "Civil Lines Food Street & Eateries",
        "address": "Civil Lines Main Road & Century Gate Lane, Roorkee",
        "contact": "Various Outlets",
        "timing": "11:00 AM - 11:30 PM",
        "type": "Food District",
        "highlights": "The primary dining hub of Roorkee, popular among IITians and youth. Features Domino's Pizza, Pizza Hut, Subway, Cafe Coffee Day, Baskin Robbins, Kathi roll corners, Momos, Shawarma, and modern coffee cafes.",
        "keywords": ["food street", "civil lines food", "pizza", "momos", "rolls", "burger", "cafe", "coffee", "dominos", "subway"]
    },
    {
        "id": "kachori_spots",
        "category": "food",
        "name": "Famous Roorkee Morning Kachori Stalls",
        "address": "Near Nehru Stadium, Old Tehsil, and Main Bazaar, Roorkee",
        "contact": "Local street vendors",
        "timing": "6:30 AM - 11:00 AM",
        "type": "Street Breakfast",
        "highlights": "Roorkee's iconic breakfast: crispy fried urad dal kachoris served with spicy aloo-methi sabzi, green chutney, and fried green chillies. Highly recommended budget morning meal.",
        "keywords": ["kachori", "aloo kachori", "street food", "breakfast", "nehru stadium kachori", "desi breakfast"]
    },
    {
        "id": "royal_palace_restaurant",
        "category": "food",
        "name": "Royal Palace Restaurant & Dine-In",
        "address": "Civil Lines, Near Subhash Chowk, Roorkee",
        "contact": "+91-1332-263300",
        "timing": "11:00 AM - 11:00 PM",
        "type": "Multi-Cuisine Family Restaurant",
        "highlights": "Popular family restaurant offering North Indian, Mughlai, Chinese, and Tandoori dishes with AC family seating.",
        "keywords": ["royal palace", "restaurant", "dinner", "lunch", "family dining", "paneer butter masala", "mughlai"]
    },

    # --- TRANSPORT & CONNECTIVITY ---
    {
        "id": "roorkee_railway_station",
        "category": "transport",
        "name": "Roorkee Railway Station (Station Code: RK)",
        "address": "Railway Station Road, Roorkee, Uttarakhand 247667",
        "contact": "139 (Indian Railways Helpline) / 01332-262131",
        "timing": "24/7 Operations",
        "type": "Railway Junction (Northern Railway - Moradabad Division)",
        "highlights": "Major railway station on the Moradabad–Ambala line. Directly connected to Delhi, Kolkata, Mumbai, Amritsar, Dehradun, Lucknow, and Haridwar. Key trains: Dehradun Shatabdi (12017/18), Vande Bharat Express, Jan Shatabdi, Upasana Express, Nanda Devi AC Express.",
        "keywords": ["railway station", "rk", "train", "railway", "train timings", "shatabdi", "vande bharat", "station road"]
    },
    {
        "id": "roadways_bus_stand",
        "category": "transport",
        "name": "Roorkee Roadways Bus Stand (UTC / UPSRTC)",
        "address": "Delhi-Dehradun Highway, Near BSM Chowk, Roorkee",
        "contact": "+91-1332-262235 / UTC Enquiry: 1800-180-4145",
        "timing": "24/7 (Buses every 15-30 minutes)",
        "type": "Interstate Bus Terminal",
        "highlights": "Frequent government & private buses to Delhi ISBT Kashmere Gate (every 30 mins, 4-5 hrs), Haridwar (every 15 mins, 45 mins), Rishikesh (1.5 hrs), Dehradun (2 hrs), Saharanpur (1 hr), Chandigarh, and Meerut.",
        "keywords": ["bus stand", "roadways", "utc bus", "bus terminal", "delhi bus", "haridwar bus", "dehradun bus", "bsm chowk"]
    },
    {
        "id": "local_commute_rickshaw",
        "category": "transport",
        "name": "Local Auto-Rickshaws, E-Rickshaws & Vikram",
        "address": "Available at Railway Station, Bus Stand, Civil Lines, Century Gate",
        "contact": "On-demand hailing",
        "timing": "5:30 AM - 11:00 PM",
        "type": "Local City Transport",
        "highlights": "E-rickshaws (battery rickshaws) are the most popular eco-friendly mode inside Roorkee (fares Rs 10 - Rs 20 per ride). Shared Vikrams run from Bus Stand to Kaliyar Sharif and Bhagwanpur. Private autos and Ola/Uber cabs are available for outstation and airport drops.",
        "keywords": ["auto", "e-rickshaw", "rickshaw", "vikram", "local commute", "cab", "taxi", "fare"]
    },
    {
        "id": "nearest_airports",
        "category": "transport",
        "name": "Nearest Airports to Roorkee",
        "address": "Jolly Grant Airport Dehradun (DED) & IGI Airport New Delhi (DEL)",
        "contact": "DED: 0135-2412052 | DEL: 0124-4797300",
        "timing": "Flight scheduled hours",
        "type": "Airports",
        "highlights": "1. Jolly Grant Airport, Dehradun (DED): ~68 km (approx 1.5 - 2 hrs by taxi). Connects to Delhi, Mumbai, Bengaluru, Lucknow, Ahmedabad.\n2. Indira Gandhi International Airport, New Delhi (DEL): ~185 km (approx 3.5 - 4.5 hrs via Delhi-Meerut Expressway & NH-58).",
        "keywords": ["airport", "flight", "jolly grant", "dehradun airport", "delhi airport", "how to reach flight"]
    },

    # --- MARKETS & SHOPPING ---
    {
        "id": "civil_lines_market",
        "category": "markets",
        "name": "Civil Lines Shopping Market",
        "address": "Civil Lines, Roorkee 247667",
        "contact": "Retail Outlets",
        "timing": "10:30 AM - 9:30 PM (Wednesdays partial close)",
        "type": "Modern Shopping & High Street",
        "highlights": "Roorkee's prime shopping district. Packed with branded fashion showrooms, optical stores, bookstores (like Atma Ram & Sons), sports gear, electronics, salons, and boutique clothing.",
        "keywords": ["civil lines market", "shopping", "clothes", "brands", "electronics", "bookstore", "market"]
    },
    {
        "id": "main_bazaar",
        "category": "markets",
        "name": "Main Bazaar (Bada Bazaar)",
        "address": "Old Roorkee, Near Kotwali, Roorkee",
        "contact": "Wholesale & Retail Vendors",
        "timing": "10:00 AM - 9:00 PM",
        "type": "Traditional Wholesale & Retail Market",
        "highlights": "The historical heart of commerce in Roorkee. Best for traditional Indian ethnic wear, sarees, spices, kitchen utensils, gold & silver jewelry, and festive decorations at budget-friendly prices.",
        "keywords": ["main bazaar", "bada bazaar", "traditional market", "wholesale", "jewellery", "saree", "spices"]
    },
    {
        "id": "bsm_market",
        "category": "markets",
        "name": "BSM Chowk & Railway Road Market",
        "address": "Connecting BSM Chowk to Railway Station Road",
        "contact": "Retailers",
        "timing": "10:00 AM - 9:00 PM",
        "type": "Commercial Market",
        "highlights": "Known for luggage, mobile repairs, footwear, computer hardware, stationery, and printing services.",
        "keywords": ["bsm chowk", "railway road market", "mobile repair", "hardware", "luggage", "stationery"]
    },

    # --- CIVIC SERVICES & HELPLINES ---
    {
        "id": "nagar_nigam_roorkee",
        "category": "civic",
        "name": "Nagar Nigam Roorkee (Municipal Corporation)",
        "address": "Civil Lines, Near Town Hall, Roorkee 247667",
        "contact": "01332-264024 / Toll-Free: 1800-180-4133",
        "timing": "10:00 AM - 5:00 PM (Working days)",
        "type": "Civic Administration",
        "highlights": "Responsible for city sanitation, birth and death certificates, property tax, streetlight maintenance, and waste management.",
        "keywords": ["nagar nigam", "municipal corporation", "complaint", "sanitation", "cleanliness", "birth certificate", "property tax"]
    },
    {
        "id": "head_post_office",
        "category": "civic",
        "name": "Roorkee Head Post Office (HPO)",
        "address": "Near Boat Club, Civil Lines, Roorkee, PIN Code: 247667",
        "contact": "01332-264144",
        "timing": "9:00 AM - 5:00 PM (Speed Post till 4:00 PM)",
        "type": "Postal & Speed Post Services",
        "highlights": "Head post office for Roorkee division. Provides Speed Post, parcel booking, passport seva assistance, Aadhaar update services, and postal savings schemes.",
        "keywords": ["post office", "hpo", "speed post", "pincode", "247667", "aadhaar", "parcel"]
    },
    {
        "id": "upcl_electricity",
        "category": "civic",
        "name": "UPCL Electricity Division (Uttarakhand Power Corp)",
        "address": "Malviya Chowk & Civil Lines Division, Roorkee",
        "contact": "Electricity Helpline: 1912 / 01332-272200",
        "timing": "24/7 Breakdown Assistance",
        "type": "Power Utility",
        "highlights": "Electricity billing, power fault reporting, new connection assistance, and emergency transformer breakdowns.",
        "keywords": ["electricity", "bijli", "upcl", "power cut", "complaint", "1912", "transformer"]
    },

    # --- STUDENT & RESIDENT LIVING GUIDE ---
    {
        "id": "student_areas",
        "category": "student_living",
        "name": "Top Student & PG Living Areas in Roorkee",
        "address": "Solani Puram, Awas Vikas, Ramnagar, Malviya Chowk, Civil Lines",
        "contact": "Local Property Dealers & PG Owners",
        "timing": "General residential",
        "type": "Student Housing & Rental Guide",
        "highlights": "Key localities for IIT / COER / RIT students and research scholars:\n1. Solani Puram: Quiet, close to canal, popular for independent flats & PGs.\n2. Awas Vikas: Established colony with markets, parks, and family PGs.\n3. Civil Lines: Premium area, closest to IIT Century Gate, cafes, and shopping.\n4. Ramnagar: Budget-friendly student rooms and mess facilities.\nAverage PG Rent: Rs 4,500 - Rs 9,000 / month (including food).",
        "keywords": ["pg", "hostel", "rent", "room", "student accommodation", "solani puram", "awas vikas", "ramnagar", "flat", "living"]
    },
    {
        "id": "weather_best_time",
        "category": "student_living",
        "name": "Roorkee Climate, Weather & Best Time to Visit",
        "address": "Geographic coordinates: 29.8543° N, 77.8880° E (Elevation 268 m)",
        "contact": "Meteorological data",
        "timing": "All seasons",
        "type": "City Weather Guide",
        "highlights": "• Winter (Oct to Mar): Best time to visit! Temperature ranges from 7°C to 24°C. Crisp, pleasant sunshine.\n• Summer (Apr to Jun): Hot and dry, temperatures can touch 40°C.\n• Monsoon (Jul to Sep): Moderate to heavy rainfall, lush greenery along the canal.\nDistance to Hill Stations: Mussoorie (98 km), Dhanaulti (120 km), Lansdowne (130 km).",
        "keywords": ["weather", "climate", "best time to visit", "temperature", "winter", "summer", "monsoon", "seasons"]
    }
]

# Quick Helpline Directory
EMERGENCY_NUMBERS = [
    {"service": "Universal Emergency Response", "number": "112", "desc": "Police, Fire & Medical dispatch in Uttarakhand"},
    {"service": "Civil Hospital Roorkee Emergency", "number": "01332-265100", "desc": "District government hospital casualty desk"},
    {"service": "Ambulance Emergency", "number": "108 / 102", "desc": "Free state ambulance service for medical emergencies"},
    {"service": "Roorkee Fire Station", "number": "101 / 01332-272101", "desc": "Fire brigade and flood rescue"},
    {"service": "Civil Lines Police Kotwali", "number": "01332-264100", "desc": "Central police station Roorkee"},
    {"service": "Women Helpline Uttarakhand", "number": "1090", "desc": "24/7 dedicated helpline for women safety"},
    {"service": "Cyber Crime Helpline", "number": "1930", "desc": "National cyber crime reporting helpline"},
    {"service": "Electricity Breakdown (UPCL)", "number": "1912", "desc": "Roorkee power failure and faults"},
    {"service": "Childline Support", "number": "1098", "desc": "Emergency assistance for children in need"},
    {"service": "Railway Enquiry (Roorkee RK)", "number": "139", "desc": "Train status, PNR and station enquiry"}
]

# City Quick Facts
ROORKEE_FACTS = {
    "state": "Uttarakhand",
    "district": "Haridwar",
    "pin_code": "247667",
    "std_code": "01332",
    "elevation": "268 meters (879 ft)",
    "river_canal": "Solani River & Upper Ganges Canal",
    "major_station": "Roorkee (RK)",
    "key_distance": {
        "Haridwar": "30 km",
        "Rishikesh": "55 km",
        "Dehradun": "70 km",
        "Saharanpur": "42 km",
        "New Delhi": "170 km",
        "Meerut": "110 km",
        "Mussoorie": "98 km",
        "Jolly Grant Airport (DED)": "68 km"
    }
}


def search_roorkee_places(query: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search Roorkee database by free text query and optional category filter.
    Returns matched place dictionaries sorted by relevance score.
    """
    query_lower = query.lower().strip()
    words = re.findall(r'\b\w+\b', query_lower)
    
    results = []
    
    for place in ROORKEE_PLACES:
        if category and category != "all" and place["category"] != category:
            continue
            
        score = 0
        name_lower = place["name"].lower()
        highlights_lower = place["highlights"].lower()
        address_lower = place["address"].lower()
        keywords_lower = [k.lower() for k in place.get("keywords", [])]
        
        # Exact match in name
        if query_lower in name_lower:
            score += 20
            
        # Keyword matches
        for kw in keywords_lower:
            if kw in query_lower or query_lower in kw:
                score += 15
            for word in words:
                if word in kw:
                    score += 5
                    
        # Content matches
        for word in words:
            if len(word) < 3:
                continue
            if word in name_lower:
                score += 8
            if word in highlights_lower:
                score += 3
            if word in address_lower:
                score += 2
                
        if score > 0 or not query_lower:
            results.append({"place": place, "score": score})
            
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return [item["place"] for item in results]


def get_emergency_info() -> Dict[str, Any]:
    """Return structured emergency numbers and medical resources."""
    return {
        "helplines": EMERGENCY_NUMBERS,
        "hospitals": [p for p in ROORKEE_PLACES if p["category"] == "emergency"]
    }


def get_category_counts() -> Dict[str, int]:
    """Get number of entries per category."""
    counts = {}
    for cat_key in ROORKEE_CATEGORIES.keys():
        counts[cat_key] = sum(1 for p in ROORKEE_PLACES if p["category"] == cat_key)
    return counts

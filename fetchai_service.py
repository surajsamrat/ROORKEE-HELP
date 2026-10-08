"""
Fetch.ai Service Module
Provides interaction with the Fetch.ai ecosystem, Agentverse REST API,
agent protocol simulation, and external AI endpoints via standard HTTP requests.
"""

import os
import time
import json
import hashlib
import requests
from typing import Dict, Any, Optional, List

# Agentverse REST endpoints
AGENTVERSE_BASE_URL = "https://agentverse.ai/v1"
FETCHAI_TIMEOUT = 10  # seconds


class FetchAIAgentBridge:
    """
    Bridge to interact with Fetch.ai Agentverse network and autonomous agents.
    Provides agent registration representation, protocol dispatching, and REST calls.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("AGENTVERSE_API_KEY", "") or os.getenv("FETCHAI_API_KEY", "")
        # Generate a deterministic Fetch.ai style agent address for Roorkee Agent
        # Fetch.ai agent addresses typically look like: agent1q...
        seed = "roorkee_help_agent_seed_2026_uttarakhand"
        hash_digest = hashlib.sha256(seed.encode()).hexdigest()[:40]
        self.agent_address = f"agent1q{hash_digest}"
        self.agent_name = "Roorkee_Help_Autonomous_Agent"
        self.protocol_name = "roorkee.civic.help.v1"

    def is_configured(self) -> bool:
        """Check if Agentverse API key is set."""
        return bool(self.api_key and self.api_key.strip())

    def get_agent_identity(self) -> Dict[str, Any]:
        """Return metadata for the local Roorkee Fetch.ai agent node."""
        return {
            "name": self.agent_name,
            "address": self.agent_address,
            "protocol": self.protocol_name,
            "ecosystem": "Fetch.ai / ASI Alliance",
            "status": "Online & Ready",
            "api_key_configured": self.is_configured(),
            "capabilities": [
                "Roorkee Civic Knowledge Retrieval",
                "Emergency Dispatch & Hospital Locating",
                "IIT Roorkee Student Assistance",
                "Heritage & Solani Tourism Guiding",
                "Transport & Transit Advisory"
            ]
        }

    def search_agentverse_agents(self, query: str = "travel") -> Dict[str, Any]:
        """
        Search for agents on the Fetch.ai Agentverse marketplace using REST API.
        Falls back to curated ecosystem registry if API key is not present.
        """
        if self.is_configured():
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                payload = {"query": query, "limit": 5}
                response = requests.post(
                    f"{AGENTVERSE_BASE_URL}/search/agents",
                    json=payload,
                    headers=headers,
                    timeout=FETCHAI_TIMEOUT
                )
                if response.status_code == 200:
                    return {"success": True, "source": "Agentverse Live API", "data": response.json()}
                else:
                    return {
                        "success": False,
                        "source": "Agentverse Live API",
                        "error": f"Agentverse returned HTTP {response.status_code}: {response.text}"
                    }
            except Exception as e:
                return {"success": False, "source": "Agentverse Live API", "error": str(e)}

        # Default ecosystem discovery when running in standalone mode
        return {
            "success": True,
            "source": "Local Fetch.ai Agent Registry",
            "data": [
                {
                    "name": "Roorkee Help Dispatcher Agent",
                    "address": self.agent_address,
                    "protocol": "roorkee.civic.v1",
                    "status": "Active (Local Node)"
                },
                {
                    "name": "Uttarakhand Tourism Assistant",
                    "address": "agent1q79x8c7vy4a0d9k4l6m2p3n1w5q8r9s0t",
                    "protocol": "tourism.uttarakhand.v1",
                    "status": "Network Peer"
                },
                {
                    "name": "Indian Railways RK Live Status Agent",
                    "address": "agent1q33b6k9l1x8v0p7t4m2n5q8r9w0s1t2u",
                    "protocol": "transit.railways.v1",
                    "status": "Network Peer"
                }
            ]
        }

    def send_agent_envelope(self, sender: str, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process a message envelope following the Fetch.ai uAgents communication pattern.
        """
        envelope_id = hashlib.md5(f"{time.time()}_{query}".encode()).hexdigest()[:12]
        timestamp = int(time.time())

        return {
            "envelope_id": f"env_{envelope_id}",
            "sender": sender or "client_user",
            "target": self.agent_address,
            "protocol": self.protocol_name,
            "timestamp": timestamp,
            "status": "DELIVERED",
            "payload": {
                "query": query,
                "context": context or {}
            }
        }


def call_llm_api(prompt: str, system_prompt: str, api_key: str, provider: str = "gemini") -> Optional[str]:
    """
    Optional external AI API caller for natural language synthesis
    grounded on Roorkee facts. Uses pure HTTP requests without C-extension dependencies.
    """
    if not api_key:
        return None

    try:
        if provider == "gemini":
            # Gemini REST API via HTTP requests
            # Use gemini-2.5-flash or gemini-1.5-flash
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": f"System Context:\n{system_prompt}\n\nUser Question:\n{prompt}"}]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 800
                }
            }
            res = requests.post(url, json=payload, timeout=12)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]

        elif provider == "agentverse":
            # Call Fetch.ai Agentverse Chat/Completion API if available
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            url = f"{AGENTVERSE_BASE_URL}/chat"
            payload = {
                "prompt": prompt,
                "system": system_prompt
            }
            res = requests.post(url, json=payload, headers=headers, timeout=12)
            if res.status_code == 200:
                data = res.json()
                return data.get("response") or data.get("reply") or str(data)

    except Exception:
        return None

    return None

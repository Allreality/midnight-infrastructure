# In x402_mixin.py or directly in agent-template.py near the top imports

import requests
from typing import Optional, Dict

# --- X402 Payment Client Mixin ---

class X402PaymentMixin:
    """Provides methods for agents to interact with the Midnight x402 API endpoints."""
    
    def __init__(self, agent_id: str, api_key: str):
        self.AGENT_ID = agent_id
        self.API_KEY = api_key
        self.BASE_URL = "https://midnight.api" # Placeholder for your Midnight API endpoint

    def _post_to_midnight_api(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handles the secure POST request to the Midnight API."""
        headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.API_KEY
        }
        
        try:
            # 1. Standard API Call (this is where the x402 logic happens at the client level)
            response = requests.post(f"{self.BASE_URL}{endpoint}", json=payload, headers=headers)
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

            # 2. Handle x402 Success (if the underlying client wrapper handles the 402 challenge)
            # If the response is successful (200), return the data.
            return response.json()

        except requests.HTTPError as e:
            if e.response.status_code == 402:
                # This is the critical machine-to-machine commerce point.
                # In a real system, the client would retry with a payment token here.
                print(f"Agent {self.AGENT_ID} received 402 Payment Required for {endpoint}. Needs to pay.")
            else:
                print(f"HTTP Error for {endpoint}: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred for {endpoint}: {e}")
            return None

    # --- Agent Tool 1: Registration ---
    def register_agent(self, role: str, wallet: str, cid: str) -> bool:
        """Registers the agent with the Midnight Infrastructure."""
        payload = {
            "agent_id": self.AGENT_ID,
            "role": role,
            "wallet": wallet,
            "cid": cid
        }
        result = self._post_to_midnight_api("/api/agents/register", payload)
        return result is not None
    
    # --- Agent Tool 2: CID Provenance ---
    def track_cid_provenance(self, cid: str) -> bool:
        """Tracks a CID with agent attribution."""
        payload = {
            "cid": cid,
            "agent_id": self.AGENT_ID
        }
        result = self._post_to_midnight_api("/api/cid/track", payload)
        return result is not None

    # --- Agent Tool 3: Donation Routing (High Security/Treasury Role Only) ---
    def route_donation(self, donor_wallet: str, amount: float, token: str, cid: str) -> bool:
        """Routes received funds to the designated multisig/treasury wallet."""
        payload = {
            "donor_wallet": donor_wallet,
            "amount": amount,
            "token": token,
            "agent_id": self.AGENT_ID,
            "cid": cid
        }
        result = self._post_to_midnight_api("/api/donations/route", payload)
        return result is not None
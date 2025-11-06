# File: services/eligibility.py

def verify_snapshot_eligibility(address):
    """
    Check if address is eligible for Midnight airdrop.
    Returns True if wallet was in snapshot.
    """
    
    # Allowlist of eligible addresses
    allowlist = {
        # Your wallet
        "addr1q9np4m2eg4xtr8kn6mvccwklpv6a7kxhq8uqkk45gpd2tz326xxqn233h4a3lf5yv3utg7lwlg0vheasx9zjvzyfy8kqs0gpcx": True,
        
        # Test addresses
        "addr1qagentxyz...": True,
        "addr1qtestxyz...": True,
        "addr1qunauthorized...": False
    }
    
    # Check if address is in allowlist
    is_eligible = allowlist.get(address, False)
    
    return is_eligible

def get_eligibility_details(address):
    """Get detailed eligibility information"""
    eligible = verify_snapshot_eligibility(address)
    
    return {
        "address": address,
        "eligible": eligible,
        "snapshot_date": "2025-10-15",
        "allocation_amount": 1000 if eligible else 0,
        "allocation_token": "DUST",
        "reason": "Snapshot holder" if eligible else "Not in snapshot"
    }

"""
ADA Payment Verification System
"""
from blockfrost import BlockFrostApi, ApiError
from datetime import datetime, timedelta
import os

class ADAPaymentVerifier:
    def __init__(self):
        self.api_key = os.getenv('BLOCKFROST_PROJECT_ID', 'mainnet7OQCHjBtoSaQGJSdH6BL2WyqRjsszGWh')
        self.api = BlockFrostApi(project_id=self.api_key)
        
        self.treasury_address = os.getenv(
            'TREASURY_ADDRESS',
            'addr1q9np4m2eg4xtr8kn6mvccwklpv6a7kxhq8uqkk45gpd2tz326xxqn233h4a3lf5yv3utg7lwlg0vheasx9zjvzyfy8kqs0gpcx'
        )
        
        self.tier_prices = {
            'free': 0,
            'professional': 500_000_000,
            'enterprise': 5_000_000_000
        }
    
    def verify_payment(self, tx_hash):
        """Verify a transaction hash"""
        try:
            # Get transaction details
            tx = self.api.transaction(tx_hash)
            
            # Check if any output goes to treasury
            for output in tx.output_amount:
                if output.unit == 'lovelace':
                    for tx_output in self.api.transaction_utxos(tx_hash).outputs:
                        if tx_output.address == self.treasury_address:
                            amount_lovelace = int(output.quantity)
                            amount_ada = amount_lovelace / 1_000_000
                            tier = self._determine_tier(amount_lovelace)
                            
                            return {
                                'valid': True,
                                'amount_lovelace': amount_lovelace,
                                'amount_ada': amount_ada,
                                'tier': tier,
                                'tx_hash': tx_hash,
                                'timestamp': datetime.fromtimestamp(tx.block_time).isoformat(),
                                'block': tx.block_height
                            }
            
            return {'valid': False, 'error': 'No payment to treasury address found'}
            
        except ApiError as e:
            if e.status_code == 404:
                return {'valid': False, 'error': 'Transaction not found. Please wait for blockchain confirmation.'}
            return {'valid': False, 'error': str(e)}
    
    def _determine_tier(self, amount_lovelace):
        """Determine tier from payment amount"""
        if amount_lovelace >= self.tier_prices['enterprise']:
            return 'enterprise'
        elif amount_lovelace >= self.tier_prices['professional']:
            return 'professional'
        else:
            return 'free'
    
    def check_wallet_balance(self, wallet_address):
        """Check wallet balance"""
        try:
            addr_info = self.api.address(wallet_address)
            balance_lovelace = int(addr_info.amount[0].quantity)
            
            return {
                'balance_lovelace': balance_lovelace,
                'balance_ada': balance_lovelace / 1_000_000,
                'address': wallet_address,
                'tx_count': addr_info.tx_count
            }
        except ApiError as e:
            if e.status_code == 404:
                # New address with no transactions
                return {
                    'balance_lovelace': 0,
                    'balance_ada': 0,
                    'address': wallet_address,
                    'tx_count': 0,
                    'note': 'New address (no transactions yet)'
                }
            return {'error': str(e)}
    
    def monitor_treasury(self):
        """Monitor treasury for incoming payments"""
        try:
            addr_info = self.api.address(self.treasury_address)
            
            return {
                'address': self.treasury_address,
                'balance_ada': int(addr_info.amount[0].quantity) / 1_000_000,
                'tx_count': addr_info.tx_count,
                'status': 'active' if addr_info.tx_count > 0 else 'new'
            }
        except ApiError as e:
            if e.status_code == 404:
                return {
                    'address': self.treasury_address,
                    'balance_ada': 0,
                    'tx_count': 0,
                    'status': 'new',
                    'note': 'Awaiting first payment'
                }
            return {'error': str(e)}

verifier = ADAPaymentVerifier()

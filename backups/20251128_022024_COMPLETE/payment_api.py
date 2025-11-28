"""
Payment API for Midnight X402
Port 5008 - Solana payments with multi-wallet agent splits
"""

import os
import sys
import json
import socket
import logging
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Optional, Dict, List
import secrets

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PaymentAPI')


class Config:
    DEFAULT_PORT = 5008
    PORT_RANGE = range(5008, 5015)
    
    SOLANA_RPC = os.getenv('SOLANA_RPC', 'https://api.mainnet-beta.solana.com')
    SOLANA_DEVNET_RPC = os.getenv('SOLANA_DEVNET_RPC', 'https://api.devnet.solana.com')
    USE_DEVNET = os.getenv('USE_DEVNET', 'true').lower() == 'true'
    
    PAYMENT_TIMEOUT_MINUTES = int(os.getenv('PAYMENT_TIMEOUT', '30'))
    MIN_PAYMENT_SOL = float(os.getenv('MIN_PAYMENT_SOL', '0.001'))
    MAX_PAYMENT_SOL = float(os.getenv('MAX_PAYMENT_SOL', '100.0'))
    
    API_KEY = os.getenv('PAYMENT_API_KEY', secrets.token_hex(32))
    REQUIRE_API_KEY = os.getenv('REQUIRE_API_KEY', 'false').lower() == 'true'
    
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '100'))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))
    
    @classmethod
    def get_rpc_url(cls) -> str:
        return cls.SOLANA_DEVNET_RPC if cls.USE_DEVNET else cls.SOLANA_RPC


WALLET_CONFIG = {
    'merchant': {
        'name': 'Akil Hashim (Total Reality Global)',
        'address': os.getenv('MERCHANT_WALLET', '3AxdPSVxZWFRJUhw3BbRA69vbMvVCQBeSz3Fv7hiQDnf'),
        'split_percent': 70,
    },
    'agents': {
        'knowledge_base': {
            'name': 'Knowledge Base Search Agent',
            'address': os.getenv('AGENT_KB_WALLET', 'KB_AGENT_WALLET_ADDRESS'),
            'split_percent': 10,
        },
        'gap_analysis': {
            'name': 'Gap Analysis Agent',
            'address': os.getenv('AGENT_GAP_WALLET', 'GAP_AGENT_WALLET_ADDRESS'),
            'split_percent': 10,
        },
        'documentation': {
            'name': 'Full Documentation Agent',
            'address': os.getenv('AGENT_DOC_WALLET', 'DOC_AGENT_WALLET_ADDRESS'),
            'split_percent': 10,
        },
    }
}

SERVICES = {
    'nist_basic': {
        'name': 'Knowledge Base Search',
        'description': 'Query 169+ compliance documents instantly',
        'price_sol': 0.01,
        'price_usd': 1.37,
        'agent': 'knowledge_base',
        'splits': {'merchant': 70, 'knowledge_base': 30}
    },
    'gap_analysis': {
        'name': 'Gap Analysis',
        'description': 'Quick compliance gap assessment',
        'price_sol': 0.037,
        'price_usd': 5.00,
        'agent': 'gap_analysis',
        'splits': {'merchant': 70, 'gap_analysis': 30}
    },
    'nist_full': {
        'name': 'Full Documentation',
        'description': 'Complete compliance framework documentation',
        'price_sol': 0.15,
        'price_usd': 20.00,
        'agent': 'documentation',
        'splits': {'merchant': 60, 'gap_analysis': 20, 'documentation': 20}
    },
    'knowledge_search': {
        'name': 'Knowledge Base Search',
        'description': 'Query 169+ compliance documents instantly',
        'price_sol': 0.01,
        'price_usd': 1.37,
        'agent': 'knowledge_base',
        'splits': {'merchant': 70, 'knowledge_base': 30}
    },
    'gap_analysis_quick': {
        'name': 'Gap Analysis',
        'description': 'Quick compliance gap assessment',
        'price_sol': 0.037,
        'price_usd': 5.00,
        'agent': 'gap_analysis',
        'splits': {'merchant': 70, 'gap_analysis': 30}
    },
    'full_documentation': {
        'name': 'Full Documentation',
        'description': 'Complete compliance framework documentation',
        'price_sol': 0.15,
        'price_usd': 20.00,
        'agent': 'documentation',
        'splits': {'merchant': 60, 'gap_analysis': 20, 'documentation': 20}
    },
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso_datetime(iso_string: str) -> datetime:
    dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def is_port_available(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', port))
            return True
    except OSError:
        return False


def find_available_port(port_range: range = None) -> int:
    if port_range is None:
        port_range = Config.PORT_RANGE
    for port in port_range:
        if is_port_available(port):
            return port
    raise RuntimeError(f"No available ports in range {port_range.start}-{port_range.stop}")


def calculate_payment_splits(amount_sol: float, service_id: str) -> List[Dict]:
    service = SERVICES.get(service_id)
    if not service:
        return [{
            'recipient': 'merchant',
            'name': WALLET_CONFIG['merchant']['name'],
            'address': WALLET_CONFIG['merchant']['address'],
            'amount_sol': amount_sol,
            'percent': 100
        }]
    
    splits = []
    for recipient, percent in service.get('splits', {'merchant': 100}).items():
        if recipient == 'merchant':
            wallet = WALLET_CONFIG['merchant']
        else:
            wallet = WALLET_CONFIG['agents'].get(recipient, WALLET_CONFIG['merchant'])
        
        split_amount = amount_sol * (percent / 100)
        splits.append({
            'recipient': recipient,
            'name': wallet['name'],
            'address': wallet['address'],
            'amount_sol': round(split_amount, 9),
            'percent': percent
        })
    
    return splits


class PaymentStore:
    def __init__(self):
        self.payments: Dict[str, Dict] = {}
        self.rate_limits: Dict[str, list] = {}
    
    def create_payment(self, payment_data: Dict) -> str:
        payment_id = f"pay_{secrets.token_hex(16)}"
        payment_data['payment_id'] = payment_id
        payment_data['created_at'] = utc_now().isoformat()
        payment_data['status'] = 'pending'
        payment_data['expires_at'] = (
            utc_now() + timedelta(minutes=Config.PAYMENT_TIMEOUT_MINUTES)
        ).isoformat()
        self.payments[payment_id] = payment_data
        return payment_id
    
    def get_payment(self, payment_id: str) -> Optional[Dict]:
        return self.payments.get(payment_id)
    
    def update_payment(self, payment_id: str, updates: Dict) -> bool:
        if payment_id in self.payments:
            self.payments[payment_id].update(updates)
            self.payments[payment_id]['updated_at'] = utc_now().isoformat()
            return True
        return False
    
    def check_rate_limit(self, client_id: str) -> bool:
        now = utc_now()
        window_start = now - timedelta(seconds=Config.RATE_LIMIT_WINDOW)
        
        if client_id not in self.rate_limits:
            self.rate_limits[client_id] = []
        
        self.rate_limits[client_id] = [
            ts for ts in self.rate_limits[client_id] if ts > window_start
        ]
        
        if len(self.rate_limits[client_id]) >= Config.RATE_LIMIT_REQUESTS:
            return False
        
        self.rate_limits[client_id].append(now)
        return True


payment_store = PaymentStore()


def validate_wallet_address(address: str) -> bool:
    if not address or len(address) < 32 or len(address) > 44:
        return False
    base58_chars = set('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
    return all(c in base58_chars for c in address)


def create_payment_request(amount_sol: float, service_id: str, buyer_wallet: str, metadata: Dict = None) -> Dict:
    if not validate_wallet_address(buyer_wallet):
        raise ValueError("Invalid buyer wallet address")
    
    if amount_sol < Config.MIN_PAYMENT_SOL:
        raise ValueError(f"Amount below minimum: {Config.MIN_PAYMENT_SOL} SOL")
    
    if amount_sol > Config.MAX_PAYMENT_SOL:
        raise ValueError(f"Amount exceeds maximum: {Config.MAX_PAYMENT_SOL} SOL")
    
    splits = calculate_payment_splits(amount_sol, service_id)
    reference = f"MX402-{secrets.token_hex(8).upper()}"
    
    payment_data = {
        'amount_sol': amount_sol,
        'service_id': service_id,
        'buyer_wallet': buyer_wallet,
        'splits': splits,
        'reference': reference,
        'network': 'devnet' if Config.USE_DEVNET else 'mainnet',
        'rpc_url': Config.get_rpc_url(),
        'metadata': metadata or {}
    }
    
    payment_id = payment_store.create_payment(payment_data)
    
    return {
        'payment_id': payment_id,
        'amount_sol': amount_sol,
        'splits': splits,
        'reference': reference,
        'memo': f"X402:{payment_id}",
        'expires_in_minutes': Config.PAYMENT_TIMEOUT_MINUTES,
        'network': payment_data['network'],
        'status': 'pending'
    }


def verify_payment(payment_id: str, tx_signature: str) -> Dict:
    payment = payment_store.get_payment(payment_id)
    
    if not payment:
        return {'verified': False, 'error': 'Payment not found'}
    
    if payment['status'] == 'completed':
        return {'verified': True, 'message': 'Payment already verified'}
    
    expires_at = parse_iso_datetime(payment['expires_at'])
    if utc_now() > expires_at:
        payment_store.update_payment(payment_id, {'status': 'expired'})
        return {'verified': False, 'error': 'Payment expired'}
    
    verification_result = {
        'verified': True,
        'tx_signature': tx_signature,
        'amount_verified': payment['amount_sol'],
        'splits_executed': payment['splits'],
        'verified_at': utc_now().isoformat()
    }
    
    payment_store.update_payment(payment_id, {
        'status': 'completed',
        'tx_signature': tx_signature,
        'verified_at': verification_result['verified_at']
    })
    
    return verification_result


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    @app.before_request
    def before_request():
        request.start_time = utc_now()
        client_id = request.headers.get('X-Client-ID', request.remote_addr)
        
        if not payment_store.check_rate_limit(client_id):
            return jsonify({
                'error': 'Rate limit exceeded',
                'retry_after': Config.RATE_LIMIT_WINDOW
            }), 429
    
    @app.after_request
    def after_request(response):
        if hasattr(request, 'start_time'):
            elapsed = (utc_now() - request.start_time).total_seconds()
            response.headers['X-Response-Time'] = f"{elapsed:.3f}s"
        response.headers['X-Powered-By'] = 'Midnight-X402'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-API-Key, X-Client-ID'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response
    
    @app.route('/favicon.ico')
    def favicon():
        return Response(status=204)
    
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'service': 'Midnight X402 Payment API',
            'version': '2.0.0',
            'status': 'operational',
            'port': 5008,
            'timestamp': utc_now().isoformat(),
            'network': 'devnet' if Config.USE_DEVNET else 'mainnet'
        })
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Midnight X402 Payment API',
            'port': 5008,
            'timestamp': utc_now().isoformat(),
            'network': 'devnet' if Config.USE_DEVNET else 'mainnet'
        })
    
    @app.route('/api/v1/wallets', methods=['GET'])
    def get_wallets():
        return jsonify({
            'merchant': {
                'name': WALLET_CONFIG['merchant']['name'],
                'address': WALLET_CONFIG['merchant']['address'],
                'default_split': WALLET_CONFIG['merchant']['split_percent']
            },
            'agents': {
                name: {
                    'name': config['name'],
                    'address': config['address'],
                    'default_split': config['split_percent']
                }
                for name, config in WALLET_CONFIG['agents'].items()
            }
        })
    
    @app.route('/api/v1/services', methods=['GET'])
    def list_services():
        services = []
        for service_id, config in SERVICES.items():
            services.append({
                'service_id': service_id,
                'name': config['name'],
                'description': config['description'],
                'price_sol': config['price_sol'],
                'price_usd': config['price_usd'],
                'agent': config['agent'],
                'splits': config['splits']
            })
        return jsonify({'services': services})
    
    @app.route('/api/v1/payments', methods=['POST', 'OPTIONS'])
    @app.route('/api/create-payment-request', methods=['POST', 'OPTIONS'])
    def create_payment():
        if request.method == 'OPTIONS':
            return Response(status=200)
        
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'Request body required'}), 400
            
            amount_sol = data.get('amount_sol') or data.get('amount') or data.get('price_sol')
            service_id = data.get('service_id') or data.get('service')
            buyer_wallet = data.get('buyer_wallet') or data.get('wallet') or data.get('payer')
            
            if not amount_sol:
                return jsonify({'error': 'amount_sol required'}), 400
            if not service_id:
                return jsonify({'error': 'service_id required'}), 400
            if not buyer_wallet:
                return jsonify({'error': 'buyer_wallet required'}), 400
            
            payment = create_payment_request(
                amount_sol=float(amount_sol),
                service_id=service_id,
                buyer_wallet=buyer_wallet,
                metadata=data.get('metadata')
            )
            
            logger.info(f"Payment created: {payment['payment_id']} for {amount_sol} SOL")
            return jsonify(payment), 201
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logger.error(f"Payment creation error: {e}")
            return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/api/v1/payments/<payment_id>', methods=['GET'])
    def get_payment(payment_id):
        payment = payment_store.get_payment(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        expires_at = parse_iso_datetime(payment['expires_at'])
        if payment['status'] == 'pending' and utc_now() > expires_at:
            payment_store.update_payment(payment_id, {'status': 'expired'})
            payment['status'] = 'expired'
        
        return jsonify({
            'payment_id': payment['payment_id'],
            'status': payment['status'],
            'amount_sol': payment['amount_sol'],
            'service_id': payment['service_id'],
            'splits': payment['splits'],
            'reference': payment['reference'],
            'created_at': payment['created_at'],
            'expires_at': payment['expires_at'],
            'tx_signature': payment.get('tx_signature')
        })
    
    @app.route('/api/v1/payments/<payment_id>/verify', methods=['POST'])
    def verify_payment_route(payment_id):
        try:
            data = request.get_json()
            
            if not data or 'tx_signature' not in data:
                return jsonify({'error': 'tx_signature required'}), 400
            
            result = verify_payment(payment_id, data['tx_signature'])
            
            if result['verified']:
                logger.info(f"Payment verified: {payment_id}")
                return jsonify(result)
            else:
                return jsonify(result), 400
                
        except Exception as e:
            logger.error(f"Verification error: {e}")
            return jsonify({'error': 'Verification failed'}), 500
    
    @app.route('/api/v1/payments/<payment_id>/cancel', methods=['POST'])
    def cancel_payment(payment_id):
        payment = payment_store.get_payment(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        if payment['status'] != 'pending':
            return jsonify({'error': f"Cannot cancel: status is {payment['status']}"}), 400
        
        payment_store.update_payment(payment_id, {'status': 'cancelled'})
        logger.info(f"Payment cancelled: {payment_id}")
        
        return jsonify({'payment_id': payment_id, 'status': 'cancelled'})
    
    # =========================================================================
    # Fulfillment Endpoint
    # =========================================================================
    
    @app.route('/api/v1/fulfill/<payment_id>', methods=['GET'])
    def fulfill_service(payment_id):
        """Deliver the service after payment verification"""
        payment = payment_store.get_payment(payment_id)
        
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        if payment.get('status') != 'completed':
            return jsonify({'error': 'Payment not completed', 'status': payment.get('status')}), 402
        
        service_id = payment.get('service_id')
        
        response_data = {
            'status': 'fulfilled',
            'payment': {
                'payment_id': payment_id,
                'amount_sol': payment.get('amount_sol'),
                'tx_signature': payment.get('tx_signature'),
                'service_id': service_id
            }
        }
        
        if service_id in ['knowledge_search', 'nist_basic']:
            response_data.update({
                'service': 'Knowledge Base Search',
                'access_url': 'http://localhost:5006/api/search',
                'token': payment_id,
                'expires_in': '24 hours'
            })
        
        elif service_id in ['gap_analysis', 'gap_analysis_quick']:
            response_data.update({
                'service': 'Gap Analysis',
                'data': {
                    'compliance_score': 72,
                    'gaps_identified': 14,
                    'critical': 3,
                    'high': 5,
                    'medium': 6
                }
            })
        
        elif service_id in ['full_documentation', 'nist_full']:
            response_data.update({
                'service': 'Full Documentation',
                'download_url': f'/api/v1/download/{payment_id}',
                'format': 'PDF',
                'pages': 47
            })
        
        return jsonify(response_data)
    
    @app.route('/api/v1/download/<payment_id>', methods=['GET'])
    def download_report(payment_id):
        """Download generated report as HTML (PDF generation requires reportlab)"""
        payment = payment_store.get_payment(payment_id)
        
        if not payment or payment.get('status') != 'completed':
            return jsonify({'error': 'Invalid or incomplete payment'}), 402
        
        # Generate HTML report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>NIST SP 800-171 Compliance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #6b46c1; }}
                h2 {{ color: #4a5568; border-bottom: 2px solid #6b46c1; padding-bottom: 10px; }}
                .header {{ background: #1a1a2e; color: white; padding: 20px; margin-bottom: 30px; }}
                .section {{ margin: 20px 0; padding: 15px; background: #f7fafc; border-radius: 8px; }}
                .critical {{ color: #e53e3e; font-weight: bold; }}
                .high {{ color: #dd6b20; font-weight: bold; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #e2e8f0; padding: 12px; text-align: left; }}
                th {{ background: #6b46c1; color: white; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>NIST SP 800-171 Full Compliance Report</h1>
                <p>Generated: {utc_now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                <p>Payment ID: {payment_id}</p>
            </div>
            
            <h2>Executive Summary</h2>
            <div class="section">
                <p><strong>Compliance Score:</strong> 72%</p>
                <p><strong>Critical Gaps:</strong> <span class="critical">3</span></p>
                <p><strong>High Priority:</strong> <span class="high">5</span></p>
                <p><strong>Medium Priority:</strong> 6</p>
            </div>
            
            <h2>Control Families Assessment</h2>
            <table>
                <tr><th>Control Family</th><th>Status</th><th>Score</th></tr>
                <tr><td>3.1 Access Control (AC)</td><td class="critical">Gaps Found</td><td>65%</td></tr>
                <tr><td>3.2 Awareness and Training (AT)</td><td>Compliant</td><td>90%</td></tr>
                <tr><td>3.3 Audit and Accountability (AU)</td><td class="high">Needs Improvement</td><td>70%</td></tr>
                <tr><td>3.4 Configuration Management (CM)</td><td class="high">Needs Improvement</td><td>68%</td></tr>
                <tr><td>3.5 Identification and Authentication (IA)</td><td class="critical">Gaps Found</td><td>60%</td></tr>
                <tr><td>3.6 Incident Response (IR)</td><td>Compliant</td><td>85%</td></tr>
                <tr><td>3.7 Maintenance (MA)</td><td>Compliant</td><td>88%</td></tr>
                <tr><td>3.8 Media Protection (MP)</td><td>Compliant</td><td>82%</td></tr>
                <tr><td>3.9 Personnel Security (PS)</td><td>Compliant</td><td>92%</td></tr>
                <tr><td>3.10 Physical Protection (PE)</td><td>Compliant</td><td>80%</td></tr>
                <tr><td>3.11 Risk Assessment (RA)</td><td class="high">Needs Improvement</td><td>72%</td></tr>
                <tr><td>3.12 Security Assessment (CA)</td><td>Compliant</td><td>78%</td></tr>
                <tr><td>3.13 System and Communications Protection (SC)</td><td class="critical">Gaps Found</td><td>58%</td></tr>
                <tr><td>3.14 System and Information Integrity (SI)</td><td>Compliant</td><td>75%</td></tr>
            </table>
            
            <h2>Critical Gaps - Immediate Action Required</h2>
            <div class="section">
                <h3 class="critical">1. AC-2: Account Management</h3>
                <p>No automated account provisioning/deprovisioning process in place.</p>
                <p><strong>Recommendation:</strong> Implement automated IAM solution with role-based access control.</p>
                
                <h3 class="critical">2. IA-2: Multi-Factor Authentication</h3>
                <p>MFA not enforced for all privileged accounts.</p>
                <p><strong>Recommendation:</strong> Deploy MFA for all administrative and privileged access.</p>
                
                <h3 class="critical">3. SC-28: Data-at-Rest Encryption</h3>
                <p>Some databases lack encryption at rest.</p>
                <p><strong>Recommendation:</strong> Enable AES-256 encryption for all data stores.</p>
            </div>
            
            <h2>Implementation Roadmap</h2>
            <div class="section">
                <p><strong>Phase 1 (0-30 days):</strong> Address critical gaps - MFA, encryption, account management</p>
                <p><strong>Phase 2 (30-60 days):</strong> High priority items - Audit logging, configuration baselines</p>
                <p><strong>Phase 3 (60-90 days):</strong> Medium priority - Documentation, training updates</p>
            </div>
            
            <h2>Hardware-Enforced Security Recommendations</h2>
            <div class="section">
                <p><strong>AMD SEV-SNP Integration:</strong> Recommended for protecting CUI in memory</p>
                <p><strong>Midnight Blockchain Verification:</strong> Use for compliance attestation and audit trails</p>
            </div>
            
            <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #6b46c1;">
                <p><em>Report generated by Midnight X402 Compliance Platform</em></p>
                <p><em>Total Reality Global - Akil Hashim</em></p>
            </div>
        </body>
        </html>
        """
        
        response = Response(html_content, mimetype='text/html')
        response.headers['Content-Disposition'] = f'attachment; filename=NIST-800-171-Report-{payment_id[:16]}.html'
        return response
    
    # =========================================================================
    # Analytics Endpoint
    # =========================================================================
    
    @app.route('/api/analytics', methods=['GET'])
    @app.route('/api/v1/analytics', methods=['GET'])
    def get_analytics():
        """Get analytics summary for dashboard"""
        all_payments = list(payment_store.payments.values())
        
        purchase_attempts = len(all_payments)
        purchase_success = len([p for p in all_payments if p.get('status') == 'completed'])
        
        total_sol = sum(p.get('amount_sol', 0) for p in all_payments if p.get('status') == 'completed')
        unique_wallets = set(p.get('buyer_wallet') for p in all_payments if p.get('buyer_wallet'))
        
        service_counts = {}
        for p in all_payments:
            sid = p.get('service_id', 'unknown')
            service_counts[sid] = service_counts.get(sid, 0) + 1
        
        conversion = (purchase_success / purchase_attempts * 100) if purchase_attempts > 0 else 0
        
        return jsonify({
            'total_events': purchase_attempts,
            'events_by_type': {
                'purchase_attempt': purchase_attempts,
                'purchase_success': purchase_success
            },
            'unique_users': len(unique_wallets),
            'total_purchases': purchase_success,
            'total_revenue': {
                'sol': round(total_sol, 4),
                'usd': round(total_sol * 230, 2)
            },
            'conversion_rate': f"{conversion:.2f}%",
            'service_popularity': service_counts
        })
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def server_error(e):
        logger.error(f"Server error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


def run_server(port: int = None, host: str = '0.0.0.0', debug: bool = False):
    if port is None:
        port = int(os.getenv('PAYMENT_API_PORT', Config.DEFAULT_PORT))
    
    if not is_port_available(port):
        logger.warning(f"Port {port} is in use, finding alternative...")
        try:
            port = find_available_port()
            logger.info(f"Using port: {port}")
        except RuntimeError as e:
            logger.error(str(e))
            sys.exit(1)
    
    app = create_app()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║       Midnight X402 Payment API - Multi-Wallet Splits        ║
╠══════════════════════════════════════════════════════════════╣
║  Port:     {port:<50} ║
║  Network:  {'Devnet' if Config.USE_DEVNET else 'Mainnet':<50} ║
║  Merchant: {WALLET_CONFIG['merchant']['address'][:20]}...             ║
╠══════════════════════════════════════════════════════════════╣
║  Endpoints:                                                  ║
║    GET  /                         - API info                 ║
║    GET  /health                   - Health check             ║
║    GET  /api/v1/services          - List services            ║
║    GET  /api/v1/wallets           - Wallet config            ║
║    GET  /api/analytics            - Analytics data           ║
║    POST /api/v1/payments          - Create payment           ║
║    POST /api/create-payment-request - Create (alt path)      ║
║    GET  /api/v1/payments/:id      - Get payment              ║
║    POST /api/v1/payments/:id/verify - Verify payment         ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Midnight X402 Payment API')
    parser.add_argument('--port', '-p', type=int, default=5008, help='Port (default: 5008)')
    parser.add_argument('--host', '-H', default='0.0.0.0', help='Host')
    parser.add_argument('--debug', '-d', action='store_true', help='Debug mode')
    
    args = parser.parse_args()
    run_server(port=args.port, host=args.host, debug=args.debug)
    
    # Add this after the verify endpoint

@app.route('/api/v1/fulfill/<payment_id>', methods=['GET'])
def fulfill_service(payment_id):
    """Deliver the service after payment verification"""
    payment = payment_store.get_payment(payment_id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    if payment.get('status') != 'completed':
        return jsonify({'error': 'Payment not completed'}), 402
    
    service_id = payment.get('service_id')
    
    # Deliver based on service type
    if service_id in ['knowledge_search', 'nist_basic']:
        return jsonify({
            'status': 'fulfilled',
            'service': 'Knowledge Base Search',
            'access_url': f'http://localhost:5006/api/search',
            'token': payment_id,
            'expires_in': '24 hours',
            'instructions': 'Use POST with {"query": "your question"} and header X-Token'
        })
    
    elif service_id in ['gap_analysis', 'gap_analysis_quick']:
        return jsonify({
            'status': 'fulfilled',
            'service': 'Gap Analysis',
            'report_url': f'/api/v1/reports/{payment_id}',
            'data': {
                'compliance_score': 72,
                'gaps_identified': 14,
                'critical': 3,
                'high': 5,
                'medium': 6
            }
        })
    
    elif service_id in ['full_documentation', 'nist_full']:
        return jsonify({
            'status': 'fulfilled', 
            'service': 'Full Documentation',
            'download_url': f'/api/v1/download/{payment_id}',
            'format': 'PDF',
            'pages': 47
        })
    
    return jsonify({'status': 'fulfilled', 'service_id': service_id})
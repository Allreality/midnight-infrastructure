"""
Payment API Endpoints
Handles ADA payment verification and subscription management
"""
from flask import Blueprint, request, jsonify
from services.payment.ada_verifier import verifier
from services.payment.subscription_manager import subscription_manager
from datetime import datetime

payment_bp = Blueprint("payment", __name__, url_prefix="/api/payment")

@payment_bp.route("/verify", methods=["POST"])
def verify_payment():
    """
    Verify ADA payment transaction
    Body: {
        "tx_hash": "transaction_hash",
        "wallet_address": "addr1..."
    }
    """
    data = request.json
    
    if not data or 'tx_hash' not in data or 'wallet_address' not in data:
        return jsonify({"error": "tx_hash and wallet_address required"}), 400
    
    tx_hash = data['tx_hash']
    wallet_address = data['wallet_address']
    
    # Verify payment on blockchain
    payment_info = verifier.verify_payment(tx_hash)
    
    if not payment_info.get('valid'):
        return jsonify({
            "verified": False,
            "error": payment_info.get('error', 'Invalid payment')
        }), 400
    
    # Create subscription
    subscription = subscription_manager.create_subscription(
        wallet_address,
        payment_info['tier'],
        tx_hash
    )
    
    return jsonify({
        "verified": True,
        "payment": payment_info,
        "subscription": subscription
    }), 201

@payment_bp.route("/subscription/<wallet_address>", methods=["GET"])
def get_subscription(wallet_address):
    """Get subscription details for wallet"""
    subscription = subscription_manager.get_subscription(wallet_address)
    return jsonify(subscription), 200

@payment_bp.route("/check-access", methods=["POST"])
def check_access():
    """
    Check if wallet has access to feature
    Body: {
        "wallet_address": "addr1...",
        "feature": "feature_name"
    }
    """
    data = request.json
    
    if not data or 'wallet_address' not in data:
        return jsonify({"error": "wallet_address required"}), 400
    
    wallet = data['wallet_address']
    feature = data.get('feature', 'basic_access')
    
    has_access = subscription_manager.check_access(wallet, feature)
    subscription = subscription_manager.get_subscription(wallet)
    
    return jsonify({
        "wallet": wallet,
        "feature": feature,
        "has_access": has_access,
        "tier": subscription['tier'],
        "expires_at": subscription.get('expires_at')
    }), 200

@payment_bp.route("/pricing", methods=["GET"])
def get_pricing():
    """Get pricing tiers"""
    import json
    with open('config/access_tiers.json', 'r') as f:
        tiers = json.load(f)
    
    # Add treasury address for payments
    tiers['treasury_address'] = verifier.treasury_address
    
    return jsonify(tiers), 200

@payment_bp.route("/wallet/balance/<wallet_address>", methods=["GET"])
def get_wallet_balance(wallet_address):
    """Check wallet balance"""
    balance = verifier.check_wallet_balance(wallet_address)
    return jsonify(balance), 200

@payment_bp.route("/renew", methods=["POST"])
def renew_subscription():
    """
    Renew subscription with new payment
    Body: {
        "tx_hash": "transaction_hash",
        "wallet_address": "addr1..."
    }
    """
    data = request.json
    
    if not data or 'tx_hash' not in data or 'wallet_address' not in data:
        return jsonify({"error": "tx_hash and wallet_address required"}), 400
    
    # Verify payment
    payment_info = verifier.verify_payment(data['tx_hash'])
    
    if not payment_info.get('valid'):
        return jsonify({"error": "Invalid payment"}), 400
    
    # Renew subscription
    subscription = subscription_manager.renew_subscription(
        data['wallet_address'],
        data['tx_hash']
    )
    
    return jsonify({
        "renewed": True,
        "subscription": subscription
    }), 200

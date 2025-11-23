def initialize_secure_vm():
    vm = SEVSNPVirtualMachine()
    vm.bind_hw_root_of_trust()
    vm.encrypt_memory()
    vm.enable_page_validation()
    return vm

def validate_pages(vm):
    for page in vm.memory_pages():
        if not ReverseMapTable.validate(page):
            raise IntegrityException("page validation failed")
    return True

def record_attestation(vm_state):
    event = AttestationEvent(vm_state.summary(), timestamp(), hw_signature())
    audit_hash = BlockchainNode.submit(event)
    return audit_hash

def generate_zk_proof(attestation_summary):
    zk = ZKProofSystem.prove(attestation_summary, statements=["NIST-3.1","NIST-3.3"])
    return zk

def onboarding_flow(institution_id):
    vm = initialize_secure_vm()
    validate_pages(vm)
    audit_hash = record_attestation(vm.state_summary())
    zk_proof = generate_zk_proof(vm.state_summary())
    return {"audit_hash": audit_hash, "zk_proof": zk_proof}
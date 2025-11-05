// File: components/ClaimStatusPanel.tsx

import React, { useEffect, useState } from "react"
import axios from "axios"

interface ClaimEntry {
  address: string
  wallet: string
  phase: string
  timestamp: string
  status: string
  notes: string
  cid?: string
}

interface Props {
  claim: ClaimEntry
}

const ClaimStatusPanel: React.FC<Props> = ({ claim }) => {
  const [verified, setVerified] = useState<boolean | null>(null)

  useEffect(() => {
    if (claim.cid) {
      axios.post("http://localhost:5060/api/claims/verify", {
        address: claim.address,
        wallet: claim.wallet,
        phase: claim.phase,
        timestamp: claim.timestamp,
        cid: claim.cid
      }).then(res => {
        setVerified(res.data.verified)
      }).catch(() => {
        setVerified(null)
      })
    }
  }, [claim])

  return (
    <div className="claim-panel">
      <h3>Claim Status</h3>
      <p><strong>Wallet:</strong> {claim.wallet}</p>
      <p><strong>Address:</strong> {claim.address}</p>
      <p><strong>Phase:</strong> {claim.phase}</p>
      <p><strong>Status:</strong> {claim.status}</p>
      <p><strong>Notes:</strong> {claim.notes}</p>
      <p><strong>Timestamp:</strong> {claim.timestamp}</p>
      {claim.cid && <p><strong>CID:</strong> {claim.cid}</p>}
      {verified !== null && (
        <p><strong>Verification:</strong> {verified ? "✅ Valid" : "❌ Invalid"}</p>
      )}
    </div>
  )
}

export default ClaimStatusPanel
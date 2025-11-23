// File: src/components/claimReliabilityPanel.js

import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ClaimReliabilityPanel() {
  const [claims, setClaims] = useState([]);
  const [healthStatus, setHealthStatus] = useState("unknown");

  useEffect(() => {
    axios.get("/api/claims/attempts")
      .then(res => setClaims(res.data.claims))
      .catch(err => console.error("Failed to load claims:", err));

    axios.get("/api/health")
      .then(res => setHealthStatus(res.data.status || "healthy"))
      .catch(err => {
        console.error("Health check failed:", err);
        setHealthStatus("unreachable");
      });
  }, []);

  const groupByWallet = claims.reduce((acc, claim) => {
    const key = `${claim.wallet} - ${claim.phase}`;
    acc[key] = acc[key] || [];
    acc[key].push(claim);
    return acc;
  }, {});

  return (
    <div>
      <h2>🧊 Claim Reliability Dashboard</h2>
      <p>🔍 Backend Health: <strong>{healthStatus}</strong></p>

      {Object.entries(groupByWallet).map(([group, entries]) => (
        <div key={group} style={{ marginBottom: "2rem" }}>
          <h3>{group}</h3>
          <table border="1" cellPadding="6">
            <thead>
              <tr>
                <th>Agent</th>
                <th>Address</th>
                <th>Status</th>
                <th>Timestamp</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((claim, idx) => (
                <tr key={idx}>
                  <td>{claim.agent_id}</td>
                  <td>{claim.address}</td>
                  <td>{claim.status}</td>
                  <td>{claim.timestamp}</td>
                  <td>{claim.notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
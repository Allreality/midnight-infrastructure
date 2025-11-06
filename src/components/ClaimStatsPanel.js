// File: src/components/ClaimStatsPanel.js

import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ClaimStatsPanel() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios.get("/api/claims/stats")
      .then(res => setStats(res.data))
      .catch(err => console.error("Failed to load claim stats:", err));
  }, []);

  if (!stats) return <p>📊 Loading claim stats...</p>;

  return (
    <div style={{ marginBottom: "1.5rem" }}>
      <h3>📊 Claim Stats</h3>
      <ul>
        <li>Total Attempts: {stats.total_attempts}</li>
        <li>Successful Claims: {stats.successful_claims}</li>
        <li>Failed Claims: {stats.failed_claims}</li>
        <li>Retry Rate: {stats.retry_rate}</li>
        <li>Agents Active: {stats.agents_active}</li>
      </ul>
    </div>
  );
}
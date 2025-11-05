// File: AgentStatusPanel.tsx
// Location: /project-dashboard/src/components/

import React, { useEffect, useState } from 'react';

const statusColors = {
  planned: '🟡 Planned',
  implemented: '🟠 Implemented',
  running: '🟢 Running'
};

const AgentStatusPanel = () => {
  const [agents, setAgents] = useState([]);

  useEffect(() => {
    fetch('/api/agents') // You can serve agentRegistry.json via FastAPI or Express
      .then(res => res.json())
      .then(data => setAgents(Object.values(data)));
  }, []);

  return (
    <div className="agent-status-panel">
      <h3>🧠 Agent Status Overview</h3>
      {agents.map(agent => (
        <div key={agent.name} className="agent-card">
          <strong>{agent.name}</strong><br />
          Status: {statusColors[agent.status]}<br />
          Port: {agent.port ? `🔌 ${agent.port}` : '—'}<br />
          Last Updated: {agent.lastUpdated}<br />
          {agent.cid && <span>CID: {agent.cid}</span>}
        </div>
      ))}
    </div>
  );
};

export default AgentStatusPanel;
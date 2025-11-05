// File: PortStatusPanel.tsx
// Location: /project-dashboard/src/components/

import React, { useEffect, useState } from 'react';

const PortStatusPanel = () => {
  const [ports, setPorts] = useState([]);

  useEffect(() => {
    fetch('/api/ports')
      .then(res => res.json())
      .then(data => setPorts(data));
  }, []);

  return (
    <div className="port-status">
      {ports.map(({ project, port }) => (
        <div key={port} className="port-card">
          <strong>{project}</strong>: Port {port} 🟢 Running
        </div>
      ))}
    </div>
  );
};

export default PortStatusPanel;
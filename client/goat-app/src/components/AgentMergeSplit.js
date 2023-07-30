import React, { useState } from 'react';
import axios from 'axios';

const AgentMergeSplit = () => {
  const [toAgentId, setToAgentId] = useState('');
  const [fromAgentId, setFromAgentId] = useState('');
  const [fromAgentIds, setFromAgentIds] = useState('');
  const [splitToAgentIds, setSplitToAgentIds] = useState('');

  const handleMergeSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.put('/api/agent-merge-split/1/', {
        merge: {
          to_agent_id: toAgentId,
          from_agent_ids: fromAgentIds.split(',').map((id) => id.trim()),
        },
      });
      console.log('Merge Response:', response.data);
      // Handle success, show a success message or redirect as needed
    } catch (error) {
      console.error('Merge Error:', error);
      // Handle error, show an error message or perform error handling
    }
  };

  const handleSplitSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.put('/api/agent-merge-split/1/', {
        split: {
          from_agent_id: fromAgentId, // Use toAgentId here instead of fromAgentIds
          to_agent_ids: splitToAgentIds.split(',').map((id) => id.trim()),
        },
      });
      console.log('Split Response:', response.data);
      // Handle success, show a success message or redirect as needed
    } catch (error) {
      console.error('Split Error:', error);
      // Handle error, show an error message or perform error handling
    }
  };

  return (
    <div>
      <h2>Agent Merge Split Component</h2>
      <h3>Merge</h3>
      <form onSubmit={handleMergeSubmit}>
        <label>
          To Agent ID:
          <input type="text" value={toAgentId} onChange={(e) => setToAgentId(e.target.value)} />
        </label>
        <br />
        <label>
          From Agent IDs (comma-separated):
          <input type="text" value={fromAgentIds} onChange={(e) => setFromAgentIds(e.target.value)} />
        </label>
        <br />
        <button type="submit">Merge</button>
      </form>
      <h3>Split</h3>
      <form onSubmit={handleSplitSubmit}>
        <label>
          From Agent ID:
          <input type="text" value={fromAgentId} onChange={(e) => setFromAgentId(e.target.value)} /> {/* Use toAgentId here instead of fromAgentIds */}
        </label>
        <br />
        <label>
          To Agent IDs (comma-separated):
          <input type="text" value={splitToAgentIds} onChange={(e) => setSplitToAgentIds(e.target.value)} />
        </label>
        <br />
        <button type="submit">Split</button>
      </form>
    </div>
  );
};

export default AgentMergeSplit;

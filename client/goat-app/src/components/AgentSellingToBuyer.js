import React, { useState } from 'react';
import axios from 'axios';

const AgentSellingToBuyer = () => {
  const [agentId, setAgentId] = useState('');
  const [goatIds, setGoatIds] = useState('');
  const [buyerId, setBuyerId] = useState('');
  const [amountPaid, setAmountPaid] = useState('');

  const handleSellToBuyer = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/agent-selling-to-buyer/', {
        agent_id: agentId,
        goat_ids: goatIds.split(',').map((id) => parseInt(id.trim())),
        buyer_id: buyerId,
        amount_paid: amountPaid,
      });
      console.log('Sale to Buyer Successful:', response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <h2>Agent Selling to Buyer Component</h2>
      <div>
        <input
          type="text"
          placeholder="Agent ID"
          value={agentId}
          onChange={(e) => setAgentId(e.target.value)}
        />
        <input
          type="text"
          placeholder="Goat IDs (comma-separated)"
          value={goatIds}
          onChange={(e) => setGoatIds(e.target.value)}
        />
        <input
          type="text"
          placeholder="Buyer ID"
          value={buyerId}
          onChange={(e) => setBuyerId(e.target.value)}
        />
        <input
          type="text"
          placeholder="Amount Paid"
          value={amountPaid}
          onChange={(e) => setAmountPaid(e.target.value)}
        />
        <button onClick={handleSellToBuyer}>Sell to Buyer</button>
      </div>
    </div>
  );
};

export default AgentSellingToBuyer;

import React, { useState } from 'react';
import axios from 'axios';

const SellerSellingToAgent = () => {
  const [sellerId, setSellerId] = useState('');
  const [agentId, setAgentId] = useState('');
  const [amountPaid, setAmountPaid] = useState('');
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/seller-selling-to-agent/', {
        seller_id: sellerId,
        agent: agentId,
        paid_amount: amountPaid,
      });
      console.log('Response:', response.data);
      // Handle success, show a success message or redirect as needed
    } catch (error) {
      console.error('Error:', error);
      // Handle error, show an error message or perform error handling
    }
  };

  return (
    <div>
      <h2>Seller Selling to Agent Component</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Seller ID:
          <input type="text" value={sellerId} onChange={(e) => setSellerId(e.target.value)} />
        </label>
        <br />
        <label>
          Agent ID:
          <input type="text" value={agentId} onChange={(e) => setAgentId(e.target.value)} />
        </label>
        <br />
        <label>
          Amount Paid:
          <input type="text" value={amountPaid} onChange={(e) => setAmountPaid(e.target.value)} />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default SellerSellingToAgent;

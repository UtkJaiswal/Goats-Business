// src/components/BuyerGoatList.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const BuyerGoatList = ({ match }) => {
  const [buyerGoats, setBuyerGoats] = useState([]);
  const buyer_id = match.params.buyer_id
  
  useEffect(() => {
    // Fetch goats belonging to the buyer from the backend API
    axios.get(`http://localhost:8000/api/buyer-goats/${buyer_id}/`)
      .then((response) => {
        setBuyerGoats(response.data);
      })
      .catch((error) => {
        console.error('Error fetching buyer goats:', error);
      });
  }, [buyer_id]);

  return (
    <div>
      <h1>Buyer's Goat List</h1>
      <ul>
        {buyerGoats.map((goat) => (
          <li key={goat.id}>
            Goat Id - {goat.id}
            <br></br>
            {goat.sex} - {goat.weight} kg
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BuyerGoatList;

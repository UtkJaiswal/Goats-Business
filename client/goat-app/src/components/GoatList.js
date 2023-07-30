// src/components/GoatList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const GoatList = () => {
  const [goats, setGoats] = useState([]);

  useEffect(() => {
    // Fetch all goats from the backend API
    axios.get('/api/goats/')
      .then((response) => {
        setGoats(response.data);
      })
      .catch((error) => {
        console.error('Error fetching goats:', error);
      });
  }, []);

  return (
    <div>
      <h1>Goat List</h1>
      <ul>
        {goats.map(goat => (
            
          <li key={goat.id}>Goat with id - {goat.id}</li>
        ))}
      </ul>
    </div>
  );
};

export default GoatList;

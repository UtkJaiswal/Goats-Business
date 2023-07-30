import React, { useState } from 'react';
import axios from 'axios';

const CreateGoatBySeller = ({ match }) => {
  const sellerId = match.params.seller_id;
  const [goats, setGoats] = useState([
    { sex: 'Male', weight: 0 },
    { sex: 'Female', weight: 0 },
  ]);

  const handleGoatChange = (index, field, value) => {
    setGoats((prevGoats) => {
      const updatedGoats = [...prevGoats];
      updatedGoats[index][field] = value;
      return updatedGoats;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Seller id",sellerId)
    try {
      const response = await axios.post('http://localhost:8000/api/seller-create-goat/', {
        goats,
        seller_id: sellerId,
      });

      console.log('Goats created:', response.data);
      // Handle success, show a success message or redirect as needed
    } catch (error) {
      console.error('Error creating goats:', error);
      // Handle error, show an error message or perform error handling
    }
  };

  const handleAddGoat = () => {
    setGoats((prevGoats) => [...prevGoats, { sex: 'Male', weight: 0 }]);
  };

  return (
    <div>
      <h2>Create Goat by Seller</h2>
      <form onSubmit={handleSubmit}>
        {goats.map((goat, index) => (
          <div key={index}>
            <label>
              Sex:
              <select value={goat.sex} onChange={(e) => handleGoatChange(index, 'sex', e.target.value)}>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </label>
            <br />
            <label>
              Weight:
              <input
                type="number"
                value={goat.weight}
                onChange={(e) => handleGoatChange(index, 'weight', e.target.value)}
              />
            </label>
            <br />
          </div>
        ))}
        <button type="submit">Create Goats</button>
      </form>
      <button onClick={handleAddGoat}>Add Goat</button>
    </div>
  );
};

export default CreateGoatBySeller;

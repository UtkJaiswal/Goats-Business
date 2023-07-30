// src/components/NewUserForm.js
import React, { useState } from 'react';
import axios from 'axios';

const NewUserForm = () => {
  const [formData, setFormData] = useState({
    type: '',
    name: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Post the form data to the backend API
    axios.post('http://localhost:8000/api/users/', formData)
      .then((response) => {
        console.log('User created successfully:', response.data);
        // Clear the form after successful submission
        setFormData({
          type: '',
          name: '',
        });
      })
      .catch((error) => {
        console.error('Error creating user:', error);
      });
  };

  return (
    <div>
      <h2>Create New User</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="type">Type:</label>
          <select
            id="type"
            name="type"
            value={formData.type}
            onChange={handleChange}
            required
          >
            <option value="">Select User Type</option>
            <option value="Seller">Seller</option>
            <option value="Agent">Agent</option>
            <option value="Buyer">Buyer</option>
          </select>
        </div>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit">Create User</button>
      </form>
    </div>
  );
};

export default NewUserForm;

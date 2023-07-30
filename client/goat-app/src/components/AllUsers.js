import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AllUsers = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users/');
        setUsers(response.data);
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };
    fetchUsers();
  }, []);

  return (
    <div>
      <h1>All Users</h1>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            Name: {user.name}, Type: {user.type}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AllUsers;

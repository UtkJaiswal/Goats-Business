import React, { useState, useEffect } from 'react';
import axios from 'axios';
// import { useParams } from 'react-router-dom';
// import { withRouter } from 'react-router-dom';

const AgentGoatList = ({ match }) => {
  const agent_id  = match.params.agent_id;
  const [goats, setGoats] = useState([]);

  useEffect(() => {
    const fetchAgentGoats = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/agent-goats/${agent_id}/`);
        setGoats(response.data);
      } catch (error) {
        console.error('Error fetching agent goats:', error);
      }
    };
    fetchAgentGoats();
  }, [agent_id]);

  return (
    <div>
      <h1>Agent Goats List</h1>
      <ul>
        {goats.map((goat) => (
          <li key={goat.id}>Goat id - {goat.id}</li>
        ))}
      </ul>
    </div>
  );
};

export default AgentGoatList;

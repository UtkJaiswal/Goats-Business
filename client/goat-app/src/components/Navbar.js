import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Goat List</Link>
        </li>
        <li>
          <Link to="/create-goat-by-seller/1">Create Goat By Seller</Link>
        </li>
        <li>
          <Link to="/seller-selling-to-agent">Seller Selling to Agent</Link>
        </li>
        <li>
          <Link to="/agent-goat-list/1">Agent Goat List</Link>
        </li>
        <li>
          <Link to="/agent-merge-split/1">Agent Merge Split</Link>
        </li>
        <li>
          <Link to="/agent-selling-to-buyer">Agent Selling to Buyer</Link>
        {/* <li>
          <Link to="/buyer-goats/4">Buyers Goat List</Link>
        </li> */}
        </li>
        <li>
          <Link to="/create-user">Create User</Link>
        </li>
        <li>
          <Link to="/all-users">All Users</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;

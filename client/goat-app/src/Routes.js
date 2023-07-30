import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'; // Import Switch
import Navbar from './components/Navbar';
import GoatList from './components/GoatList';
// import SellerCreateGoat from './components/SellerCreateGoat';
import SellerSellingToAgent from './components/SellerSellingToAgent';
import AgentMergeSplit from './components/AgentMergeSplit';
import AgentSellingToBuyer from './components/AgentSellingToBuyer';
import NewUserForm from './components/NewUserForm';
import AgentGoatList from './components/AgentGoatList';
import AllUsers from './components/AllUsers'; // Import the AllUsers component
import CreateGoatBySeller from './components/CreateGoatBySeller';
import BuyerGoatList from './components/BuyerGoatList'; // Import the BuyerGoatList component


const Routes = () => {
  return (
    <Router>
      <Navbar />
      <Switch> {/* Wrap Route components with Switch */}
        <Route exact path="/" component={GoatList} />
        {/* <Route exact path="/create-goat" component={SellerCreateGoat} /> */}
        <Route exact path="/seller-selling-to-agent" component={SellerSellingToAgent} />
        <Route path="/agent-goat-list/:agent_id" component={AgentGoatList} />
        {/* <Route exact path="/agent-merge-split/:id" component={AgentMergeSplit} /> */}
        <Route exact path="/agent-merge-split/:id" component={AgentMergeSplit} />
        <Route exact path="/agent-selling-to-buyer" component={AgentSellingToBuyer} />
        <Route path="/create-user" component={NewUserForm} /> 
        <Route path="/all-users" component={AllUsers} />
        {/* <Route path="/create-goat-by-seller" component={CreateGoatBySeller} /> */}
        <Route path="/create-goat-by-seller/:seller_id" component={CreateGoatBySeller} /> {/* Use a placeholder for seller_id */}
        {/* <Route path="/buyer-goats/:buyer_id" component={BuyerGoatList} /> */}

        

      </Switch>
    </Router>
  );
};

export default Routes;

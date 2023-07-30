// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Routes from './Routes';

const App = () => {
  return (
    <Router>
      <div>
        {/* Add any common layout or components here */}
        <Switch>
          {/* Define the routes using the Routes component */}
          <Route path="/" component={Routes} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;

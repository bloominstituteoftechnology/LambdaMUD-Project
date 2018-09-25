import React, { Component } from 'react';
import { BrowserRouter as Router,Route, Link } from "react-router-dom";

import SignIn from './components/sign-in/signin'
import Register from './components/register/register'
import Game from './components/game/game'

class App extends Component {
  render() {
    return (
      <div className="App">
        <Route exact path="/" component={SignIn} />
        <Route path="/register" component={Register} />
        <Route path="/game" component={Game} />
      </div>
    );
  }
}

export default App;

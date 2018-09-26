import React, { Component } from 'react';
import { BrowserRouter as Router,Route, Link } from "react-router-dom";

import SignIn from './components/sign-in/signin'
import Register from './components/register/register'
import Game from './components/game/game'

class App extends Component {
  constructor(){
    super();
    this.state = {
      key: ''
    }
    this.setKey = this.setKey.bind(this);
  }
  setKey(value){
    this.setState({
      key: value
    })
  }
  render() {
    return (
      <div className="App">
        <Route exact path="/" render={(props) => <SignIn {...props} getKey={this.setKey} />} />
        <Route path="/register" render={(props) => <Register {...props} getKey={this.setKey} />} />
        <Route path="/game" component={Game} />
      </div>
    );
  }
}

export default App;

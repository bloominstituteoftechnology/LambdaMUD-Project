import React, { Component } from 'react';
import { BrowserRouter as Router,Route, Link } from "react-router-dom";
import { Redirect } from 'react-router'

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
        <Route exact path="/" render={(props) => this.state.key ? (<Redirect to="/game"/>) : <SignIn {...props} getKey={this.setKey} />} />
        <Route path="/register" render={(props) => <Register {...props} getKey={this.setKey} />} />
        <Route path="/game" render={(props) => <Game {...props} UserKey={this.state.key} />} />
      </div>
    );
  }
}

export default App;

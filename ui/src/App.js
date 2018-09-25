import React, { Component } from 'react';
import './App.css';
import SignIn from './components/sign-in/signin'
class App extends Component {
  render() {
    return (
      <div className="App">
        <SignIn />
      </div>
    );
  }
}

export default App;

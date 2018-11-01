import React, { Component } from 'react';
// import { Route } from 'react-router-dom';
import './App.css';
import Login from './components/Login/Login';
import MainPage from './components/Main/Main';
import NewAcct from './components/Create-Acct/Create-acct';
import Authenticate from "./components/Authenticate/Authenticate";

class App extends Component {
  constructor() {
    super();
    this.state = {
      username: ""
    };
  }

  componentDidMount() {
    const user = localStorage.getItem("user");
    this.setState({ username: user });
  }
  render() {
    return (
      <div className="App">
        <Login />
        <NewAcct />
        <MainPage />
      </div>
    );
  }
}

export default Authenticate(App);

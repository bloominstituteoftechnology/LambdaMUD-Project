import React, { Component } from 'react';
import './App.css';
import { NavLink, Route} from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';

const Home = props => {
  return (
    <div>
      <h1>WELCOME TO LAMBDA MUD</h1>
    </div>
  )
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <header classname="App-header">
          <nav>
            <NavLink to="/" exact>Home</NavLink>
            &nbsp;|&nbsp;
            <NavLink to="/login">Login</NavLink>
            &nbsp;|&nbsp;
            <NavLink to="/signup">Signup</NavLink>
          </nav>
          <main>
            <Route path="/" exact component={Home}></Route>
            <Route path="/login" component={Login}></Route>
            <Route path="/signup" component={Signup}></Route>
          </main>
        </header>
      </div>
    );
  }
}

export default App;

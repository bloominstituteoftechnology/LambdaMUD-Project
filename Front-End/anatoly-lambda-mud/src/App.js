import React, { Component } from 'react';
import './App.css';
import { NavLink, Route} from 'react-router-dom';
import Login from './components/Login';
import Signup from './components/Signup';
import Main from './components/Main';

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
        <header className="App-header">

         {localStorage.token ? null : <nav>
            <NavLink to="/" exact>Home</NavLink>
            &nbsp;|&nbsp;
            <NavLink to="/login">Login</NavLink>
            &nbsp;|&nbsp;
            <NavLink to="/signup">Signup</NavLink>
          </nav>}
          <main>
            <Route path="/" exact component={Home}></Route>
            <Route path="/login" component={Login}></Route>
            <Route path="/signup" component={Signup}></Route>
            <Route path="/main" component={Main}></Route>
          </main>
        </header>
      </div>
    );
  }
}

export default App;

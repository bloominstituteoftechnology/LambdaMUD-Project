import React, { Component } from 'react';
import Routes from "./Routes/Routes";
import { Link } from "react-router-dom";
import { Nav, Navbar, NavItem } from "react-bootstrap";
import './App.css';
import { LinkContainer } from "react-router-bootstrap";

class App extends Component {

  render() {
    return (
      <div className="App container">
        <Navbar className="" fluid collapseOnSelect>
          <Navbar.Header>
            <Navbar.Brand>
              <Link to="/">LambdaMUD</Link>
            </Navbar.Brand>
            <Navbar.Toggle />
          </Navbar.Header>

          <Navbar.Collapse>
            <Nav pullRight>
              
              <LinkContainer to="/adventure">
                <NavItem>Adventure</NavItem>
              </LinkContainer>
              <LinkContainer to="/register">
                <NavItem>Register</NavItem>
              </LinkContainer>
              

              <LinkContainer to="/login">
                <NavItem>Login</NavItem>
              </LinkContainer>

            </Nav>
          </Navbar.Collapse>
        </Navbar>
        <Routes />
      </div>
    );
  }
}

export default App;

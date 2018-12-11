import React, { Component } from 'react';
import '../App.css';
import axios from 'axios';

class Login extends Component {
    state = {
        username: '',
        password: ''
    }
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
           <div><label htmlFor="username">Username</label><input value={this.state.username} onChange={this.handleInputChange} type="text"/></div>
           <div><label htmlFor="password">Password</label><input value={this.state.password} onChange={this.handleInputChange} type="password"/></div>
           <div><button type="submit">Login</button></div>
        </form>
      );
    }

    handleInputChange = event => {
        const { name, value } = event.target;
        this.setState({ [name]: value});
    }

    handleSubmit = event => {
        event.preventDefault();
        const endpoint = "https://anatoly-lambda-mud.herokuapp.com/api/login/";

        axios.post(endpoint, this.state)
        .then(res => {
            console.log(res.data);
            localStorage.setItem('jwt', res.data.token)
        })
        .catch(err => {
            console.error('ERROR', err);
        })
    }
  }

  export default Login;
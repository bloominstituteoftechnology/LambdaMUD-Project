import React, { Component } from 'react';
import '../App.css';
import axios from 'axios';

class Signup extends Component {
    state = {
        username: '',
        password: '',
        passwordagain: ''
    }
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
           <div><label htmlFor="username">Username</label><input name="username" value={this.state.username} onChange={this.handleInputChange} type="text"/></div>
           <div><label htmlFor="password">Password</label><input name="password" value={this.state.password} onChange={this.handleInputChange} type="password"/></div>
           <div><label htmlFor="password">Password Again</label><input name="password" value={this.state.passwordagain} onChange={this.handleInputChange} type="password"/></div>
           <div><button type="submit">Signup</button></div>
        </form>
      );
    }

    handleInputChange = event => {
        const { name, value } = event.target;
        this.setState({ [name]: value});
    }

    handleSubmit = event => {
        event.preventDefault();
        const endpoint = "https://anatoly-lambda-mud.herokuapp.com/api/registration/";

        axios.post(endpoint, this.state)
        .then(res => {
            console.log(res.data);
        })
        .catch(err => {
            console.error('ERROR', err);
        })
    }
  }

  export default Signup;
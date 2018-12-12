import React, { Component } from 'react';
import '../App.css';
import axios from 'axios';

class Signup extends Component {
    state = {
        username: '',
        password1: '',
        password2: ''
    }
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
           <div><label htmlFor="username">Username</label><input name="username" value={this.state.username} onChange={this.handleInputChange} type="text"/></div>
           <div><label htmlFor="password">Password1</label><input name="password1" value={this.state.password} onChange={this.handleInputChange} type="password"/></div>
           <div><label htmlFor="password">Password2</label><input name="password2" value={this.state.passwordagain} onChange={this.handleInputChange} type="password"/></div>
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
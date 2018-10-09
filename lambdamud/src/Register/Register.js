import React, { Component } from "react";
import {
  HelpBlock,
  FormGroup,
  FormControl,
  ControlLabel
} from "react-bootstrap";
import LoaderButton from "../LoaderButton/LoaderButton";
import "./Register.css";
import axios from 'axios';

export default class Register extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      username: "",
      password: "",
      confirmPassword: "",
      confirmationCode: "",
      newUser: null
    };
  }

  validateForm() {
    return (
      this.state.username.length > 0 &&
      this.state.password.length > 0 &&
      this.state.password === this.state.confirmPassword
    );
  }

  validateConfirmationForm() {
    return this.state.confirmationCode.length > 0;
  }

  handleChange = event => {
    console.log("Value: ", event.target.value,"ID: ", event.target.id);
    this.setState({
      [event.target.id]: event.target.value
    });
  }

  // handleSubmit = async event => {
  //   event.preventDefault();

  //   this.setState({ isLoading: true });

  //   console.log(this.state.newUser, this.state.username);
  //   // this.setState({ newUser: this.state.username });
  //   this.setState(prevState => this.state.newUser : prevState.username)
  //   console.log(this.state.newUser, this.state.username, "After");

  //   this.setState({ isLoading: false });
  // }

  handleSubmit = async e => {
    e.preventDefault();

    const apiUrl = 'http://localhost:8000';
     
    // axios
    //     // .get('http://localhost:8888/notes')
    //     .get(apiUrl+`/notes`)
    //     .then(response => {
    //         console.log("GET", response);
    //         this.setState({notes: response.data.notes });
    //     })
    //     .catch(err => {
    //         console.log(err);
    //     })
    const user = { "username": this.state.username, "password1": this.state.password, "password2": this.state.confirmPassword }

    axios
        // .post('http://localhost:8888/notes', note)
        .post(apiUrl+`/api/registration`, user)
        .then(response => {
          // console.log("POST Response", response);
          localStorage.setItem("key", response.data.key);
          console.log(response.data.key);
          console.log(localStorage.getItem("key"));
            this.setState({
                user: {
                    "username": '',
                    "password1": '',
                    "password2": ''
                }
            });
            // this.props.history.push('/');
        })
        .catch( error => console.log(error));
  }

  handleConfirmationSubmit = async event => {
    event.preventDefault();

    this.setState({ isLoading: true });
  }

  renderConfirmationForm() {
    return (
      <form onSubmit={this.handleConfirmationSubmit}>
        <FormGroup controlId="confirmationCode" bsSize="large">
          <ControlLabel>Confirmation Code</ControlLabel>
          <FormControl
            autoFocus
            type="tel"
            value={this.state.confirmationCode}
            onChange={this.handleChange}
          />
          <HelpBlock>Please check your username for the code.</HelpBlock>
        </FormGroup>
        <LoaderButton
          block
          bsSize="large"
          disabled={!this.validateConfirmationForm()}
          type="submit"
          isLoading={this.state.isLoading}
          text="Verify"
          loadingText="Verifying…"
        />
      </form>
    );
  }

  renderForm() {
    return (
      <form onSubmit={this.handleSubmit}>
        <FormGroup controlId="username" bsSize="large">
          <ControlLabel>Username</ControlLabel>
          <FormControl
            autoFocus
            type="text"
            value={this.state.username}
            onChange={this.handleChange}
          />
        </FormGroup>
        <FormGroup controlId="password" bsSize="large">
          <ControlLabel>Password</ControlLabel>
          <FormControl
            value={this.state.password}
            onChange={this.handleChange}
            type="password"
          />
        </FormGroup>
        <FormGroup controlId="confirmPassword" bsSize="large">
          <ControlLabel>Confirm Password</ControlLabel>
          <FormControl
            value={this.state.confirmPassword}
            onChange={this.handleChange}
            type="password"
          />
        </FormGroup>
        <LoaderButton
          block
          bsSize="large"
          disabled={!this.validateForm()}
          type="submit"
          isLoading={this.state.isLoading}
          text="Register"
          loadingText="Signing up…"
        />
      </form>
    );
  }

  render() {
    return (
      <div className="Register">
        {this.state.newUser === null
          ? this.renderForm()
          : this.renderConfirmationForm()}
      </div>
    );
  }
}
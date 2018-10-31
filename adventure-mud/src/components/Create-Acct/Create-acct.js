import React, { Component } from "react";
import { Button, Form, FormGroup, Input } from "reactstrap";
import './Create-Acct.css';
import axios from 'axios';

export default class NewAcct extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: ""
        };
    }

    componentDidMount() {
        axios
            .post('http://adventure-mud-app.herokuapp.com/api/registration')
            .then(response => {
                this.setState(() => (response.data));
            })
            .catch(error => {
                console.error('Server Error', error);
            });
    }

    handleInputChange = e => {
        this.setState({ [e.target.name]: e.target.value });
    };

    handleCreateSubmit = e => {
        const user = this.state.username;
        localStorage.setItem("user", user);
        window.location.reload();
    };

    render() {
        return (
            <Form className="new-acct-form">
                <h3>Create New Account</h3>
                <div>Fill in the fields below and start playing!</div>
                <FormGroup>
                    <Input
                        type="text"
                        placeholder="Login"
                        name="username"
                        value={this.state.username}
                        onChange={this.handleInputChange}
                    />
                </FormGroup>
                <FormGroup>
                    <Input
                        type="text"
                        placeholder="Password"
                        name="password"
                        value={this.state.username}
                        onChange={this.handleInputChange}
                    />
                </FormGroup>
                <FormGroup>
                    <Input
                        type="password"
                        placeholder="Password again"
                        name="password"
                        value={this.state.password}
                        onChange={this.handleInputChange}
                    />
                    <br />
                    <Button color="success" size="large" onClick={this.handleLoginSubmit}>
                        Connect
          </Button>
                </FormGroup>
            </Form>
        );
    }
}

import React, { Component } from "react";
import { Button, Form, FormGroup, Input } from "reactstrap";
import './Create-Acct.css';
import axios from 'axios';

export default class NewAcct extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password1: "",
            password2: ""

        };
    }

                console.error('Server Error', error);
    // componentDidMount() {
    //     axios
    //         .post('http://adventure-mud-app.herokuapp.com/api/registration')
    //         .then(response => {
    //             this.setState(() => (response.data));
    //         })
    //         .catch(error => {
    //             console.error('Server Error', error);
    //         });
    // }

    handleInputChange = e => {
        this.setState({ [e.target.name]: e.target.value });
    };

    handleCreateSubmit = e => {
        const user = this.state.username;
        localStorage.setItem("user", user);
        window.location.reload();
    };

    handleRegister = () => {
        const user = {
            username: this.state.username,
            password1: this.state.password1,
            password2: this.state.password2

        }
        axios
            .post('http://adventure-mud-app.herokuapp.com/api/registration', user)
            .then(response => {
                localStorage.setItem("key", response.data.key)
                console.log(response.data.key)
            })
            .catch(error => {
                console.error('Fire', error);
            });


    }

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
                        name="password1"
                        value={this.state.password1}
                        onChange={this.handleInputChange}
                    />
                </FormGroup>
                <FormGroup>
                    <Input
                        type="password"
                        placeholder="Password again"
                        name="password2"
                        value={this.state.password2}
                        onChange={this.handleInputChange}
                    />
                    <br />
                    <Button type="button" color="success" size="large" onClick={this.handleRegister}>
                        Connect
                    </Button>
                </FormGroup>
            </Form>
        );
    }
}

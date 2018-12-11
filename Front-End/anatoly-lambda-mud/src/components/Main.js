import React, { Component } from 'react';
import '../App.css';
import axios from 'axios';

class Main extends Component {
    render() {
        return (
            <div>
                <textarea></textarea>
                <input type="text"/>
                <div><button type="submit">Send</button></div>
            </div>
        );
    }

    componentDidMount() {
        const token = localStorage.getItem('jwt');
        const endpoint = "";
        const options = {
            headers: {
                Authorization: token
            }
        };
        axios.get(endpoint, options)
        .then(res => {
            console.log(res.data);
            localStorage.setItem('jwt', res.data.token)
        })
        .catch(err => {
            console.error('ERROR', err);
        })
    }
}
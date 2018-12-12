import React, { Component } from 'react';
import '../App.css';
import axios from 'axios';

class Main extends Component {
    state = {

    }
    

    componentWillMount = () => {
        const token = localStorage.getItem('jwt');
        console.log("token", token)
        const endpoint = "https://anatoly-lambda-mud.herokuapp.com/api/adv/init";
        const options = {
            headers: {
                "Authorization": `Token ${token}`
            }
        };
        console.log("token", token)
        axios.get(endpoint, options)
        .then(res => {
            console.log(res.data);
        })
        .catch(err => {
            console.error('ERROR', err);
        })   
    }

    render() {
        return (
            <div>
                <textarea></textarea>
                <input type="text"/>
                <div><button type="submit">Send</button></div>
            </div>
        );
    }
}

export default Main;
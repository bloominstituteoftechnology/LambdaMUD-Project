import React, { Component } from 'react';
import '../App.css';
import axios from 'axios';
import Pusher from 'pusher-js'

// PUSHER
var pusher = new Pusher("a9f6b358f25143cf995c", {
    cluster: "us2"
});


class Main extends Component {
    state = {
        description: "",
        name: "",
        players: [],
        title: "",
        uuid: "",
        move: "",
        say: ""
    }

    handleInputChange = event => {
        console.log(event.target.value)
        const { name, value } = event.target;
        this.setState({ [name]: value});
    }

    submitDir = () => {
        const token = localStorage.getItem("jwt");
        console.log("token", token)
        const endpoint = "https://anatoly-lambda-mud.herokuapp.com/api/adv/move";
        const options = {
            headers: {
                "Authorization": `Token ${token}`
            }
        };
        console.log("token", token)
        axios.post(endpoint, {direction: this.state.move}, options)
        .then(res => {
            this.setState({
                description: res.data.description,
                name: res.data.name,
                players: res.data.players,
                title: res.data.title
            })
            console.log(res.data);
        })
        .catch(err => {
            console.error('ERROR', err);
        })
    }

    submitSay = () => {
        const token = localStorage.getItem("jwt");
        console.log("token", token)
        const endpoint = "https://anatoly-lambda-mud.herokuapp.com/api/adv/say";
        const options = {
            headers: {
                "Authorization": `Token ${token}`
            }
        };
        console.log("token", token)
        axios.post(endpoint, {message: this.state.say}, options)
        .then(res => {
            this.setState({
                description: res.data.description,
                name: res.data.name,
                players: res.data.players,
                title: res.data.title,
                say: res.data.say
            })
            console.log(res.data);
        })
        .catch(err => {
            console.error('ERROR', err);
        })
    }
    
    

    componentWillMount = () => {
        const token = localStorage.getItem("jwt");
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
            // console.log(res.data);

            this.setState({
            description: res.data.description,
            name: res.data.name,
            players: res.data.players,
            title: res.data.title,
            uuid: res.data.uuid
            })
            console.log(this.state);
        })
        .catch(err => {
            console.error('ERROR', err);
        })
        var channel = pusher.subscribe(`p-channel-${this.state.uuid}`);

        channel.bind('broadcast', function(data) {
        console.log('An event was triggered with message: ' + data.message);
        });

    }

    render() {
        console.log("this.state", this.state);
        return (
            <div>
                <p>description: {this.state.description}</p>
                <p>name: {this.state.name}</p>
                <p>players: {this.state.players}</p>
                <p>title: {this.state.title}</p>
                <p>say: {this.state.say}</p>
                <input name="move" onChange={this.handleInputChange}  type="text"/>
                <div><button onClick={()=>this.submitDir()} type="submit">Send</button></div>

                <input name="say" onChange={this.handleInputChange}  type="text"/>
                <div><button onClick={()=>this.submitSay()} type="submit">Say</button></div>
            </div>
        );
    }
}

export default Main;
import React, { Component } from "react";
import "./Home.css";

export default class Home extends Component {
  render() {
    return (
      <div className="Home">
        <div className="lander">
          <h1>LambdaMUD</h1>
          <p>Welcome to your own text-based adventure!</p>
        </div>
      </div>
    );
  }
}
import React from "react";
import { Route, Switch } from "react-router-dom";
import Home from "../Home/Home";
import NotFound from "../NotFound/NotFound"
import Login from "../Login/Login"
import Register from "../Register/Register"

export default () =>
  <Switch>
    <Route path="/" exact component={Home} />
    <Route path="/login" exact component={Login} />
    <Route path="/register" exact component={Register} />
    <Route component={NotFound} />
  </Switch>;
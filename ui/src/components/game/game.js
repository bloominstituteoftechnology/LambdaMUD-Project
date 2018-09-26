import Paper from '@material-ui/core/Paper';
import React from 'react';
import withStyles from '@material-ui/core/styles/withStyles';
import Input from '@material-ui/core/Input';

import axios from 'axios';

const styles = theme => ({
  layout: {
    width: 'auto',
    display: 'block', // Fix IE11 issue.
    marginLeft: theme.spacing.unit * 3,
    marginRight: theme.spacing.unit * 3,
    [theme.breakpoints.up(400 + theme.spacing.unit * 3 * 2)]: {
      width: 400,
      marginLeft: 'auto',
      marginRight: 'auto',
    },
  },
  paper: {
    marginTop: '70%',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: `${theme.spacing.unit * 2}px ${theme.spacing.unit * 3}px ${theme.spacing.unit * 3}px`,
  }
})

class Game extends React.Component {

  componentDidMount(){
    axios.get('http://localhost:8000/api/adv/init/', {
      headers: {
        Authorization: `Token ${this.props.UserKey}`
      }
    })
    .then(response => {
      console.log(response.data)
    })
    .catch(err => {
      console.log(err)
    })
  }

  render(){
    return(
      <main className={this.props.classes.layout}>
        <Paper className={this.props.classes.paper}>
          <Input />
        </Paper>
      </main>
    )
  }
}

export default withStyles(styles)(Game);

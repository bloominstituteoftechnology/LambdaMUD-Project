import Paper from '@material-ui/core/Paper';
import React from 'react';
import withStyles from '@material-ui/core/styles/withStyles';
import Input from '@material-ui/core/Input';
import Avatar from '@material-ui/core/Avatar';
import Face from '@material-ui/icons/Face';
import Backdrop from '@material-ui/core/Backdrop';
import Tooltip from '@material-ui/core/Tooltip';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import Person from '@material-ui/icons/Person';
import ListItemText from '@material-ui/core/ListItemText';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import Collapse from '@material-ui/core/Collapse';
import KeyboardArrowDown from '@material-ui/icons/KeyboardArrowDown';
import KeyboardArrowUp from '@material-ui/icons/KeyboardArrowUp';
import KeyboardArrowLeft from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRight from '@material-ui/icons/KeyboardArrowRight';

import axios from 'axios';
import Pusher from 'pusher-js';

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
    padding: `${theme.spacing.unit * 1}px ${theme.spacing.unit * 1}px ${theme.spacing.unit * 1}px`,
  },
  avatarDiv: {
    display: 'flex',
    alignItems: 'center',
    fontSize: '20px',
  },
  avatarName: {
    marginRight: '5%'
  },
  location: {
    marginTop: '40px',
    display: 'flex',
    justifyContent: 'center'
  },
  nested: {
    paddingLeft: theme.spacing.unit * 4,
  },
  listFormat: {
    marginTop: '20px'
  },
  controlNav: {
    marginTop: '20px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'column'
  },
  controlNavLeft: {
    marginRight: '24px'
  }
})

class Game extends React.Component {
  constructor(){
    super();
    this.state = {
      title: '',
      description: '',
      open: false,
      players: []
    }
    this.updateDirection = this.updateDirection.bind(this);
    this.testCode = this.testCode.bind(this);
  }
  componentDidMount(){
    axios.get('http://localhost:8000/api/adv/init/', {
      headers: {
        Authorization: `Token ${this.props.UserKey}`
      },

    })
    .then(response => {
      this.setState(response.data)
      this.testCode()
    })
    .catch(err => {
      console.log(err)
    })
  }

  handleClick = () => {
    this.setState(state => ({ open: !state.open }));
  };

  updateDirection(direction) {
    let data = JSON.stringify({
        direction: direction
    })
    axios.post('http://localhost:8000/api/adv/move/', data, {
      headers: {
        Authorization: `Token ${this.props.UserKey}`,
        'Content-Type': 'application/json'
      }
    })
    .then(response => {
      this.setState(response.data)
      this.testCode()
    })
    .catch(err => {
      console.log(err)
    })
  }

  testCode = () => {
    console.log(this.state.title)
    Pusher.logToConsole = true;
    var pusher = new Pusher('4cfbe190ec6e8e3b3534', {
      cluster: 'us2',
    });

    var channel = pusher.subscribe(this.state.title.split(" ").join(''));
    channel.bind('say', (data) => {
      this.setState({pusher: data.message});
    });
  }
  render(){
    return(
      <main className={this.props.classes.layout}>
        <Backdrop open={true}/>
        <Paper className={this.props.classes.paper}>
          <div className={this.props.classes.avatarDiv}>
            <Avatar className={this.props.classes.avatarName}>
              <Face />
            </Avatar>
            {this.state.name}
          </div>
          <Tooltip title={this.state.description} placement="top">
            <div className={this.props.classes.location}>
                {this.state.title}
            </div>
          </Tooltip>
          <div className={this.props.classes.controlNav}>
            <KeyboardArrowUp onClick={() => this.updateDirection('n')}/>
            <div>
              <KeyboardArrowLeft onClick={() => this.updateDirection('w')} className={this.props.classes.controlNavLeft}/>
              <KeyboardArrowRight onClick={() => this.updateDirection('e')} />
            </div>
            <KeyboardArrowDown onClick={() => this.updateDirection('s')} />
          </div>
          <List className={this.props.classes.listFormat}>
            <ListItem button onClick={this.handleClick}>
              <ListItemIcon>
                <Person />
              </ListItemIcon>
              <ListItemText inset primary="Users" />
              {this.state.open ? <ExpandLess /> : <ExpandMore />}
            </ListItem >
            <Collapse in={this.state.open} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {this.state.players.map(function(ele, index){
                return(
                  <ListItem button className={this.props.classes.nested} key={index}>
                    <ListItemIcon>
                      <Person />
                    </ListItemIcon>
                    <ListItemText inset primary={ele} />
                  </ListItem>
                )
              }.bind(this))}
            </List>
          </Collapse>
          </List>
          <Input/>
        </Paper>
      </main>
    )
  }
}

export default withStyles(styles)(Game);

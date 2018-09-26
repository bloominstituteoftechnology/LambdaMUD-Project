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
    padding: `${theme.spacing.unit * 1}px ${theme.spacing.unit * 1}px ${theme.spacing.unit * 1}px`,
  },
  avatarDiv: {
    display: 'flex',
    alignItems: 'center',
    fontSize: '20px',
    border: '#e6e8ed 1px solid'
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
  }

  handleClick = () => {
    this.setState(state => ({ open: !state.open }));
  };

  componentDidMount(){
    axios.get('http://localhost:8000/api/adv/init/', {
      headers: {
        Authorization: `Token ${this.props.UserKey}`
      }
    })
    .then(response => {
      this.setState(response.data)
    })
    .catch(err => {
      console.log(err)
    })
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
              {this.state.players.map(function(ele){
                return(
                  <ListItem button className={this.props.classes.nested}>
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

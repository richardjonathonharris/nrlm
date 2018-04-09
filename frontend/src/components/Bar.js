import Login from './Login'
import history from './history'
import League from './League'
import Nav from './Nav'
import Home from './Home'
import Profile from './Profile'
import React from 'react';
import ReactDOM from 'react-dom';

var ReactRouter = require('react-router-dom');
var Switch = ReactRouter.Switch;
var Router = ReactRouter.Router;
var Route = ReactRouter.Route;

class Bar extends React.Component{
    render () {
        return (
            <div className='container'>
                <Router history={history}>
                <div>
                    <Nav />
                    <Switch>
                        <Route exact path='/' component={Home} />
                        <Route exact path='/league' component={League} />
                        <Route path='/login' component={Login} />
                        <Route path='/profile' component={Profile} />
                        <Route render={function () {
                            return <p>NOT FOUND HOMES</p>
                        }} />
                    </Switch>
                </div>
                </Router>
            </div>
        )
    }
}

export default Bar;

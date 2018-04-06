import App from './components/App';
import Login from './components/Login'
import history from './components/history'
import League from './components/League'
import Nav from './components/Nav'
import Home from './components/Home'
import React from 'react';
import ReactDOM from 'react-dom';

var ReactRouter = require('react-router-dom');
var Switch = ReactRouter.Switch;
var Router = ReactRouter.Router;
var Route = ReactRouter.Route;

require('./index.css');

ReactDOM.render(
    <div className='container'>
        <Router history={history}>
            <div>
                <Nav />
                <Switch>
                    <Route exact path='/' component={Home} />
                    <Route exact path='/league' component={League} />
                    <Route exact path='/login' component={Login} />
                    <Route render={function () {
                        return <p>NOT FOUND HOMES</p>
                    }} />
                </Switch>
            </div>
        </Router>
    </div>,
    document.getElementById('root')
);

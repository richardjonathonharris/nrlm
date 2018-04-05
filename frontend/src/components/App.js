var React = require('react');
var ReactRouter = require('react-router-dom');
var Router = ReactRouter.BrowserRouter;
var Route = ReactRouter.Route;
var Switch = ReactRouter.Switch;
var Nav = require('./Nav');
var Home = require('./Home');
var League = require('./League');

class App extends React.Component {
  render() {
    return (
        <Router>
            <div className='container'>
                <Nav />
                <Switch>
                    <Route exact path='/' component={Home} />
                    <Route exact path='/league' component={League} />
                    <Route render={function () {
                        return <p>NOT FOUND HOMES</p>
                    }} />
                </Switch>
            </div>
        </Router>
    );
  }
}

module.exports = App;

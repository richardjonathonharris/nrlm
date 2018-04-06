import AuthService from './AuthService';
import withAuth from './withAuth';
import history from './history';

var React = require('react');

const Auth = new AuthService();

class App extends React.Component {
  render() {
    return (
        <div className="App">
            <div className="App-header">
                <h2> Welcome {this.props.user.username}</h2>
            </div>
            <p className="App-intro">
                <button type="button" className="form-submit" onClick={this.handleLogout.bind(this)}>Log Out</button>
            </p>
    </div>
    );
  }
    handleLogout(){
        Auth.logout()
        history.replace('/login');
    }
}

export default withAuth(App);

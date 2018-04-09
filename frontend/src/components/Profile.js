import AuthService from './AuthService';
import withAuth from './withAuth';
import history from './history';

var React = require('react');
var NavLink = require('react-router-dom').NavLink;

const Auth = new AuthService();

class Profile extends React.Component {
    constructor(props) {
        super(props)
        this.logOut = this.logOut.bind(this)
    }
    logOut() {
        Auth.logout()
        history.replace('/')
    }
    render () {
        return (
            <div className='text-contaner'>
                <h3>Hello {Auth.getProfile().username}</h3>
                <button onClick={this.logOut} >Log Out</button>
            </div>
        )
    }
}

export default withAuth(Profile);

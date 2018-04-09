import AuthService from './AuthService';
import withAuth from './withAuth';
import history from './history';

var React = require('react');
var NavLink = require('react-router-dom').NavLink;

const Auth = new AuthService();

function LoginSection (props) {
    const isLoggedIn = props.isLoggedIn;
    if (isLoggedIn) { 
        return (
            <li>
            <NavLink activeClassName='active' to='/profile'>
                {Auth.getProfile().username }
            </NavLink>
            </li>
        )
    }
    else {
        return (
            <li>
                <NavLink activeClassName='active' to='/login'>
                    Login
                </NavLink>
            </li>
        )
    }
}

class Nav extends React.Component {
    logOut () {
        Auth.logout()
        return history.replace('/')
    }
    render() {
        return (
            <div className='nav-container'>
                <ul className='nav'>
                        <li>
                        <NavLink exact activeClassName='active' to='/'>
                            Home
                        </NavLink>
                    </li>
                    <li>
                        <NavLink activeClassName='active' to='/league'>
                            League
                        </NavLink>
                    </li>
                    <LoginSection isLoggedIn={Auth.loggedIn()} />
                </ul>
            </div>
        )
    }
}

export default Nav;

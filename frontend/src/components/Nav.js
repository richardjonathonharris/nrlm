import AuthService from './AuthService';
import withAuth from './withAuth';
import history from './history';

var React = require('react');
var NavLink = require('react-router-dom').NavLink;

const Auth = new AuthService();

class Nav extends React.Component {
    checkLogin () {
        return Auth.loggedIn()
    }
    handleLogout () {
        Auth.logout()
        history.replace('/login')
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
                   {!this.checkLogin()
                        ? <NavLink activeClassName='active' to='/login'>
                            Log In
                        </NavLink>
                        : <li> {this.props.user.username}  
                              <button type="button" className="form-submit" onClick={this.handleLogout.bind(this)}>Log Out</button>
                           </li>
                   }
                </ul>
            </div>
        )
    }
}

export default withAuth(Nav);

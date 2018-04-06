import AuthService from './AuthService';
import history from './history';

var React = require('react');

export default function withAuth(AuthComponent) {
    const Auth = new AuthService('http://127.0.0.1:8000/')
    return class AuthWrapped extends React.Component {
        constructor(){
            super();
            this.state = {
                user:null
            };
        }
        componentWillMount() {
            if (!Auth.loggedIn()) {
                history.replace('/login')
            }
            else {
                try {
                    const profile = Auth.getProfile()
                    this.setState({
                        user: profile
                    })
                }
                catch(err) {
                    Auth.logout()
                    history.replace('/login')
                }
            }
        }
        render() {
            if (this.state.user) {
                return (
                    <AuthComponent history={history} user={this.state.user} />
                )
            }
            else {
                return null
            }
        }
    }
};

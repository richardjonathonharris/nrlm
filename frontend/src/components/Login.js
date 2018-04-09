import AuthService from './AuthService';
import history from './history';
import withAuth from './withAuth';

var React = require('react');

class Login extends React.Component {
    constructor(props){
        super(props)
        this.handleChange = this.handleChange.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.Auth = new AuthService();
    }
    componentWillMount(){
        if(this.Auth.loggedIn()) {
            history.replace('/')
        }
    }
    render(){
        return (
            <div className="center">
                <div className="card">
                <h1>Login</h1>
                <form onSubmit={this.handleFormSubmit}>
                    <input
                        className="form-item"
                        placeholder="Username goes here..."
                        name="username"
                        type="text"
                        onChange={this.handleChange}
                    />
                    <input
                        className="form-item"
                        placeholder="Password goes here..."
                        name="password"
                        type="password"
                        onChange={this.handleChange}
                    />
                    <input
                        className="form-submit"
                        value="SUBMIT"
                        type="submit"
                    />
                </form>
            </div>
        </div>
        );
    }
    handleChange(e){
        this.setState(
            {
                [e.target.name]: e.target.value
            }
        );
    }
    handleFormSubmit(e){
        e.preventDefault();
        this.Auth.login(this.state.username, this.state.password)
            .then(res => {
                history.replace('/');
            })
            .catch(err =>{
                alert(err);
            })
    }
}
export default Login;

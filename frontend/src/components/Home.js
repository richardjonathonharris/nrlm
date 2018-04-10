import AuthService from './AuthService';
import withAuth from './withAuth';

var React = require('react');
var Link = require('react-router-dom').Link;

class Home extends React.Component {
    render () {
        return (
            <div className='text-container'>
                <h1>Here is information about the home component!</h1>
                <p>
                    This is information about our app. Our app is great! We love our app!
                </p>
            </div>
        );
    }
}

export default Home;

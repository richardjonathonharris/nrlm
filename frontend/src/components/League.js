import AuthService from './AuthService';
import withAuth from './withAuth';
import Player from './Player';

const Auth = new AuthService();

var React = require('react');
var Link = require('react-router-dom').Link;

class League extends React.Component {
    render () {
        return (
            <div className='text-container'>
                <h1>Here is information about the league component!</h1>
                <Player />
            </div>
        );
    }
}

export default withAuth(League);

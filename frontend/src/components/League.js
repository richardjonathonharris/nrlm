var React = require('react');
var Link = require('react-router-dom').Link;
var Player = require('./Player');

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

module.exports = League;

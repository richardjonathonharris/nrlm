var React = require('react');
var Link = require('react-router-dom').Link;

class Home extends React.Component {
    render () {
        return (
            <div className='text-container'>
                <h1>Here is information about the home component!</h1>
            </div>
        );
    }
}

module.exports = Home;

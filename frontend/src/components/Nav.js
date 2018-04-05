var React = require('react');
var NavLink = require('react-router-dom').NavLink;

function Nav () {
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
            </ul>
        </div>
    );
}

module.exports = Nav;

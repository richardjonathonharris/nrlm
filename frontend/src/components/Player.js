var React = require('react');
var axios = require('axios');
var helpers = require('../api/Api').helpers;

function DisplayPlayers (props) {
    return (
            <div>
                <ul>
                    {this.state.data}
                </ul>
            </div>
        );
}

class Player extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            data: [],
        };
    }
    componentDidMount() {
        helpers.getAllPlayersData()
            .then(function (info) {
                this.state.data.push(info)
            }.bind(this))
        console.log(this.state)
    }

    render () {
        return (
            <div>
                {this.state.data.length === 0
                    ? <h1>ONE SEC YOU CRAZY CRAZY PERSON!</h1>
                    : <DisplayPlayers data={this.state.data} />}
            </div>
        );
    }
};

module.exports = Player;

var React = require('react');
var axios = require('axios');
var helpers = require('../api/Api').helpers;

function DisplayLeaderboard (props) {
    var playerData = props.data.players.results;
    var gameData = props.data.games.results;
    var leaderboard = helpers.calcLeaderboard(playerData, gameData);

    return (
            <div>
                <ul>
                    {leaderboard.map( function (player) {
                        return (
                            <li key={player.id}>{player.name}, {player.gamesPlayed}, {player.totalPoints}</li>
                        )
                    })}
                </ul>
            </div>
        );
}

function DisplayHistory (props) {
    var players = props.data.data.players.results;
    var games = props.data.data.games.results;
    var events = props.data.data.events.results;
    var identities = props.data.data.identities.results;
    console.log(games)
    var history = helpers.calcHistory(games, players, identities, events);
    console.log(history)
    return ( 'Hi' )
}

function DisplayAll (props) {
    return (
        <DisplayHistory data={props}/>
    );
}

class Player extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            data: null,
        };
    }
    componentDidMount() {
        helpers.getAllPlayersData()
            .then(function (info) {
                this.setState({
                    data: info
                });
            }.bind(this))
    }

    render () {
        return (
            <div>
                {!this.state.data
                    ? <h1>ONE SEC YOU CRAZY CRAZY PERSON!</h1>
                    : <DisplayAll data={this.state.data}/>}
            </div>
        );
    }
};

module.exports = Player;
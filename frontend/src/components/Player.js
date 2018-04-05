var React = require('react');
var axios = require('axios');
var helpers = require('../api/Api').helpers;

function DisplayPlayers (props) {
    var playerData = props.data.players.results;
    var gameData = props.data.games.results;
    var leaderboard = helpers.calcLeaderboard(playerData, gameData);
    console.log(leaderboard)
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
                    : <DisplayPlayers data={this.state.data} />}
            </div>
        );
    }
};

module.exports = Player;

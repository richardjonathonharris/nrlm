import AuthService from './AuthService';
import withAuth from './withAuth';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

const Auth = new AuthService();

var React = require('react');
var axios = require('axios');
var helpers = require('../api/Api').helpers;

function DisplayLeaderboard (props) {
    var playerData = props.players
    var gameData = props.games
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
    var players = props.players;
    var games = props.games;
    var events = props.events;
    var identities = props.identities;
    var history = helpers.calcHistory(games, players, identities, events);
    console.log(history)
    return (
        <table>
            <tbody>
                { history.map(function (match) {
                    return (
                        <tr>
                            <td>
                                <div className='player-container'>{match.player1}</div>
                                <div className='id-container'>{match.identity1}</div>
                            </td>
                            <td>
                                <div className='point-container'>({match.points1} - {match.points2})</div>
                            </td>
                            <td>
                                <div className='player-container'>{match.player2}</div>
                                <div className='id-container'>{match.identity2}</div>
                            </td>
                            <td>
                                <div className='match-container'>{match.event}, Round {match.round}</div>
                            </td>
                        </tr>
                    )})}
            </tbody>
        </table>
    )
}

function DisplayAll (props) {
    return (
        <div className='text-container'>
            <DisplayLeaderboard 
                players={props.data.players.results}
                games={props.data.games.results}
            />
            <DisplayHistory 
                players={props.data.players.results}
                games={props.data.games.results}
                identities={props.data.identities.results}
                events={props.data.events.results}
            />
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
        helpers.getAllPlayersData(localStorage.id_token)
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

export default withAuth(Player);

var axios = require('axios');

var dbName = 'http://127.0.0.1:8000'

function getAllPlayers () {
    return axios.get(dbName + '/players/')
}

function getAllGames () {
    return axios.get(dbName + '/games/')
}

function getAllEvents() {
    return axios.get(dbName + '/events/')
}

function getAllIdentities() {
    return axios.get(dbName + '/identities/')
}

function totalGames (playerId, gamesArray) {
    return (
        gamesArray.reduce(function (acc, obj) {
            if (obj.player === playerId || obj.played_against_player === playerId) {
                return acc + 1
            } else
                return acc
        }, 0)
    )
}

function totalPoints (playerId, gamesArray) {
    return (
        gamesArray.reduce(function (acc, obj) {
            if (obj.player === playerId || obj.played_against_player === playerId) {
                return acc + obj.points
            } else {
                return acc
            }
        }, 0)
    );
};

function createLookup(arrayobs) {
    return arrayobs.reduce((obj, item) => {
        obj[item.id] = item
        return obj
    }, {})
}

function calcHistory(games, players, identities, events) {
    var playerLookup = createLookup(players);
    var identitiesLookup = createLookup(identities);
    var eventsLookup = createLookup(events);

    var history = [];

    function getPoints (points) {
        return String(points) + ' - ' + String(6 - points)
        }
    games.map(function (game) {
        return (
            history.push(
                {'id': game.id,
                'player1': playerLookup[game.player].name,
                'player2': playerLookup[game.played_against_player].name,
                'points': getPoints(game.points)
                }
            )
        )
    })
    return history
}

var helpers = {
    getAllPlayersData: function () {
        return axios.all([getAllPlayers(), getAllGames(), getAllIdentities(), getAllEvents()])
            .then(function (arr) {
                return {
                    'players': arr[0].data,
                    'games': arr[1].data,
                    'identities': arr[2].data,
                    'events': arr[3].data
                }
            })
    },
    calcLeaderboard: function (playersArray, gamesArray) {
        var playerGames = [];
        playersArray.map(function (player) {
            return (
                playerGames.push(
                    {'id': player.id,
                    'name': player.name,
                    'gamesPlayed': totalGames(player.id, gamesArray),
                    'totalPoints': totalPoints(player.id, gamesArray)
                    }))
            })
        return playerGames;
    },
    calcHistory: calcHistory
};

module.exports = {
    getAllPlayers: getAllPlayers, 
    helpers: helpers
};

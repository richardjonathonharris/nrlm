var axios = require('axios');

var dbName = 'http://127.0.0.1:8000'

function getAllPlayers (token) {
    var header = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    var request = axios.get(dbName + '/players/', 
        {headers: header}
    )
    return request 
}

function getAllGames (token) {
    var header = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    var request = axios.get(dbName + '/games/', 
        {headers: header}
    )
    return request 
}

function getAllEvents(token) {
    var header = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    var request = axios.get(dbName + '/events/', 
        {headers: header}
    )
    return request 
}

function getAllIdentities(token) {
    var header = {
        'Content-type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    var request = axios.get(dbName + '/identities/', 
        {headers: header}
    )
    return request 
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
            if (obj.player === playerId) {
                return acc + obj.points
            }
            else if (obj.played_against_player === playerId) {
                return acc + obj.played_against_points
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

    games.map(function (game) {
        return (
            history.push(
                {'id': game.id,
                'player1': playerLookup[game.player].name,
                'player2': playerLookup[game.played_against_player].name,
                    'points1': game.points, 
                    'points2': game.played_against_points,
                    'identity1': identitiesLookup[game.identity].name,
                    'identity2': identitiesLookup[game.played_against_identity].name,
                    'event': eventsLookup[game.event].name,
                    'round': game.round_num
                }
            )
        )
    })
    return history
}

var helpers = {
    getAllPlayersData: function (token) {
        return axios.all([getAllPlayers(token), getAllGames(token), getAllIdentities(token), getAllEvents(token)])
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

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

var helpers = {
    getAllPlayersData: function () {
        return axios.all([getAllPlayers(), getAllGames(), getAllIdentities(), getAllEvents()])
            .then(function (arr) {
                return {
                    'players': arr[0].data.results,
                    'games': arr[1].data.results,
                    'identities': arr[2].data.results,
                    'events': arr[3].data.results
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
    }
};

module.exports = {
    getAllPlayers: getAllPlayers, 
    helpers: helpers
};

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
            if (obj.runner === playerId || obj.corp === playerId) {
                return acc + 1
            } else
                return acc
        }, 0)
    )
}

function totalPoints (playerId, gamesArray) {
    return (
        gamesArray.reduce(function (acc, obj) {
            if (obj.runner === playerId) {
                return acc + obj.r_points
            }
            else if (obj.corp === playerId) {
                return acc + obj.c_points
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
                'runner': playerLookup[game.runner].name,
                'corp': playerLookup[game.corp].name,
                    'r_points': game.r_points, 
                    'c_points': game.c_points,
                    'r_identity': identitiesLookup[game.r_identity].name,
                    'c_identity': identitiesLookup[game.c_identity].name,
                    'r_faction': identitiesLookup[game.r_identity].faction,
                    'c_faction': identitiesLookup[game.c_identity].faction,
                    'event': eventsLookup[game.event].name,
                    'round': game.round_num
                }
            )
        )
    })
    return history
}

function getIds () {
    var endpoint = 'https://netrunnerdb.com/api/2.0/public/cards'
    var request = axios.get(endpoint)
    return request
}

var helpers = {
    getIds: getIds,
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

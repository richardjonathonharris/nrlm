import AuthService from './AuthService';
import withAuth from './withAuth';
import { BootstrapTable, TableHeaderColumn } from 'react-bootstrap-table';

require('../../node_modules/react-bootstrap-table/dist/react-bootstrap-table-all.min.css')

const Auth = new AuthService();

var React = require('react');
var axios = require('axios');
var helpers = require('../api/Api').helpers;

class AddMatch extends React.Component {
    constructor (props) {
        super(props)
        this.state = {
            runner: '',
            corp: '',
            ids: null,
            runner_id: '',
            corp_id: '',
        };
        this.handleRunnerSelection = this.handleRunnerSelection.bind(this)
        this.handleCorpSelection = this.handleCorpSelection.bind(this)
        this.handleRunnerIdSelection = this.handleRunnerIdSelection.bind(this)
        this.handleCorpIdSelection = this.handleCorpIdSelection.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    componentDidMount() {
        helpers.getIds()
            .then(resp => {
                this.setState({
                    ids: resp.data.data.filter(function (card) {
                        return card.type_code === 'identity'
                    })
                })
            })
    }
    handleRunnerSelection (event) {
        this.setState({runner: event.target.value})
    }

    handleCorpSelection (event) {
        this.setState({corp: event.target.value})
    }

    handleRunnerIdSelection (event) {
        this.setState({runner_id: event.target.value})
    }

    handleCorpIdSelection (event) {
        this.setState({corp_id: event.target.value})
    }

    handleSubmit (event) {
        // We'll want an event here to see if we have the nrdb entry included and if not, to add it before sending
        // We'll also want an event here to see if we have an actual event to add this to
        // What do we do with Byes?
        event.preventDefault()
    }

    render () {
        return (
            <div>
                <h1>Add Match Class Here</h1>
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Runner Player: 
                        <select value={this.state.runner} onChange={this.handleRunnerSelection}>
                            {this.props.players.map(function (player) {
                                return <option key={player.id} value={player.id}> {player.name} </option>
                            })}
                        </select>
                    </label>
                    <label>
                        Corp Player:
                        <select value={this.state.corp} onChange={this.handleCorpSelection}>
                            {this.props.players.map(function (player) {
                                return <option key={player.id} value={player.id}> {player.name} </option>
                            })}
                        </select>
                    </label>
                    <br />
                    <label>
                        Runner ID:
                        <select value={this.state.runner_id} onChange={this.handleRunnerIdSelection}>
                            {!this.state.ids 
                                ? <option> Loading... </option>
                                : this.state.ids.filter(function (ids) {
                                return ids.side_code === 'runner'
                            }).map(function (card) {
                                return <option key={card.code} value={card.code}> {card.title} </option>
                            })}
                        </select>
                    </label>
                    <label>
                        Corp ID:
                        <select value={this.state.corp_id} onChange={this.handleCorpIdSelection}>
                            {!this.state.ids
                                ?<option> Loading... </option>
                                : this.state.ids.filter(function (ids) {
                                    return ids.side_code === 'corp'
                                }).map(function (card) {
                                    return <option key={card.code} value={card.code}> {card.title} </option>
                                })}
                        </select>
                    </label>
                    <input type='submit' value ='submit'/>
                </form>
            </div>
        );
    }
}

class DisplayLeaderboard extends React.Component {
    constructor(props) {
        super(props);
        this.options = {
            defaultSortName: 'totalPoints',
            defaultSortOrder: 'desc'
        };
    }
    render () {
        var leaderboard = helpers.calcLeaderboard(this.props.players, 
            this.props.games);
        return (
                <div>
                    <BootstrapTable data={leaderboard} 
                        bordered={false}
                        striped
                        hover={true}
                        condensed
                        multiColumnSort = {3}
                        options={this.options}
                    >
                        <TableHeaderColumn isKey
                            dataField='name'
                            width='400'
                            dataAlign='left'
                            headerAlign='left'
                            dataSort = {true}
                        >Player
                        </TableHeaderColumn>
                        <TableHeaderColumn 
                            dataField='gamesPlayed'
                            width='100'
                            dataAlign='center'
                            headerAlign='center'
                            dataSort= {true}
                        >Games Played
                        </TableHeaderColumn>
                        <TableHeaderColumn 
                            dataField='totalPoints'
                            width='100'
                            dataAlign='center'
                            headerAlign='center'
                            dataSort={true}
                        >Total Points
                        </TableHeaderColumn>
                    </BootstrapTable>
                </div>
            );
    }
}

class DisplayHistory extends React.Component {
    constructor(props) {
        super(props)
        this.options = {
            defaultSortName: 'totalPoints',
            defaultSortOrder: 'desc'
        };
    }
    corpHandler (fieldValue, row, rowIdx, colIdx) {
        var corps = ['haas-bioroid', 'jinteki', 'nbn', 'weyland-consortium'];
        if (corps.includes(rowIdx.c_faction)) {
            return 'faction' + rowIdx.c_faction
        }
        else {
            return 'faction'
        }
    }
    runnerHandler (fieldValue, row, rowIdx, colIdx) {
        var runners = ['anarch', 'shaper', 'criminal',
            'adam', 'sunny-lebeau', 'apex'
        ];
        if (runners.includes(rowIdx.r_faction)) {
            return 'faction' + rowIdx.r_faction
        }
        else {
            return 'faction'
        }
    }
    render () {
        var history = helpers.calcHistory(this.props.games, 
            this.props.players, 
            this.props.identities, 
            this.props.events);
        return (
                <div>
                    <BootstrapTable data={history} 
                        bordered={false}
                        striped
                        hover
                        condensed
                        multiColumnSort = {3}
                    >
                    <TableHeaderColumn
                        dataField='id'
                        isKey
                        hidden={true}
                    >Id
                    </TableHeaderColumn>
                    <TableHeaderColumn
                        dataField='runner'
                    >Runner
                    </TableHeaderColumn>
                    <TableHeaderColumn
                        dataField='r_points'
                    >Runner Points
                    </TableHeaderColumn>
                    <TableHeaderColumn
                        dataField='c_points'
                    >Corp Points
                    </TableHeaderColumn>
                    <TableHeaderColumn
                        dataField='corp'
                    >Corp
                    </TableHeaderColumn>
                    <TableHeaderColumn
                        dataField='r_identity'
                        columnClassName={this.runnerHandler.bind(this)}
                    >Runner ID
                    </TableHeaderColumn>
                    <TableHeaderColumn
                        dataField='c_identity'
                        columnClassName={this.corpHandler.bind(this)}
                    >Corp ID
                    </TableHeaderColumn>
                    <TableHeaderColumn
                        dataField='event'
                    >Event
                    </TableHeaderColumn>
                    <TableHeaderColumn
                        dataField='round'
                    >Round
                    </TableHeaderColumn>
                    </BootstrapTable>
                </div>
        )
    }
}

function DisplayAll (props) {
    return (
        <div className='text-container'>
            <AddMatch 
                players={props.data.players.results}
            />
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

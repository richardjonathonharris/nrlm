import Bar from './components/Bar';
import React from 'react';
import ReactDOM from 'react-dom';

require('./index.css');
require('../node_modules/react-bootstrap-table/dist/react-bootstrap-table-all.min.css')


ReactDOM.render(
    <Bar />,
    document.getElementById('root')
);

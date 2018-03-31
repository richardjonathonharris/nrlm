import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

var numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];


class App extends Component {
  render() {
    return (
      <div className="App">
          <p>I have tried something new! Look, here is my new message!</p>
          {numbers.map((number) =>
              <li key={number}>{number} is a number! </li>
          )}
      </div>
    );
  }
}

export default App;

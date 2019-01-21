import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

const APIURL = window.location.pathname.replace('/db_table', '')
ReactDOM.render(<App url={APIURL}/>, document.getElementById('root'));

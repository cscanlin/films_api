import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';

const API_URL = window.location.pathname.replace('/db_table', '')
ReactDOM.render(<App url={API_URL}/>, document.getElementById('root'));

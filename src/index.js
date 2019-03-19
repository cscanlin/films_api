import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';
import DBTable from './db_table/DBTable.js'
import { loadOpenAPI3Metadata } from './db_table/utils.js'

const APIUrl = window.location.pathname.replace('/db_table', '')

ReactDOM.render(
  <DBTable
    APIUrl={APIUrl}
    loadMetadata={() => loadOpenAPI3Metadata('/api/schema/', APIUrl)}
  />,
  document.getElementById('root')
);

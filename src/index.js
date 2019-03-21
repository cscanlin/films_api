import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';
import DBTable from './db_table/DBTable.js'
import { loadOpenAPI3Metadata, loadSwagger2Metadata } from './db_table/utils.js'

const APIUrl = window.location.pathname.replace('/db_table', '')

ReactDOM.render(
  // loadMetadata={() => loadSwagger2Metadata('/api/swagger.json', APIUrl)}
  <DBTable
    APIUrl={APIUrl}
    loadMetadata={() => loadOpenAPI3Metadata('/api/open_api_schema.json', APIUrl)}
  />,
  document.getElementById('root')
);

import React from 'react'

import './App.css'

import DBTable from './db_table/DBTable.js'

class App extends React.Component {

  render() {
    return <DBTable url='/films/'/>
  }
}

export default App

import React from 'react'
import ReactTable, { ReactTableDefaults } from 'react-table'
import 'react-table/react-table.css'

import './App.css'
import { ArrayCell } from './Cells.js'

const requestData = (urlString, params, pageSize, page, sorted, filtered) => {
  const url = new URL(urlString, window.location.href)
  url.search = new URLSearchParams(params)

  return fetch(url)
    .then((response) => {
        if (response.status >= 400) {
            throw new Error("Bad response from server")
        }
        return response.json()
    })
    .then((response) => ({
        rows: response.results,
        pages: Math.ceil(response.count / pageSize)
      })
    )
}

class App extends React.Component {
  constructor() {
    super()
    this.state = {
      url: '/films/',
      metadata: {},
      data: [],
      pages: null,
      loading: true
    }
    this.loadMetadata = this.loadMetadata.bind(this)
    this.fetchData = this.fetchData.bind(this)
  }

  componentDidMount() {
    this.loadMetadata()
  }

  loadMetadata() {
    return fetch(this.state.url, {method: 'OPTIONS'})
      .then((response) => {
          if (response.status >= 400) {
              throw new Error("Bad response from server")
          }
          return response.json()
      }).then(response => {
        this.setState({ metadata: response })
      })
  }

  getColumns(metadata) {
    let columns = []
    if (Object.keys(metadata).length) {
      columns = metadata.ordered_fields.map((fieldName) => {
        const fieldData = metadata.fields[fieldName]
        const column = {
          Header: fieldData['label'],
          accessor: fieldName,
        }
        if (fieldData.child) {
          column.Cell = (row) => (
            <ArrayCell
              row={row}
              fieldName={fieldName}
              renderArrayItem={(arrayItem) => <p>{arrayItem[fieldData.display_accessor]}</p>}
            />
          )
        }
        return column
      })
    }
    return columns
  }

  fetchData(state, instance) {
    // Whenever the table model changes, or the user sorts or changes pages, this method gets called and passed the current table model.
    // You can set the `loading` prop of the table to true to use the built-in one or show you're own loading bar if you want.
    this.setState({ loading: true })

    let params = {'page': state.page + 1}

    if (state.sorted.length) {
      const sorting = state.sorted[0]
      const sortParams = {'ordering': (sorting.desc ? '-' : '') + sorting.id}
      params = {...params, ...sortParams}
    }
    const filterParams = state.filtered.reduce((filterParams, filterEntry) => (
      { ...filterParams, [`${filterEntry.id}__icontains`]: filterEntry.value }), {}
    )
    params = {...params, ...filterParams}

    requestData(
      this.state.url,
      params,
      state.pageSize,
      state.page,
      state.sorted,
      state.filtered,
    ).then(res => {
      // Now just get the rows of data to your React Table (and update anything else like total pages or loading)
      this.setState({
        data: res.rows,
        pages: res.pages,
        loading: false,
      })
    })
  }

  render() {
    const { metadata, data, pages, loading } = this.state
    return (
      <div>
        <ReactTable
          column={{
            ...ReactTableDefaults.column,
            style: {whiteSpace: 'normal'},
          }}
          columns={this.getColumns(metadata)}
          manual // Forces table not to paginate or sort automatically, so we can handle it server-side
          data={data}
          pages={pages} // Display the total number of pages
          loading={loading} // Display the loading overlay when we need it
          onFetchData={this.fetchData} // Request new data when things change
          filterable
          defaultPageSize={10}
          className='-striped -highlight'
        />
      </div>
    )
  }
}

export default App

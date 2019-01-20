import React from 'react'
import ReactTable from 'react-table'
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
      data: [],
      pages: null,
      loading: true
    }
    this.fetchData = this.fetchData.bind(this)
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
      '/films/',
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
    const { data, pages, loading } = this.state
    return (
      <div>
        <ReactTable
          columns={[
            {
              Header: 'average_score',
              accessor: 'average_score',
            },
            {
              Header: 'description',
              accessor: 'description',
            },
            {
              Header: 'id',
              accessor: 'id',
            },
            {
              Header: 'ratings',
              id: 'ratings',
              Cell: (row) => (
                <ArrayCell
                  row={row}
                  fieldName='ratings'
                  expandable={true}
                  renderArrayItem={(arrayItem) => <p>{arrayItem.score}</p>}
                />
              ),
            },
            {
              Header: 'related_films',
              id: 'related_films',
              Cell: (row) => (
                <ArrayCell
                  row={row}
                  fieldName='related_films'
                  expandable={true}
                  renderArrayItem={(arrayItem) => <p>{arrayItem.title}</p>}
                />
              ),
            },
            {
              Header: 'title',
              accessor: 'title',
            },
            {
              Header: 'url_slug',
              accessor: 'url_slug',
            },
            {
              Header: 'year',
              accessor: 'year',
            },
          ]}
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

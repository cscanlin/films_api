import React from 'react'
import ReactTable, { ReactTableDefaults } from 'react-table'
import 'react-table/react-table.css'

import { ArrayCell } from './Cells.js'
import { DynamicFilter } from './Filters.js'


class DBTable extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      metadata: {},
      data: [],
      pages: null,
      loading: true
    }
    this.fetchData = this.fetchData.bind(this)
  }

  componentDidMount() {
    this.props.loadMetadata().then(metadata => {
      this.setState({ metadata })
    })
  }

  filterParams(filtered) {
    return filtered.reduce((filterParams, filterEntry) => (
      { ...filterParams, [`${filterEntry.value.filterType}`]: filterEntry.value.filterValue }), {}
    )
  }

  orderingParams(sorted) {
    return sorted.map(orderItem => (
      (orderItem.desc ? '-' : '') + orderItem.id
    )).join(',')
  }

  getColumns(metadata) {
    let columns = []
    if (Object.keys(metadata).length) {
      columns = metadata.orderedFields.map((fieldName) => {
        const fieldData = metadata.fields[fieldName]
        const column = {
          Header: fieldData.title,
          id: fieldName,
          accessor: fieldData.displayAccessor
                    ? f => f[fieldName][fieldData.displayAccessor] || JSON.stringify(f[fieldName])
                    : f => JSON.stringify(f[fieldName]),
        }
        console.log(fieldName);
        console.log(fieldData);
        if (fieldData.type === 'array') {
          const renderArrayItem = fieldData.displayAccessor
            ? (arrayItem) => <p>{arrayItem[fieldData.displayAccessor]}</p>
            : undefined
          column.Cell = (row) => (
            <ArrayCell
              row={row}
              fieldName={fieldName}
              renderArrayItem={renderArrayItem}
            />
          )
        }
        if (fieldData.filters) {
          column.Filter = ({ filter, onChange }) => (
            <DynamicFilter
              availableFilters={fieldData.filters.map(param => param.name)}
              filter={filter}
              onChange={onChange}
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

    const params = {...this.filterParams(state.filtered)}

    params.ordering = this.orderingParams(state.sorted)

    params.page = state.page + 1

    const URLWithParams = new URL(this.props.APIUrl, window.location.href)
    URLWithParams.search = new URLSearchParams(params)

    fetch(URLWithParams)
      .then(response => {
        if (response.status >= 400) {
            throw new Error("Bad response from server")
        }
        return response.json()
      }).then(res => {
        this.setState({
          data: res.results,
          pages: Math.ceil(res.results.count / state.pageSize),
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
          }} // FIXME
          columns={this.getColumns(metadata)}
          manual // Forces table not to paginate or sort automatically, so we can handle it server-side
          data={data}
          pages={pages} // Display the total number of pages
          loading={loading} // Display the loading overlay when we need it
          onFetchData={this.fetchData} // Request new data when things change
          filterable // FIXME
          defaultPageSize={10} // FIXME
          className='-striped -highlight'
        />
      </div>
    )
  }
}

export default DBTable

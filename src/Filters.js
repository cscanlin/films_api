// https://github.com/react-tools/react-table/issues/421#issuecomment-320947400

import React from 'react'
import PropTypes from 'prop-types';

const filterTypeDisplayNames = {
  'icontains': 'Contains',
  'gte': '>=',
  'lte': '<=',
}

class DynamicFilter extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      filterType: this.props.availableFilters[0],
      filterValue: ''
    };

    this.filterSelect = this.filterSelect.bind(this);
    this.changeFilterType = this.changeFilterType.bind(this);
    this.changeFilterValue = this.changeFilterValue.bind(this);
  }

  changeFilterType(event) {
    const newState = {
      ...this.state,
      filterType: event.target.value,
    };
    // Update local state
    this.setState(newState);
    // Fire the callback to alert React-Table of the new filter
    this.props.onChange(newState);
  }

  changeFilterValue(event) {
    const newState = {
      ...this.state,
      filterValue: event.target.value,
    };
    // Update local state
    this.setState(newState);
    // Fire the callback to alert React-Table of the new filter
    this.props.onChange(newState);
  }

  filterSelect() {
    const filterTypeOptions = this.props.availableFilters.map(filterType => (
      <option value={filterType}>{filterTypeDisplayNames[filterType]}</option>
    ))
    return (
      <select
         style={{ width: '50%' }}
         value={this.state.filterType}
         onChange={this.changeFilterType}
      >
        {filterTypeOptions}
      </select>
    )
  }

  render() {
    console.log(this.props.filter)
    return (
      <div className="filter">
        {this.filterSelect()}
        <input
          type="text"
          style={{ width: '50%' }}
          value={this.state.filterValue}
          onChange={this.changeFilterValue}
        />
      </div>
    );
  }
}

DynamicFilter.propTypes = {
  availableFilters: PropTypes.arrayOf(PropTypes.string).isRequired,
  // filter: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired,
}

export { DynamicFilter }

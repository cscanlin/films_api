import React from 'react'
import PropTypes from 'prop-types'

class ArrayCell extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      expanded: false,
    }
    this.expandCollapseItems = this.expandCollapseItems.bind(this)
  }

  fieldData() {
    return this.props.row.original[this.props.fieldName]
  }

  expandCollapseItems(e) {
    e.stopPropagation()
    this.setState(state => ({
      expanded: !state.expanded
    }))
  }

  render() {
    console.log(this.props.row);
    const dropdownArrow = this.state.expanded ? '\u25BC' : '\u25C0'
    const dropdownStyle = {
      display: this.fieldData().length && this.props.expandable ? 'inline-block' : 'none',
      float: 'right',
      cursor: 'default',
    }
    const itemContainerStyle = {
      display: this.state.expanded || !this.props.expandable ? 'inline-block' : 'none',
      pointerEvents: 'none',
    }
    return (
      <div>
        <span style={dropdownStyle} onClick={this.expandCollapseItems}>
          {dropdownArrow}
        </span>
        <div style={itemContainerStyle}>
          {this.fieldData().map(this.props.renderArrayItem)}
        </div>
      </div>
    )
  }
}

ArrayCell.propTypes = {
  row: PropTypes.object.isRequired,
  fieldName: PropTypes.string.isRequired,
  expandable: PropTypes.bool.isRequired,
  renderArrayItem: PropTypes.func,
}

ArrayCell.defaultProps = {
  expandable: true,
  renderArrayItem: (arrayItem) => <p>{JSON.stringify(arrayItem)}</p>,
}

export { ArrayCell }

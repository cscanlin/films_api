function loadOpenAPI3Metadata(schemaURL, APIUrl) {
  return fetch(schemaURL)
    .then((response) => {
        if (response.status >= 400) {
            throw new Error("Bad response from server")
        }
        return response.json()
    }).then(data => {
      const parameters = data['paths'][APIUrl]['get']['parameters']
      const schema = data['paths'][APIUrl]['get']['responses']['200']['content']['application/json']['schema']['items']
      const orderedFields = schema['x-orderedFields'] || Object.keys(schema.properties)
      const metadata = {
          orderedFields,
          fields: {},
      }
      orderedFields.forEach(fieldName => {
        metadata['fields'][fieldName] = {
          label: fieldName,
          childFields: schema.properties[fieldName]['x-childFields'],
          displayAccessor: schema.properties[fieldName]['x-displayAccessor'],
          filters: parameters.filter(param => param['x-relatedField'] === fieldName),
        }
      })
      return metadata
    }).catch(error => console.error(error));
}

export { loadOpenAPI3Metadata }

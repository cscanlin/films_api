import $RefParser from 'json-schema-ref-parser'

function loadMetadata(schemaURL, APIUrl, getObjSchema) {
  return fetch(schemaURL)
    .then((response) => {
        if (response.status >= 400) {
            throw new Error("Bad response from server")
        }
        return response.json()
    })
    .then(data => $RefParser.dereference(data))
    .then(schema => {
      const parameters = schema['paths'][APIUrl]['get']['parameters']
      const objSchema = getObjSchema(schema)
      const orderedFields = objSchema['x-orderedFields'] || Object.keys(objSchema.properties)

      const metadata = {
          orderedFields,
          fields: {},
      }
      orderedFields.forEach(fieldName => {
        metadata['fields'][fieldName] = {
          ...objSchema.properties[fieldName],
          displayAccessor: objSchema['x-relationsDiplayFields'][fieldName] || null,
          filters: parameters.filter(param => param['x-relatedField'] === fieldName),
        }
      })
      return metadata
    }).catch(error => console.error(error))
}

function loadOpenAPI3Metadata(schemaURL, APIUrl) {
  const getObjSchema = (schema) => (
    schema['paths'][APIUrl]['get']['responses']['200']['content']['application/json']['schema']['items']
  )
  return loadMetadata(schemaURL, APIUrl, getObjSchema)
}

function loadSwagger2Metadata(schemaURL, APIUrl) {
  const schemaPath = APIUrl.replace('/api', '')  // FIXME
  const getObjSchema = (schema) => {
    return schema['paths'][schemaPath]['get']['responses']['200']['schema']['properties']['results']['items']
  }
  return loadMetadata(schemaURL, schemaPath, getObjSchema)
}

export { loadOpenAPI3Metadata, loadSwagger2Metadata }

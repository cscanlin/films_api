import $RefParser from 'json-schema-ref-parser'

function loadOpenAPI3Metadata(schemaURL, APIUrl) {
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
      const objSchema = schema['paths'][APIUrl]['get']['responses']['200']['content']['application/json']['schema']['items']['properties']
      const orderedFields = objSchema['x-orderedFields'] || Object.keys(objSchema)
      const metadata = {
          orderedFields,
          fields: {},
      }
      orderedFields.forEach(fieldName => {
        metadata['fields'][fieldName] = {
          label: fieldName,
          displayAccessor: objSchema[fieldName]['x-displayAccessor'],
          filters: parameters.filter(param => param['x-relatedField'] === fieldName),
        }
      })
      return metadata
    }).catch(error => console.error(error));
}

function loadSwagger2Metadata(schemaURL, APIUrl) {
  return fetch(schemaURL)
    .then((response) => {
        if (response.status >= 400) {
            throw new Error("Bad response from server")
        }
        return response.json()
    })
    .then(data => $RefParser.dereference(data))
    .then(schema => {
      const schemaPath = APIUrl.replace(schema.basePath, '')
      const parameters = schema['paths'][schemaPath]['get']['parameters']
      const objSchema = schema['paths'][schemaPath]['get']['responses']['200']['schema']['properties']['results']['items']['properties']
      const orderedFields = objSchema['x-orderedFields'] || Object.keys(objSchema)
      const metadata = {
          orderedFields,
          fields: {},
      }
      console.log(objSchema)
      orderedFields.forEach(fieldName => {
        metadata['fields'][fieldName] = {
          ...objSchema[fieldName],
          filters: parameters.filter(param => param['x-relatedField'] === fieldName),
        }
      })
      return metadata
    })
    .catch(error => console.error(error));
}

export { loadOpenAPI3Metadata, loadSwagger2Metadata }

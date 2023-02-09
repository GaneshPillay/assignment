- Use nodejs lambda function which connects to aws open-search
const AWS = require('aws-sdk');
Api gateway to connect to lambda write a code
const AWS = require('aws-sdk');
const apigateway = new AWS.APIGateway({apiVersion: '2015-07-09'});

exports.handler = async (event) => {
  const params = {
    restApiId: 'YOUR_REST_API_ID',
    resourceId: 'YOUR_RESOURCE_ID',
    httpMethod: 'POST',
    authorizationType: 'NONE',
    authorizerId: '',
    requestParameters: {
      'method.request.header.Content-Type': false
    },
    requestTemplates: {
      'application/json': '{"statusCode": 200}'
    }
  };
  const result = await apigateway.putMethod(params).promise();
  console.log(result);
  return result;
}
- Invoke api exposed by API gateway → which connects with lambda → dumps the
data to opensearch
const AWS = require('aws-sdk');
const opensearch = new AWS.OpenSearch({apiVersion: '2017-12-01'});
const https = require('https');

exports.handler = async (event, context) => {
  // Get data from event
  const data = event.data;

  // Dump the data to Amazon OpenSearch
  const params = {
    DomainName: 'YOUR_OPENSEARCH_DOMAIN_NAME',
    Documents: [
      {
        type: 'add',
        id: '1',
        fields: {
          data: data
        }
      }
    ]
  };
  const result = await opensearch.uploadDocuments(params).promise();
  console.log(result);

  // Send response back to the client
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      message: 'Data successfully dumped to Amazon OpenSearch.'
    })
  };
  return response;
};


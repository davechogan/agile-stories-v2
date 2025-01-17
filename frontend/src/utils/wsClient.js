import { ApolloLink, HttpLink } from '@apollo/client/core'
import { createClient } from 'graphql-ws'
import { GraphQLWsLink } from '@apollo/client/link/subscriptions'

const APPSYNC_API_KEY = 'da2-52givygifzedvj575mknrvmuyu'

export const createWsClient = (endpoint) => {
  // HTTP Link for queries/mutations
  const httpLink = new HttpLink({
    uri: endpoint,
    headers: {
      'x-api-key': APPSYNC_API_KEY
    }
  })

  // WebSocket Link for subscriptions
  const wsLink = new GraphQLWsLink(
    createClient({
      url: endpoint.replace('https://', 'wss://'),
      connectionParams: {
        'x-api-key': APPSYNC_API_KEY,
        'Sec-WebSocket-Protocol': 'graphql-ws'
      },
      on: {
        connected: () => console.log('Connected to AppSync'),
        error: (err) => console.error('WebSocket error:', err)
      }
    })
  )

  // Use HTTP for queries/mutations, WebSocket for subscriptions
  return ApolloLink.split(
    operation => operation.query.definitions.some(
      definition =>
        definition.kind === 'OperationDefinition' &&
        definition.operation === 'subscription'
    ),
    wsLink,
    httpLink
  )
} 
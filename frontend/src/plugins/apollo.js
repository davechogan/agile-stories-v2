import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client/core'
import { createApolloProvider } from '@vue/apollo-option'

const APPSYNC_ENDPOINT = 'https://3ofh5tyjezgfnpqipouj4y5bfi.appsync-api.us-east-1.amazonaws.com/graphql'
const APPSYNC_API_KEY = 'da2-52givygifzedvj575mknrvmuyu'

// HTTP link for queries
const httpLink = new HttpLink({
  uri: APPSYNC_ENDPOINT,
  headers: {
    'x-api-key': APPSYNC_API_KEY
  }
})

// Create Apollo Client
export const apolloClient = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache(),
  defaultOptions: {
    watchQuery: {
      fetchPolicy: 'no-cache'
    }
  }
})

// Create and export Apollo Provider
export const apolloProvider = createApolloProvider({
  defaultClient: apolloClient
}) 
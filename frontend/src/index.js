import React from "react";
import ReactDOM from "react-dom";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import Airports from "./Airports";
import {
  ApolloClient,
  InMemoryCache,
  ApolloProvider,
  HttpLink,
  useQuery,
  gql,
  from,
} from "@apollo/client";
import { onError } from "@apollo/client/link/error";

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors)
    graphQLErrors.forEach(({ message, locations, path }) =>
      console.log(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
      )
    );

  if (networkError) console.log(`[Network error]: ${networkError}`);
});

const customFetch = (uri, options) => {
  const { operationName } = JSON.parse(options.body);
  return fetch(`${uri}/graphql?${operationName}`, options);
};

const client = new ApolloClient({
  cache: new InMemoryCache({ addTypename: false }),
  link: from([
    errorLink,
    new HttpLink({customFetch})
  ]),
});

ReactDOM.render(
  <ApolloProvider client={client}>
    <div>
      <header>
        <div className="navbar navbar-light bg-light box-shadow">
          <div className="container d-flex justify-content-between">
            <strong>SA Flights Tracker</strong>
          </div>
        </div>
      </header>
      <Airports />
    </div>
  </ApolloProvider>,
  document.getElementById("root")
);

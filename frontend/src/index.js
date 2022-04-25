import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import "../node_modules/bootstrap/dist/css/bootstrap.min.css";
import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";
import logo from "./logo.jpeg";
import Search from "./components/Search";

const client = new ApolloClient({
  cache: new InMemoryCache({ addTypename: false }),
  uri: "http://127.0.0.1:8000/graphql",
});

ReactDOM.render(
  <BrowserRouter>
    <ApolloProvider client={client}>
      <div className="container">
        <header>
          <div>
            <a
              href="/"
              className="d-flex align-items-center mb-3 mb-md-0 me-md-auto text-dark text-decoration-none"
            >
              <h1 className="fw-light text-center text-lg-start mt-4 mb-0">
                <img
                  src={logo}
                  className="d-inline-block"
                  width={50}
                  height={50}
                />
                SA Flight Tracker
              </h1>
            </a>
          </div>
          <hr className="mt-2 mb-4" />
        </header>
        <div>
          <Search />
        </div>
      </div>
    </ApolloProvider>
  </BrowserRouter>,
  document.getElementById("root")
);

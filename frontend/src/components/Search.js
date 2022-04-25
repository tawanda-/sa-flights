import { useLazyQuery } from "@apollo/client";
import React, { useState } from "react";
import { getFlights } from "../api";
import App from "../App";
import Flights from "./Flights";

function Search() {
  const [showAdvanceSearch, setShowAdvanceSearch] = useState(false);
  const [search, setSearch] = useState("");
  const [searchOne, setSearchOne] = useState("");
  const [searchTwo, setSearchTwo] = useState("");

  function handleItemClick(e) {
    setShowAdvanceSearch(!showAdvanceSearch);
  }

  function submitSearch(e) {
    switch (e.target.id) {
      case "0":
        searchFlights({ variables: { search: search, b: "", c: "" } });
        break;
      case "1":
        searchFlights({
          variables: { search: "", searchone: searchOne, searchtwo: searchTwo },
        });
        break;
      default:
        break;
    }
  }

  function handleSearch(e) {
    switch (e.target.id) {
      case "0":
        setSearch(e.target.value);
        break;
      case "1":
        setSearchOne(e.target.value);
        break;
      case "2":
        setSearchTwo(e.target.value);
        break;
      default:
        break;
    }
  }

  const [searchFlights, { loading, data }] = useLazyQuery(getFlights);

  return (
    <div className="container">
      <div className="row align-items-top mb-4">
        <div className="col"></div>
        <div className="col-6">
          <div className="input-group mb-3">
            <input
              id="0"
              type="text"
              aria-label="First name"
              className="form-control"
              onChange={handleSearch}
              value={search}
            />
            <button
              id="0"
              className="btn btn-outline-secondary"
              type="button"
              onClick={submitSearch}
            >
              Search
            </button>
          </div>

          <div
            className={showAdvanceSearch ? "input-group" : "d-none input-group"}
          >
            <span className="input-group-text">From</span>
            <input
              id="1"
              type="text"
              className="form-control"
              placeholder="Depart"
              aria-label="Depart"
              onChange={handleSearch}
              value={searchOne}
            />
            <span className="input-group-text">To</span>
            <input
              id="2"
              type="text"
              className="form-control"
              placeholder="Arrive"
              aria-label="Arrive"
              onChange={handleSearch}
              value={searchTwo}
            />
            <button
              id="1"
              className="btn btn-outline-secondary"
              type="button"
              onClick={submitSearch}
            >
              Search
            </button>
          </div>
        </div>

        <div className="col">
          <button
            type="button"
            className="btn btn-outline-secondary"
            onClick={handleItemClick}
          >
            Advanced Search
          </button>
        </div>
      </div>
      {loading ? (
        <p>Loading ...</p>
      ) : data && data.flights ? (
        <Flights flights={data.flights} />
      ) : (
        <App />
      )}
    </div>
  );
}

export default Search;

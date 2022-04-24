import React, { useState } from "react";
import { useQuery } from "@apollo/client";
import { useParams, useLocation, Link } from "react-router-dom";
import Flights from "../components/Flights";
import { getFlights } from "../api";
import Stats from "../components/Stats";

function Airport() {
  const { id } = useParams();
  const location = useLocation();
  const [isActive, setActive] = useState(0);
  const [tab, setTab] = useState(0);
  const headings = ["Departures", "Arrivals", "Airport Stats"];

  function handleItemClick(e) {
    setActive(e.target.id);
    setTab(e.target.id);
  }

  const { loading, error, data } = useQuery(getFlights, {
    variables: { search: id },
  });

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  const dep = Object.keys(data.flights).reduce(function (dep, key) {
    if (data.flights[key].departure.airport.icaoCode === id) {
      dep[key] = data.flights[key];
    }
    return dep;
  }, {});

  const arr = Object.keys(data.flights).reduce(function (arr, key) {
    if (data.flights[key].arrival.airport.icaoCode === id) {
      arr[key] = data.flights[key];
    }
    return arr;
  }, {});

  return (
    <div className="container">
      <nav aria-label="breadcrumb">
        <ol className="breadcrumb">
          <li className="breadcrumb-item">
            <Link to={"/"}>
              Airports
            </Link>
          </li>
          <li className="breadcrumb-item active">{location.state.airport}</li>
        </ol>
      </nav>
      <nav>
        <ul className="nav nav-tabs">
          {headings.map((item, index) => (
            <li className="nav-item" index={index} key={index}>
              <a
                id={index}
                className={index == isActive ? "nav-link active" : "nav-link"}
                onClick={handleItemClick}
              >
                {item}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      <Tabs tab={tab} dep={dep} arr={arr} />
    </div>
  );
}

function Tabs(props) {
  switch (props.tab) {
    case "0":
      return <Flights flights={props.dep} />;
    case "1":
      return <Flights flights={props.arr} />;
    case "2":
      return <Stats />;
    default:
      return <Flights flights={props.dep} />;
  }
}

export default Airport;

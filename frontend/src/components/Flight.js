import React from "react";
import Item from "./Item";
import Takeoff from "../svg/takeoff.svg";
import Landing from "../svg/landing.svg";
import Inflight from "../svg/inflight.svg";

function Flight(props) {
  const d = new Date(props.flight.date);
  const arrival = {
    airline: "",
    number: "",
    gate: props.flight.arrival.gate
      ? "Gate: " + props.flight.arrival.gate.toUpperCase()
      : "",
    terminal: props.flight.arrival.terminal
      ? "Terminal: " + props.flight.arrival.terminal.toUpperCase()
      : "",
    name: props.flight.arrival.airport.name.toUpperCase(),
    city: props.flight.arrival.airport.city.toUpperCase(),
    country: props.flight.arrival.airport.country.toUpperCase(),
    timeScheduled: props.flight.arrival.timeScheduled,
    date: d.toDateString(),
  };

  const departure = {
    airline: props.flight.airline.toUpperCase(),
    number: props.flight.iataCode,
    gate: props.flight.departure.gate
      ? "Gate: " + props.flight.departure.gate.toUpperCase()
      : "",
    terminal: props.flight.departure.terminal
      ? "Terminal: " + props.flight.departure.terminal.toUpperCase()
      : "",
    name: props.flight.departure.airport.name.toUpperCase(),
    city: props.flight.departure.airport.city.toUpperCase(),
    country: props.flight.departure.airport.country.toUpperCase(),
    timeScheduled: props.flight.departure.timeScheduled,
    date: d.toDateString(),
  };

  return (
    <div
      className="row align-items-center border border-light mb-2 bg-light"
      key={props.index}
    >
      <div className="col">
        <Item data={departure} />
      </div>
      <div className="col">
        <Status status={props.flight.status} />
      </div>
      <div className="col">
        <Item data={arrival} />
      </div>
    </div>
  );
}

function Status(props) {
  switch (props.status) {
    case "cancelled":
      return (
        <div className="row">
          <h5 className="text-center">Cancelled</h5>
        </div>
      );

    case "landed":
      return (
        <div className="row align-items-center">
          <div className="col-10">
            <div className="progress" style={{ height: "5px" }}>
              <div className="progress-bar w-100" role="progressbar"></div>
            </div>
          </div>
          <div className="col-2">
            <img src={Landing} />
          </div>
        </div>
      );

    case "active":
      return (
        <div className="row align-items-center">
          <div className="col-5">
            <div className="progress" style={{ height: "5px" }}>
              <div
                className="progress-bar w-100"
                role="progressbar"
                aria-valuenow="100"
                aria-valuemin="0"
                aria-valuemax="100"
              ></div>
            </div>
          </div>
          <div className="col-2">
            <img src={Inflight} />
          </div>
          <div className="col-5">
            <div className="progress" style={{ height: "5px" }}>
              <div
                className="progress-bar"
                role="progressbar"
                aria-valuenow="50"
                aria-valuemin="0"
                aria-valuemax="100"
              ></div>
            </div>
          </div>
        </div>
      );

    case "scheduled":
    default:
      return (
        <div className="row align-items-center">
          <div className="col-2">
            <img src={Takeoff} />
          </div>
          <div className="col-10">
            <div className="progress" style={{ height: "5px" }}>
              <div
                className="progress-bar w-0"
                role="progressbar"
                aria-valuenow="0"
                aria-valuemin="0"
                aria-valuemax="100"
              ></div>
            </div>
          </div>
        </div>
      );
  }
}

export default Flight;

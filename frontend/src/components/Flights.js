import React from "react";
import Flight from "./Flight";

function Flights(props) {
  return (
    <div className="container">
      {Object.values( props.flights ).map((flight, index) => (
          <Flight flight={flight} index={flight.number} key={index} />
      ))}
    </div>
  );
}

export default Flights;
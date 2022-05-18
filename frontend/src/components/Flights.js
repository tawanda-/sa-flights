import React from "react";
import Flight from "./Flight";
import NoFlights from "../static/svg/x_airplane.png"

function Flights(props) {
  return (
    <div className="container">
      {props.flights && Object.keys(props.flights).length > 0 ? (
        Object.values(props.flights).map((flight, index) => (
          <Flight flight={flight} index={flight.number} key={index} />
        ))
      ) : (
        <div className="alert alert-light text-center" role="alert">
          <img src={NoFlights} style={{width:"64px"}} alt="no flights"/>
           &nbsp;&nbsp;&nbsp;No flights available.
        </div>
      )}
    </div>
  );
}

export default Flights;
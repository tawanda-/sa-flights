import React, { useState, useEffect } from "react";

import { gql, useQuery } from "@apollo/client";

const getAirports = gql`query{airports{name,municipality,iataCode,latitudeDeg,longitudeDeg,elevation,imageUrl}}`;

function Airports() {
  const { loading, error, data } = useQuery(getAirports);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error :(</p>;

  console.log(data.airports);

  return (
    <div className="album py-5 bg-light">
      <div className="container">
        <div className="row">
          {Object.values(data.airports).map((airport, index) => (
            <div className="col-md-4" key={index}>
              <div className="card mb-4 box-shadow">
                <img
                  className="card-img-top"
                  alt="Thumbnail [100%x225]"
                  style={{ height: "225px", width: "100%", display: "block" }}
                  src={airport.imageUrl}
                  data-holder-rendered="true"
                />
                <div className="card-body">
                  <p className="card-text">{airport.name}</p>
                  <a
                    href="#"
                    className="btn btn-sm btn-outline-secondary stretched-link"
                  >
                    Check Flights
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Airports;

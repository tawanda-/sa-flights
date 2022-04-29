import React from "react";
import { Link } from "react-router-dom";

import { useQuery } from "@apollo/client";
import { getAirports } from "../api";

function Airports() {

  const { loading, error, data } = useQuery(getAirports, {variables:{search:'south africa'},});

  if (loading) return <p>Loading...</p>;

  return (
    <div className="container">
      <div className="row">
        {Object.values(data.airports).filter(ax => ax.imageUrl).map((airport, index) => (
          <div className="col-lg-3 col-md-4 col-6" key={index}>
            <div className="card mb-4 box-shadow d-block">
              <img
                className="card-img-top"
                alt="Thumbnail [100%x200]"
                style={{ height: "200px", width: "100%", display: "block" }}
                src={airport.imageUrl}
                data-holder-rendered="true"
              />
              <div className="card-body">
                <p className="card-text">{airport.name}</p>
                <Link
                  className="btn btn-sm btn-outline-secondary stretched-link"
                  to={`airport/${airport.icaoCode}`}
                  state={{airport:airport.name}}
                >
                  Check Flights
                </Link>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Airports;
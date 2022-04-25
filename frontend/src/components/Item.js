import React from "react";

function Item(props) {
    const item = props.data;
    return (
      <div className="card text-center border-light">
        <div className="card-header">{item.name.toUpperCase()}</div>
        <div className="card-body">
          <h6 className="card-title">
            {item.city.toUpperCase()}, {item.country.toUpperCase()}
          </h6>
          <p className="card-text">{item.date} {item.timeScheduled}</p>
        </div>
        <div className="card-footer text-muted">
          {item.airline.toUpperCase()} {item.number} {item.gate.toUpperCase()}{" "}
          {item.terminal.toUpperCase()}
        </div>
      </div>
    );
  }

  export default Item;
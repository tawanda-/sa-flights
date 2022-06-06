import { gql } from "@apollo/client";

const getAirports = gql`
  query Airports($search: String) {
    airports(search: $search) {
      name
      city
      country
      iataCode
      icaoCode
      imageUrl
    }
  }
`;

const getFlights = gql`
  query Flights($search: String, $searchone: String, $searchtwo: String) {
    flights(search: $search, searchone: $searchone, searchtwo: $searchtwo) {
      number
      iataCode
      icaoCode
      date
      status
      airline
      arrivalGate
      arrivalBaggage
      arrivalTerminal
      arrivalTimeDelay
      arrivalTimeScheduled
      departureGate
      departureBaggage
      departureTerminal
      departureTimeDelay
      departureTimeScheduled
      departureAirport {
        name
        icaoCode
        iataCode
        latitudeDeg
        elevation
        imageUrl
        city
        country
      }
      arrivalAirport {
        name
        icaoCode
        iataCode
        latitudeDeg
        elevation
        imageUrl
        city
        country
      }
    }
  }
`;

export { getAirports, getFlights };

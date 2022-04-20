import { gql } from "@apollo/client";

const getAirports = gql`
    query allAirports($country: String!){
        airports(country:$country){
            name
            city
            country
            iataCode
            icaoCode
            imageUrl
        }
    }
`;

const getAirportsInCountry = gql`
    query airportsInCountry($country: String!){
        airportsInCountry(country:$country){
            name
            city
            country
            iataCode
            icaoCode
            imageUrl
        }
    }
`;

const getAirportFlights = gql`
    query Flights($icao: String!){
        flights(icao:$icao){
            number
            iataCode
            icaoCode
            date
            status
            airline
            departure {
                airport{
                    name
                    city
                    country
                    icaoCode
                }
                terminal
                gate
                baggage
                timeDelay
                timeScheduled
                timeEstimated
                timeActual
                estimatedRunway
                actualRunway
            }
            arrival{
                airport{
                    name
                    city
                    country
                    icaoCode
                }
                terminal
                gate
                baggage
                timeDelay
                timeScheduled
                timeEstimated
                timeActual
                estimatedRunway
                actualRunway
            }
        }
    }
`;

const getArrivals = gql`
    query Arrivals($icao: String!){
        arrivals(icao:$icao){
            number
            iataCode
            icaoCode
            date
            status
            airline
            departure {
                airport{
                    name
                    city
                    country
                }
                terminal
                gate
                baggage
                timeDelay
                timeScheduled
                timeEstimated
                timeActual
                estimatedRunway
                actualRunway
            }
            arrival{
                airport{
                    name
                    city
                    country
                }
                terminal
                gate
                baggage
                timeDelay
                timeScheduled
                timeEstimated
                timeActual
                estimatedRunway
                actualRunway
            }
        }
    }
`;

const getDepartures = gql`
    query Departures($icao: String!){
        departures(icao:$icao){
            number
            iataCode
            icaoCode
            date
            status
            airline
            departure {
                airport{
                    name
                    city
                    country
                }
                terminal
                gate
                baggage
                timeDelay
                timeScheduled
                timeEstimated
                timeActual
                estimatedRunway
                actualRunway
            }
            arrival{
                airport{
                    name
                    city
                    country
                }
                terminal
                gate
                baggage
                timeDelay
                timeScheduled
                timeEstimated
                timeActual
                estimatedRunway
                actualRunway
            }
        }
    }
`;

export {getAirports, getAirportFlights, getAirportsInCountry, getArrivals, getDepartures}
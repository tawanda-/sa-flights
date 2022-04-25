import { gql } from "@apollo/client";

const getAirports = gql`
    query Airports($search: String){
        airports(search:$search){
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
    query Flights($search: String, $searchone: String, $searchtwo:String){
        flights(search:$search, searchone:$searchone, searchtwo:$searchtwo){
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

export {getAirports, getFlights}
import { Airport, Airports } from "./pages";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={<Airports />} />
        <Route path="airport/:id" element={<Airport />} />
      </Routes>
    </div>
  );
}

export default App;

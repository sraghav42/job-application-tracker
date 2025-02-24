import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import AddJobApplication from "./pages/AddJobApplication";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/add-job" element={<AddJobApplication />} />
      </Routes>
    </Router>
  );
}

export default App;

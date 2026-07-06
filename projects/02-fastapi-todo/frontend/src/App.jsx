import Home from "./pages/Home";
import { Routes, Route } from "react-router";
import TodoForm from "./pages/TodoForm";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/new" element={<TodoForm />} />
    </Routes>
  );
}
export default App;

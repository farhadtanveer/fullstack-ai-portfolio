import Home from "./pages/Home";
import { Routes, Route } from "react-router";
import TodoForm from "./pages/TodoForm";
import TodoDetails from "./pages/TodoDetails";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/new" element={<TodoForm />} />
      <Route path="/todo/:id" element={<TodoDetails />} />
      <Route path="/edit/:id" element={<TodoForm />} />
    </Routes>
  );
}
export default App;

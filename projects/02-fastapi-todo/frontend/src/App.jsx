import Home from "./pages/Home";
import { Routes, Route } from "react-router";
import TodoForm from "./pages/TodoForm";
import TodoDetails from "./pages/TodoDetails";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import MainLayout from "./layouts/MainLayout";
import MainProtectedRoutes from "./protectedRoutes/MainProtectedRoutes";

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <MainProtectedRoutes>
            <MainLayout />
          </MainProtectedRoutes>
        }
      >
        <Route path="/" element={<Home />} />
        <Route path="/new" element={<TodoForm />} />
        <Route path="/todo/:id" element={<TodoDetails />} />
        <Route path="/edit/:id" element={<TodoForm />} />
      </Route>

      <Route path="/signup" element={<Signup />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  );
}
export default App;

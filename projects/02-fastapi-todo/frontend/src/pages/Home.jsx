import React, { useState, useEffect } from "react";
import NewTodo from "../components/NewTodo";
import { Link } from "react-router";
import API from "../api/api";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await API.get("/todo");
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await API.delete(`/todo/${id}/delete_todo`);
      fetchData(); // Refresh the todo list after deletion
    } catch (error) {
      console.error("Error deleting todo:", error);
      setError(true);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center text-lg font-medium text-gray-600">
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center text-red-500 font-semibold">
        Error fetching data.
      </div>
    );
  }

  return (
    // Design a todo homepage with a list of todos and a button to add a new todo
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="mx-auto max-w-4xl rounded-xl bg-white p-6 shadow-lg">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-800">Todo List</h1>
          <Link
            to="/new"
            className="rounded-lg bg-blue-500 px-6 py-3 text-white transition hover:bg-blue-600"
          >
            Add New Todo
          </Link>
        </div>
        <div className="flex flex-col gap-4">
          {data.length === 0 ? (
            <p className="text-center text-gray-600">No todos available.</p>
          ) : (
            data.map((todo) => (
              <div
                key={todo.id}
                className="flex items-center justify-between rounded-lg bg-white p-4 shadow-md transition hover:shadow-lg"
              >
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">
                    {todo.title}
                  </h3>
                  <p className="text-gray-600">{todo.description}</p>
                </div>
                <div className="flex gap-2">
                  <Link
                    to={`/edit/${todo.id}`}
                    className="rounded-lg bg-blue-500 px-4 py-2 text-white transition hover:bg-blue-600"
                  >
                    Edit
                  </Link>
                  <button
                    onClick={() => deleteTodo(todo.id)}
                    className="rounded-lg bg-red-500 px-4 py-2 text-white transition hover:bg-red-600"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

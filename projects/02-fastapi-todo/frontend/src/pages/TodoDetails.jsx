import React from "react";
import { useLocation } from "react-router";
import { Link } from "react-router";

const TodoDetails = () => {
  const location = useLocation();
  const todo = location.state?.todo;

  if (!todo) {
    return <div>Todo not found.</div>;
  }

  // show todo details page with title, description and completed status
  return (
    // design a simple card with title, description and completed status
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-lg">
        <div>
          <h1>Title: {todo.title}</h1>
          <p>Description: {todo.description}</p>
          <p>{todo.completed ? <p>Completed</p> : <p>Not Completed</p>}</p>
        </div>
        <div className="mt-4">
          <button
            onClick={() => window.history.back()}
            className="rounded-lg bg-gray-500 px-6 py-3 text-white transition hover:bg-gray-600"
          >
            Back
          </button>
          <Link
            to={`/edit/${todo.id}`}
            state={{ todo: todo }}
            className="ml-4 rounded-lg bg-blue-500 px-6 py-3 text-white transition hover:bg-blue-600"
          >
            Edit
          </Link>
        </div>
      </div>
    </div>
  );
};

export default TodoDetails;

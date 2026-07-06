import axios from "axios";
import React, { useState } from "react";
import { useNavigate } from "react-router";

const TodoForm = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formElement = e.currentTarget;
    const formData = new FormData(formElement);
    const title = formData.get("title");
    console.log(title);

    try {
      await axios.post("http://127.0.0.1:8000/api/todo/new_todo/{id}", {
        title: title,
        description: "", // You can add a description field if needed
        completed: false, // Set completed to false by default
      });
      navigate("/"); // Redirect to the home page after successful submission
    } catch (e) {
      console.error("Error fetching data:", e);
      setError(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-lg">
        <h2 className="mb-6 text-center text-3xl font-bold text-gray-800">
          Add New Todo
        </h2>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label
              htmlFor="title"
              className="mb-2 block text-sm font-medium text-gray-700"
            >
              Title
            </label>

            <input
              type="text"
              id="title"
              name="title"
              placeholder="Enter todo title..."
              className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
            />
          </div>

          <div>
            <label
              htmlFor="description"
              className="mb-2 block text-sm font-medium text-gray-700"
            >
              Description
            </label>

            <input
              type="text"
              id="description"
              name="description"
              placeholder="Enter todo description..."
              className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
            />
          </div>

          <div>
            <label
              htmlFor="completed"
              className="mb-2 block text-sm font-medium text-gray-700"
            >
              Completed
            </label>

            <input
              type="checkbox"
              id="completed"
              name="completed"
              className="rounded border-gray-300 text-blue-500 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 px-4 py-2 font-semibold text-white transition hover:bg-blue-700 active:scale-[0.98]"
          >
            {loading ? "Adding..." : "Add Todo"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default TodoForm;

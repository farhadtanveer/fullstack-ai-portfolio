import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router";
import API from "../api/api";

const TodoForm = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();
  const todo = location.state?.todo;

  const isEditMode = !!todo; // Check if we are in edit mode based on the presence of a todo object

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formElement = e.currentTarget;
    const formData = new FormData(formElement);
    const title = formData.get("title");
    const description = formData.get("description");
    const completed = formData.get("completed") === "on"; // Convert checkbox value to boolean

    try {
      if (isEditMode) {
        await API.put(`/todo/${todo.id}/update_todo`, {
          title: title,
          description: description,
          completed: completed,
        });
      } else {
        await API.post("/todo/new_todo", {
          title: title,
          description: description,
          completed: completed,
        });
      }
      navigate("/"); // Redirect to the home page after successful submission
    } catch (e) {
      console.error("Failed to create Todo!", e);
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
              required
              defaultValue={todo?.title || ""}
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

            <textarea
              id="description"
              name="description"
              placeholder="Enter todo description..."
              className="w-full rounded-lg border border-gray-300 px-4 py-2 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
              defaultValue={todo?.description || ""}
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
              defaultChecked={todo?.completed || false}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-blue-600 px-4 py-2 font-semibold text-white transition hover:bg-blue-700 active:scale-[0.98]"
          >
            {/* if we are in edit mode */}
            {loading ? "Saving..." : isEditMode ? "Update Todo" : "Add Todo"}
          </button>

          {error && (
            <p className="text-sm text-red-600">
              Failed to create Todo. Please try again.
            </p>
          )}
        </form>
      </div>
    </div>
  );
};

export default TodoForm;

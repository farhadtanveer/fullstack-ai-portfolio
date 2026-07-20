import axios from "axios";
import React from "react";

const NewTodo = ({ setData }) => {
  const handleSubmit = async (e) => {
    e.preventDefault();
    // Handle form submission logic here
    // For example, you could send a POST request to your API endpoint
    const formElement = e.currentTarget;
    const formData = new FormData(formElement);
    const title = formData.get("title");
    console.log(title);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/todo/new_todo",
        {
          title: title,
          description: "", // You can add a description field if needed
          completed: false, // Set completed to false by default
        },
      );
      const newTodo = response.data;
      setData((prevData) => [newTodo, ...prevData]);
      // console.log("Todo added:", response.data);
      // Clear the form after successful submission
      formElement.reset();
    } catch (error) {
      console.error("Error adding todo:", error);
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

          <button
            type="submit"
            className="w-full rounded-lg bg-blue-600 px-4 py-2 font-semibold text-white transition hover:bg-blue-700 active:scale-[0.98]"
          >
            Add Todo
          </button>
        </form>
      </div>
    </div>
  );
};

export default NewTodo;

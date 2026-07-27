import React, { useEffect, useState, useParams } from "react";
import { Link } from "react-router";
import API from "../api/api";

const TodoDetails = () => {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await API.get(`/todo/${id}`);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      setData(response.data);
    } catch (e) {
      console.error("Error fetching data:", e);
      setError(e);
    } finally {
      setLoading(false);
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

  if (!data) {
    return (
      <div className="flex min-h-screen items-center justify-center text-lg font-medium text-gray-600">
        No data found.
      </div>
    );
  }

  return (
    // design a simple card with title, description and completed status
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-lg">
        <div>
          <h1>Title: {data?.title}</h1>
          <p>Description: {data?.description}</p>
          <p>{data?.completed ? <p>Completed</p> : <p>Not Completed</p>}</p>
        </div>
        <div className="mt-4">
          <button
            onClick={() => window.history.back()}
            className="rounded-lg bg-gray-500 px-6 py-3 text-white transition hover:bg-gray-600"
          >
            Back
          </button>
          <Link
            to={`/edit/${data?.id}`}
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

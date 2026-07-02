import React, { useState, useEffect } from "react";
import axios from "axios";
import NewTodo from "../components/NewTodo";
import { Link } from "react-router";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await axios.get("http://127.0.0.1:8000/api/todo/");
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setError(true);
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

  return (
    <div className="min-h-screen bg-gray-100 px-4 py-10">
      <div className="mx-auto grid max-w-5xl gap-10 md:grid-cols-2">
        {/* Form Section */}
        {/* <div>
          <NewTodo setData={setData} />
        </div> */}

        <Link
          to="/newTodo"
          className="mb-4 inline-block rounded bg-blue-500 px-4 py-2 text-white transition hover:bg-blue-600"
        >
          Add New Todo
        </Link>

        {/* Todo List Section */}
        <div className="rounded-xl bg-white p-6 shadow-lg">
          <h2 className="mb-4 text-2xl font-bold text-gray-800">Todo List</h2>

          {data.length === 0 ? (
            <p className="text-gray-500">No todos found.</p>
          ) : (
            <ul className="space-y-3">
              {data.map((item) => (
                <li
                  key={item.id}
                  className="rounded-lg border border-gray-200 bg-gray-50 p-3 transition hover:bg-gray-100"
                >
                  <p className="font-medium text-gray-800">{item.title}</p>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

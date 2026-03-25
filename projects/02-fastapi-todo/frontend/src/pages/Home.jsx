import React, { useState } from "react";
import { useEffect } from "react";
import axios from "axios";

export default function Home() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await axios.get("http://127.0.0.1:5000");
      console.log(response.data);
      setData(response.data);
    } catch (error) {
      setError(true);
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div className="">Error fetching data.</div>;
  }

  return (
    <div>
      {data.map((item, index) => (
        <div key={index}>
          <h3>{item.title}</h3>
        </div>
      ))}
    </div>
  );
}

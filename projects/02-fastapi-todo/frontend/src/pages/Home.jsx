import React from "react";
import { useEffect } from "react";
import axios from "axios";

export default function Home() {
  const fetchData = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000");
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);
  return <div>Home</div>;
}

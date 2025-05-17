import React, { useState, useEffect } from "react";
import axios from "axios";

const CustomerInterface = () => {
  // State for form inputs
  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");

  // State for token and queue details
  const [token, setToken] = useState(null);
  const [counter, setCounter] = useState(null);
  const [waitingTime, setWaitingTime] = useState(0);
  const [status, setStatus] = useState("Waiting");

  // State for error handling
  const [error, setError] = useState("");

  // Function to handle token generation
  const generateToken = async () => {
    if (!name || !phone) {
      setError("Please enter your name and phone number.");
      return;
    }

    try {
      // Mock API call to generate token
      const response = await axios.post("/api/customer/register", {
        name,
        phone,
      });

      // Update state with token and counter details
      setToken(response.data.token);
      setCounter(response.data.counter);
      setWaitingTime(response.data.waitingTime);
      setStatus("Waiting");
      setError("");
    } catch (err) {
      setError("Failed to generate token. Please try again.");
      console.error(err);
    }
  };

  // Function to fetch live updates for the token status
  useEffect(() => {
    if (!token) return;

    const fetchTokenStatus = async () => {
      try {
        const response = await axios.get(`/api/queue/status/${counter}`);
        const tokenData = response.data.find((t) => t.token === token);

        if (tokenData) {
          setStatus(tokenData.status);
          setWaitingTime(tokenData.waitingTime);
        }
      } catch (err) {
        console.error("Error fetching token status:", err);
      }
    };

    // Polling for live updates (every 10 seconds)
    const interval = setInterval(fetchTokenStatus, 10000);
    return () => clearInterval(interval);
  }, [token, counter]);

  return (
    <div className="customer-interface">
      <h1>Customer Interface</h1>

      {/* Input Fields */}
      <div className="form-group">
        <input
          type="text"
          placeholder="Enter Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="text"
          placeholder="Enter Phone Number"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
        />
      </div>

      {/* Error Message */}
      {error && <p className="error">{error}</p>}

      {/* Generate Token Button */}
      <button onClick={generateToken}>Generate Token</button>

      {/* Token Details Display */}
      {token && (
        <div className="token-details">
          <h2>Your Token Details</h2>
          <p>Token Number: {token}</p>
          <p>Assigned Counter: {counter}</p>
          <p>Estimated Waiting Time: {waitingTime} minutes</p>
          <p>Status: {status}</p>
        </div>
      )}
    </div>
  );
};

export default CustomerInterface;

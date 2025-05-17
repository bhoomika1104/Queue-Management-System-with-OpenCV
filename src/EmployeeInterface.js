import React, { useState, useEffect } from "react";
import axios from "axios";

const EmployeeInterface = () => {
  // State for counter number input
  const [counterNumber, setCounterNumber] = useState("");

  // State for queue data
  const [queue, setQueue] = useState([]);

  // State for error handling
  const [error, setError] = useState("");

  // Fetch queue data for the specified counter
  const fetchQueue = async () => {
    if (!counterNumber) {
      setError("Please enter a valid counter number.");
      return;
    }

    try {
      // Mock API call to fetch queue data
      const response = await axios.get(`/api/queue/status/${counterNumber}`);
      setQueue(response.data);
      setError("");
    } catch (err) {
      setError("Failed to fetch queue data. Please try again.");
      console.error(err);
    }
  };

  // Update customer status (Completed, Pending, Waiting)
  const updateStatus = async (token, newStatus) => {
    try {
      await axios.put("/api/queue/update", { token, status: newStatus });
      fetchQueue(); // Refresh queue data after update
    } catch (err) {
      setError("Failed to update status. Please try again.");
      console.error(err);
    }
  };

  // Automatically fetch queue data when counter number changes
  useEffect(() => {
    if (counterNumber) {
      fetchQueue();
    }
  }, [counterNumber]);

  return (
    <div className="employee-interface">
      <h1>Employee Interface</h1>

      {/* Counter Number Input */}
      <div className="form-group">
        <input
          type="text"
          placeholder="Enter Counter Number"
          value={counterNumber}
          onChange={(e) => setCounterNumber(e.target.value)}
        />
      </div>

      {/* Error Message */}
      {error && <p className="error">{error}</p>}

      {/* Queue Table */}
      {queue.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Token</th>
              <th>Status</th>
              <th>Waiting Time (mins)</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {queue.map((item) => (
              <tr key={item.token}>
                <td>{item.token}</td>
                <td>{item.status}</td>
                <td>{item.waitingTime}</td>
                <td>
                  <button
                    onClick={() => updateStatus(item.token, "Completed")}
                    className="btn-completed"
                  >
                    Completed
                  </button>
                  <button
                    onClick={() => updateStatus(item.token, "Pending")}
                    className="btn-pending"
                  >
                    Pending
                  </button>
                  <button
                    onClick={() => updateStatus(item.token, "Waiting")}
                    className="btn-waiting"
                  >
                    Waiting
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className="no-data">No queue data available.</p>
      )}
    </div>
  );
};

export default EmployeeInterface;

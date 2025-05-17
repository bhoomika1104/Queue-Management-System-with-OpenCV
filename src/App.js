import React from "react";
import CustomerInterface from "./CustomerInterface";
import EmployeeInterface from "./EmployeeInterface";
import "./App.css";

function App() {
  return (
    <div className="app">
      <h1>Smart Queue Management System</h1>
      <div className="interfaces">
        <CustomerInterface />
      </div>
    </div>
  );
}

export default App;

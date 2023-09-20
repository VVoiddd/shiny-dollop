import React, { useState } from 'react';
import './App.css';

function App() {
  const [key, setKey] = useState("");
  const [validated, setValidated] = useState(null);

  const generateKey = async () => {
    const response = await fetch('/generate', { method: 'POST' });
    const data = await response.json();
    setKey(data.key);
  }

  const validateKey = async () => {
    const response = await fetch('/validate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ key })
    });
    const data = await response.json();
    setValidated(data.valid);
  }

  return (
    <div className="App">
      <button onClick={generateKey}>Generate Key</button>
      <input value={key} onChange={e => setKey(e.target.value)} placeholder="Enter key" />
      <button onClick={validateKey}>Validate Key</button>
      {validated !== null && <p>Key is {validated ? "Valid" : "Invalid"}</p>}
    </div>
  );
}

export default App;

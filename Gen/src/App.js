
import React, { useState, useEffect } from 'react';

function App() {
    const [keys, setKeys] = useState([]);
    const [selectedKey, setSelectedKey] = useState("");
    const [keyLength, setKeyLength] = useState(8);
    const [useUppercase, setUseUppercase] = useState(true);
    const [useLowercase, setUseLowercase] = useState(true);
    const [useNumbers, setUseNumbers] = useState(true);
    const [useSpecial, setUseSpecial] = useState(false);
    const [newKey, setNewKey] = useState("");

    useEffect(() => {
        fetchKeys();
    }, []);

    const fetchKeys = async () => {
        const response = await fetch('/keys');
        const data = await response.json();
        setKeys(data.keys);
    }

    const handleGenerateKey = async () => {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                length: keyLength,
                useUppercase,
                useLowercase,
                useNumbers,
                useSpecial
            })
        });
        const data = await response.json();
        setNewKey(data.key);
        fetchKeys();
    }

    const handleExtendKeyTime = async (key) => {
        await fetch('/extend/' + key, { method: 'POST' });
        fetchKeys();
    }

    const handleRemoveKeyTime = async (key) => {
        await fetch('/remove-time/' + key, { method: 'POST' });
        fetchKeys();
    }

    const handleDeleteKey = async (key) => {
        await fetch('/delete/' + key, { method: 'DELETE' });
        fetchKeys();
    }

    return (
        <div className="App">
            {/* Key Generation */}
            <h2>Key Generation</h2>
            <div>
                Key Length: <input type="number" value={keyLength} onChange={(e) => setKeyLength(e.target.value)} />
                <br />
                Use Uppercase: <input type="checkbox" checked={useUppercase} onChange={(e) => setUseUppercase(e.target.checked)} />
                <br />
                Use Lowercase: <input type="checkbox" checked={useLowercase} onChange={(e) => setUseLowercase(e.target.checked)} />
                <br />
                Use Numbers: <input type="checkbox" checked={useNumbers} onChange={(e) => setUseNumbers(e.target.checked)} />
                <br />
                Use Special Characters: <input type="checkbox" checked={useSpecial} onChange={(e) => setUseSpecial(e.target.checked)} />
                <br />
                <button onClick={handleGenerateKey}>Generate Key</button>
                <br />
                Generated Key: {newKey}
            </div>

            {/* Key Management */}
            <h2>Key Management</h2>
            <div>
                <select value={selectedKey} onChange={(e) => setSelectedKey(e.target.value)}>
                    {keys.map(keyObj => <option key={keyObj.key} value={keyObj.key}>{keyObj.key} (Expiry: {keyObj.expiry})</option>)}
                </select>
                <br />
                <button onClick={() => handleExtendKeyTime(selectedKey)}>Extend Key Time</button>
                <button onClick={() => handleRemoveKeyTime(selectedKey)}>Remove Key Time</button>
                <button onClick={() => handleDeleteKey(selectedKey)}>Delete Key</button>
            </div>
        </div>
    );
}

export default App;

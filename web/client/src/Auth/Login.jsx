import { useState } from 'react';

import './Login.css';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [msg, setMsg] = useState('');

  const handleSubmit = async () => {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    console.log('Login response:', response);
    if (!response.ok) {
      setMsg('Incorrect username or password');
    }
    window.location.href = '/';
  };
  return (
    <div className="card">
      <h2>Sign in to your account</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            placeholder="Email or username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <br />
        <button type="submit">Sign In</button>
        <div className="hrLine">
          <hr />
          <span>or</span>
          <hr />
        </div>
        <button type="submit">Register new account</button>
        {msg && <p style={{ color: 'red' }}>{msg}</p>}
      </form>
    </div>
  );
};

export { LoginForm };

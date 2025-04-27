'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:8000/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        throw new Error('Invalid login');
      }

      const data = await response.json();

      if (data.role === 'admin') {
        router.push('/admin');
      } else if (data.role === 'user') {
        router.push('/user');
      } else {
        setError('Invalid username or password');
      }
    } catch (err) {
      setError('Login failed. Please check your credentials.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-300">
      <h1 className="text-3xl text-blue-500 font-extrabold mb-15">Vending Machine</h1>
      <h1 className="text-3xl text-blue-500 font-bold mb-6">Login</h1>

      <form onSubmit={handleLogin} className="bg-white p-6 rounded-lg shadow-md w-80">
        <div className="mb-4">
          <label className="block text-blue-500 mb-1 font-semibold">Username</label>
          <input
            type="text"
            className="w-full border text-blue-500 rounded px-3 py-2"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="mb-6">
          <label className="block mb-1 text-blue-500 font-semibold">Password</label>
          <input
            type="password"
            className="w-full border text-blue-500 rounded px-3 py-2"
            value={password || "" }
            onChange={(e) => setPassword(e.target.value)}
            
          />
        </div>

        {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

        <button
          type="submit"
          className="w-full bg-blue-500 text-white font-bold py-2 rounded hover:bg-blue-600"
        >
          Login
        </button>
      </form>
    </div>
  );
}

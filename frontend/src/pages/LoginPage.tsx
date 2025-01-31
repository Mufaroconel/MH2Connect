import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { School, AlertCircle } from "lucide-react";
import { authService } from "../services/authService";

export default function LoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState(""); // Changed from email to username
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      await authService.login(username, password); // Changed from email to username
      navigate("/students");
    } catch (err) {
      setError("Invalid username or password"); // Updated error message
    } finally {
      setIsLoading(false);
    }
  };

  const testConnection = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/test`);
      const data = await response.json();
      console.log("Connection test:", data);
      alert("Backend connection successful!");
    } catch (error) {
      console.error("Connection test failed:", error);
      alert("Backend connection failed!");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex items-center justify-center gap-3 mb-8">
          <School className="w-12 h-12 text-emerald-600" />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Mufakose 2</h1>
            <p className="text-sm text-gray-600">Secondary School</p>
          </div>
        </div>

        <div className="bg-white py-8 px-4 shadow-lg sm:rounded-lg sm:px-10">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Admin Login
          </h2>

          {error && (
            <div className="mb-4 flex items-center gap-2 text-red-600 bg-red-50 p-3 rounded-md">
              <AlertCircle className="w-5 h-5" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label
                htmlFor="username"
                className="block text-sm font-medium text-gray-700"
              >
                Username
              </label>
              <input
                id="username"
                type="text" // Changed from email to text
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-emerald-500 focus:outline-none focus:ring-emerald-500"
              />
            </div>

            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-emerald-500 focus:outline-none focus:ring-emerald-500"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Signing in..." : "Sign in"}
            </button>
          </form>
        </div>
      </div>

      <div className="mt-4 text-center">
        <button
          onClick={testConnection}
          className="text-sm text-emerald-600 hover:text-emerald-500"
        >
          Test Backend Connection
        </button>
      </div>
    </div>
  );
}

import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";

import { login } from "../store/slices/authSlice";

import type { AppDispatch } from "../store";

export function LoginPage() {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();

  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(e: React.SubmitEvent) {
    e.preventDefault();

    try {
      setIsLoading(true);

      const result = await dispatch(
        login({
          identifier,
          password,
        }),
      );

      if (login.fulfilled.match(result)) {
        setSuccess("Login Successful");
        navigate("/");
      } else {
        setError("Invalid credentials");
      }
    } catch (error: any) {
      const backendErrors = error.response?.data;

      if (backendErrors) {
        const message = Object.values(backendErrors).flat().join(" ");
        setError(message);
      } else {
        setError("Unexpected error");
      }
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center px-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-zinc-900 rounded-2xl p-8 space-y-5"
      >
        <div className="space-y-2">
          <h1 className="text-4xl font-bold text-white">Login</h1>

          <p className="text-zinc-400">Enter your account</p>
        </div>

        {error && (
          <div className="bg-red-500/10 text-center border border-red-500 text-red-400 p-3 rounded-lg">
            {error}
          </div>
        )}

        {success && (
          <div className="bg-green-500/10 text-center border border-green-500 text-green-400 p-3 rounded-lg">
            {success}
          </div>
        )}

        <input
          id="username-email"
          type="text"
          placeholder="Your Username or E-mail"
          required
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          className="w-full bg-zinc-800 rounded-lg p-3 text-white"
        />

        <input
          id="password"
          type="password"
          placeholder="Password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full bg-zinc-800 rounded-lg p-3 text-white"
        />

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 disabled:opacity-50 hover:bg-blue-700 transition p-3 rounded-lg text-white font-semibold"
        >
          Login
        </button>

        <Link
          to="/register"
          className="block text-center text-zinc-400 hover:text-white transition"
        >
          Create an account
        </Link>
      </form>
    </div>
  );
}

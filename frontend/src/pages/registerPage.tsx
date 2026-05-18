import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

import { authService } from "../services/authService";
import { validateBirthDate } from "../utils/validateBirthDate";

export function RegisterPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    email: "",
    birth_date: "",
    password: "",
    password_confirm: "",
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function handleSubmit(e: React.SubmitEvent) {
    e.preventDefault();

    if (!validateBirthDate(form.birth_date)) {
      return setError("Type a valid date");
    }

    try {
      setIsLoading(true);

      await authService.register(form);

      setSuccess("Register Successful");
      navigate("/login");
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
          <h1 className="text-4xl font-bold text-white">Register</h1>

          <p className="text-zinc-400">Create your account</p>
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
          id="username"
          type="text"
          required
          placeholder="Username"
          value={form.username}
          onChange={(e) =>
            setForm({
              ...form,
              username: e.target.value,
            })
          }
          className="w-full bg-zinc-800 rounded-lg p-3 text-white"
        />

        <input
          id="email"
          type="email"
          required
          placeholder="E-mail"
          value={form.email}
          onChange={(e) =>
            setForm({
              ...form,
              email: e.target.value,
            })
          }
          className="w-full bg-zinc-800 rounded-lg p-3 text-white"
        />

        <input
          id="birth-date"
          type="date"
          value={form.birth_date}
          onChange={(e) => setForm({ ...form, birth_date: e.target.value })}
          className="w-full bg-zinc-800 rounded-lg p-3 text-white"
        />

        <input
          id="password"
          type="password"
          required
          placeholder="Password"
          value={form.password}
          onChange={(e) =>
            setForm({
              ...form,
              password: e.target.value,
            })
          }
          className="w-full bg-zinc-800 rounded-lg p-3 text-white"
        />

        <input
          id="password-confirm"
          type="password"
          required
          placeholder="Confirm your password"
          value={form.password_confirm}
          onChange={(e) =>
            setForm({
              ...form,
              password_confirm: e.target.value,
            })
          }
          className="w-full bg-zinc-800 rounded-lg p-3 text-white"
        />

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-green-600 disabled:opacity-50 hover:bg-green-700 transition p-3 rounded-lg text-white font-semibold"
        >
          Register
        </button>

        <Link
          to="/login"
          className="block text-center text-zinc-400 hover:text-white transition"
        >
          Already have an account?
        </Link>
      </form>
    </div>
  );
}

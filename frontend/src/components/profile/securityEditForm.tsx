import { useState } from "react";
import { useNavigate } from "react-router-dom";

import type { Profile } from "../../types";

import { profileService } from "../../services/profileService";

interface Props {
  profile: Profile;
}

export function SecurityEditForm({ profile }: Props) {
  const navigate = useNavigate();

  const [email, setEmail] = useState(profile.email || "");
  const [password, setPassword] = useState("");
  const [password_confirm, setPasswordConfirm] = useState("");

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const hasChanges =
    email.trim() !== (profile.email || "").trim() || password.trim();

  const cancelChanges = () => {
    setEmail(profile.email!);
    setPassword("");
    setPasswordConfirm("");

    return;
  };

  async function handleSubmit(e: React.SubmitEvent) {
    e.preventDefault();

    try {
      setIsLoading(true);

      await profileService.updateProfile({
        email,
        password,
        password_confirm,
      });

      setError("");
      setSuccess("Credentials updated");

      navigate(`/profile/@${profile.username}`);
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
    <form
      onSubmit={handleSubmit}
      className="bg-zinc-900 rounded-3xl p-8 space-y-6 shadow-xl"
    >
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-bold text-white">Account and Security</h1>

        <p className="text-zinc-400">E-mail and Password</p>
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
        id="email"
        type="email"
        placeholder="New e-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full bg-zinc-800 border border-zinc-700 rounded-xl p-4 text-white"
      />

      <input
        id="password"
        type="password"
        placeholder="New password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full bg-zinc-800 border border-zinc-700 rounded-xl p-4 text-white"
      />

      <input
        id="password-confirm"
        type="password"
        placeholder="Confirm password"
        value={password_confirm}
        onChange={(e) => setPasswordConfirm(e.target.value)}
        className="w-full bg-zinc-800 border border-zinc-700 rounded-xl p-4 text-white"
      />

      <div className="flex gap-4">
        <button
          type="reset"
          disabled={!hasChanges || isLoading}
          onClick={() => cancelChanges()}
          className="w-full bg-zinc-700 hover:bg-zinc-600 cursor-pointer disabled:opacity-50 transition p-4 rounded-xl text-white"
        >
          Cancel changes
        </button>
        <button
          type="submit"
          disabled={!hasChanges || isLoading}
          className="w-full bg-blue-600 cursor-pointer hover:bg-blue-700 disabled:opacity-50 transition p-4 rounded-xl text-white"
        >
          {isLoading ? "Saving..." : "Save security"}
        </button>
      </div>
    </form>
  );
}

import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import type { Profile } from "../../types";

import { profileService } from "../../services/profileService";

import { validateBirthDate } from "../../utils/validateBirthDate";
import { ImageUp } from "lucide-react";

interface Props {
  profile: Profile;
}

export function ProfileEditForm({ profile }: Props) {
  const navigate = useNavigate();

  const [display_name, setDisplayName] = useState(profile.display_name || "");
  const [bio, setBio] = useState(profile.bio || "");
  const [image, setImage] = useState<File | null>(null);
  const [birth_date, setBirthDate] = useState(profile.birth_date || "");

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const previewImage = useMemo(() => {
    if (image) return URL.createObjectURL(image);

    return profile.avatar;
  }, [image, profile]);

  const hasChanges =
    display_name.trim() !== (profile.display_name || "").trim() ||
    bio.trim() !== (profile.bio || "").trim() ||
    birth_date !== profile.birth_date ||
    image !== null;

  const cancelChanges = () => {
    setDisplayName(profile.display_name!);
    setBio(profile.bio!);
    setBirthDate(profile.birth_date!);
    setImage(null);

    return;
  };

  async function handleSubmit(e: React.SubmitEvent) {
    e.preventDefault();

    if (!validateBirthDate(birth_date)) {
      setError("Invalid date");
      return;
    }

    try {
      setIsLoading(true);

      await profileService.updateProfile({
        display_name,
        bio,
        avatar: image,
        birth_date,
      });

      setError("");
      setSuccess("Profile updated");

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
        <h1 className="text-3xl font-bold text-white">Edit Profile</h1>

        <p className="text-zinc-400">Update your public information</p>
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

      <div className="flex flex-col items-center gap-4">
        <div className="relative">
          <img
            src={
              previewImage ||
              "https://placehold.co/160x160/18181b/ffffff?text=Avatar"
            }
            className="w-40 h-40 rounded-full object-cover border-4 border-zinc-800"
          />

          <label
            htmlFor="avatar"
            title="Upload avatar"
            className="absolute bottom-2 right-2 cursor-pointer bg-blue-600 hover:bg-blue-700 transition text-white text-sm px-4 py-2 rounded-xl"
          >
            <ImageUp size={22} />
          </label>

          <input
            hidden
            id="avatar"
            type="file"
            accept="image/*"
            onChange={(e) => setImage(e.target.files?.[0] || null)}
          />
        </div>
      </div>

      <input
        id="display-name"
        value={display_name}
        onChange={(e) => setDisplayName(e.target.value)}
        placeholder="Nome de exibição"
        className="w-full bg-zinc-800 border border-zinc-700 rounded-xl p-4 text-white"
      />

      <textarea
        id="bio"
        value={bio}
        onChange={(e) => setBio(e.target.value)}
        maxLength={500}
        className="w-full min-h-[140px] bg-zinc-800 border border-zinc-700 rounded-xl p-4 text-white resize-none"
      />

      <input
        id="birth-date"
        value={birth_date}
        onChange={(e) => setBirthDate(e.target.value)}
        className="w-full bg-zinc-800 cursor-text border border-zinc-700 rounded-xl p-4 text-white"
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
          className="w-full bg-blue-600 hover:bg-blue-700 cursor-pointer disabled:opacity-50 transition p-4 rounded-xl text-white"
        >
          {isLoading ? "Saving..." : "Save changes"}
        </button>
      </div>
    </form>
  );
}

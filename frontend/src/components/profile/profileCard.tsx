import { useState } from "react";
import { Link } from "react-router-dom";

import type { Profile } from "../../types";

import { formatDate } from "../../utils/formatDate";
import { UserPen } from "lucide-react";

interface Props {
  profile: Profile;
  postsCount: number;
  isOwnProfile: boolean;
  onFollow: () => void;
}

export function ProfileHeader({
  profile,
  postsCount,
  isOwnProfile,
  onFollow,
}: Props) {
  const [selectedAvatar, setSelectedAvatar] = useState<string | null>(null);

  return (
    <div className="bg-zinc-900 rounded-2xl p-6">
      <div className="flex flex-col md:flex-row gap-6 md:items-start">
        <img
          src={
            profile.avatar! ||
            "https://placehold.co/160x160/18181b/ffffff?text=Avatar"
          }
          alt={`@${profile.username}`}
          onClick={() => setSelectedAvatar(profile.avatar!)}
          className="w-28 h-28 rounded-full object-cover cursor-zoom-in"
        />

        <div className="flex-1 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">
                {profile.display_name}
              </h1>
              <h1 className="text-xl py-2 text-white">@{profile.username}</h1>
            </div>

            {isOwnProfile ? (
              <Link
                to="/profile/edit"
                title="Edit profile"
                className="bg-zinc-800 hover:bg-zinc-700 transition px-5 py-2 rounded-lg text-white"
              >
                <UserPen size={26} />
              </Link>
            ) : (
              <button
                onClick={onFollow}
                className={`px-5 py-2 cursor-pointer rounded-lg text-white ${
                  profile.is_following
                    ? "bg-zinc-700 hover:bg-zinc-600"
                    : "bg-blue-600 hover:bg-blue-700"
                }`}
              >
                {profile.is_following ? "Following" : "Follow"}
              </button>
            )}
          </div>

          {profile.bio && (
            <p className="text-zinc-400 mt-2 break-words">{profile.bio}</p>
          )}

          <div className="flex gap-6 text-zinc-300">
            <div>
              <span className="font-bold">{postsCount}</span> posts
            </div>

            <Link to={`/profile/@${profile.username}/followers`}>
              <span className="font-bold">{profile.followers_count}</span>{" "}
              followers
            </Link>

            <Link to={`/profile/@${profile.username}/following`}>
              <span className="font-bold">{profile.following_count}</span>{" "}
              following
            </Link>
          </div>
          <div className="text-zinc-400">
            <p className="text-sl">
              Member since: {formatDate(profile.created_at)}
            </p>
          </div>
        </div>
      </div>

      {selectedAvatar && (
        <div
          onClick={() => setSelectedAvatar(null)}
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
        >
          <img
            src={selectedAvatar}
            alt=""
            className="max-w-full max-h-full rounded-xl object-contain cursor-zoom-out"
          />
        </div>
      )}
    </div>
  );
}

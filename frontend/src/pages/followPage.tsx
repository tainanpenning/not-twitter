import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { Navbar } from "../components/layout/navbar";
import { FollowList } from "../components/profile/followList";

import { profileService } from "../services/profileService";

import type { Profile } from "../types";
import { ArrowLeft } from "lucide-react";

export function FollowPage() {
  const { username, type } = useParams();
  const normalizedUsername = username?.replace("@", "");
  const [users, setUsers] = useState<Profile[]>([]);

  const isFollowers = type === "followers";

  const loadUsers = useCallback(async () => {
    if (!normalizedUsername) return;

    try {
      const data = isFollowers
        ? await profileService.getFollowers(normalizedUsername)
        : await profileService.getFollowing(normalizedUsername);

      setUsers(data.results);
    } catch (error) {
      console.error(error);
    }
  }, [normalizedUsername, isFollowers]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadUsers();
  }, [loadUsers]);

  return (
    <div className="min-h-screen bg-zinc-950">
      <Navbar />

      <div className="max-w-2xl mx-auto px-4 py-6 space-y-6">
        <h1 className="flex items-center gap-2 text-3xl font-bold text-white">
          <Link
            to={`/profile/@${normalizedUsername}`}
            className="hover:underline"
          >
            <ArrowLeft size={28} />
          </Link>
          {isFollowers ? "Followers" : "Following"}
        </h1>

        {users.length === 0 && (
          <p className="text-center text-zinc-400 p-4">
            {isFollowers
              ? "You don't have followers"
              : "You don't follow any account"}
          </p>
        )}

        <FollowList users={users} />
      </div>
    </div>
  );
}

import { Link } from "react-router-dom";

import type { Profile } from "../../types";

interface Props {
  users: Profile[];
}

export function FollowList({ users }: Props) {
  return (
    <div className="space-y-4">
      {users.map((user) => (
        <Link
          key={user.id}
          to={`/profile/@${user.username}`}
          className="bg-zinc-900 rounded-2xl p-4 flex items-center gap-4 hover:bg-zinc-800 transition"
        >
          <img
            src={
              user.avatar || "https://placehold.co/160x160/18181b/ffffff?text=?"
            }
            className="w-14 h-14 rounded-full object-cover"
          />

          <div>
            <h2 className="text-white font-semibold">{user.display_name}</h2>
            <h2 className="text-white font-semibold">@{user.username}</h2>
          </div>
        </Link>
      ))}
    </div>
  );
}

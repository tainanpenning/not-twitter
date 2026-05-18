import { useCallback, useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { Link } from "react-router-dom";

import { profileService } from "../../services/profileService";

import type { SearchUser } from "../../types";

interface Props {
  close: () => void;
  position: DOMRect;
}

export function SearchModal({ close, position }: Props) {
  const [search, setSearch] = useState("");
  const [users, setUsers] = useState<SearchUser[]>([]);

  const loadSearch = useCallback(() => {
    if (!search.trim()) {
      setUsers([]);
      return;
    }

    const timeout = setTimeout(async () => {
      const data = await profileService.searchUsers(search);

      setUsers(data.results);
    }, 500);

    return () => {
      clearTimeout(timeout);
    };
  }, [search]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadSearch();
  }, [loadSearch]);

  if (!document.body) {
    return null;
  }

  return createPortal(
    <div onClick={close} className="fixed inset-0 bg-black/30 z-[999]">
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          top: position.bottom + 32,
          left: position.left + position.width,
        }}
        className="fixed -translate-x-1/2 w-90 max-h-100 overflow-y-auto bg-zinc-900 border border-zinc-800 rounded-2xl shadow-xl"
      >
        <input
          id="search"
          type="search"
          placeholder="Search profiles..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-zinc-800 rounded-xl px-4 py-3 text-white border-2 border-zinc-800 outline-none focus:border-zinc-400"
        />
        {users.length === 0 ? (
          <div className="p-4 text-zinc-400 text-center">No users found</div>
        ) : (
          users.map((user) => (
            <Link
              key={user.id}
              to={`/profile/@${user.username}`}
              onClick={() => {
                setSearch("");
              }}
              className="flex items-center gap-3 p-4 rounded-2xl hover:bg-zinc-800 transition"
            >
              <img
                src={
                  user.avatar ||
                  "https://placehold.co/80x80/18181b/ffffff?text=?"
                }
                className="w-12 h-12 rounded-full object-cover"
              />

              <div>
                <h3 className="text-white font-medium">{user.display_name}</h3>

                <p className="text-zinc-400">@{user.username}</p>
              </div>
            </Link>
          ))
        )}
      </div>
    </div>,
    document.body,
  );
}

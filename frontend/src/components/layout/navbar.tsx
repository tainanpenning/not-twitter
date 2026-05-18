import { useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";

import type { AppDispatch, RootState } from "../../store/";
import { logout } from "../../store/slices/authSlice";

import { LogOut, Search } from "lucide-react";
import { SearchModal } from "./searchModal";

export function Navbar() {
  const dispatch = useDispatch<AppDispatch>();
  const navigate = useNavigate();

  const currentUser = useSelector((state: RootState) => state.authSlice.user);
  const [isOpen, setIsOpen] = useState(false);

  const searchRef = useRef<HTMLButtonElement>(null);
  const [position, setPosition] = useState<DOMRect | null>(null);

  function handleLogout() {
    dispatch(logout());
    navigate("/login");
  }

  return (
    <header className="border-b border-zinc-800 bg-zinc-950 sticky top-0 z-40">
      <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="text-2xl font-bold text-white">
          Not-Twitter
        </Link>

        <div className="flex items-center">
          <button
            ref={searchRef}
            title="Search profiles"
            onClick={() => {
              if (searchRef.current) {
                setPosition(searchRef.current.getBoundingClientRect());
              }
              setIsOpen((prev) => !prev);
            }}
            className="cursor-pointer text-zinc-300 transition hover:text-zinc-100"
          >
            <Search size={22} />
          </button>
          {isOpen && position && (
            <SearchModal close={() => setIsOpen(false)} position={position} />
          )}
        </div>

        <div className="flex items-center gap-4">
          <Link
            title="Your profile"
            to={`/profile/@${currentUser?.username}`}
            className="text-zinc-300 hover:text-white transition"
          >
            Olá, @{currentUser?.username}
          </Link>

          <button
            title="Logout"
            onClick={handleLogout}
            className="bg-red-600 cursor-pointer hover:bg-red-700 transition px-4 py-2 rounded-lg text-white"
          >
            <LogOut size={20} />
          </button>
        </div>
      </div>
    </header>
  );
}

import { Loader } from "lucide-react";

export function LoadingScreen() {
  return (
    <div className="min-h-screen bg-zinc-950 flex items-center justify-center text-white">
      <Loader size={30} />
    </div>
  );
}

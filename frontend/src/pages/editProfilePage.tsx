import { useEffect, useState, useCallback } from "react";

import { Navbar } from "../components/layout/navbar";
import { LoadingScreen } from "../components/layout/loading";
import { ProfileEditForm } from "../components/profile/profileEditForm";
import { SecurityEditForm } from "../components/profile/securityEditForm";

import { authService } from "../services/authService";
import type { Profile } from "../types";

export function EditProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);

  const loadProfile = useCallback(async () => {
    const data = await authService.getCurrentUser();

    setProfile(data);
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadProfile();
  }, [loadProfile]);

  if (!profile) {
    return <LoadingScreen />;
  }

  return (
    <div className="min-h-screen bg-zinc-950">
      <Navbar />

      <div className="max-w-xl mx-auto px-4 py-8 space-y-6">
        <ProfileEditForm profile={profile} />

        <SecurityEditForm profile={profile} />
      </div>
    </div>
  );
}

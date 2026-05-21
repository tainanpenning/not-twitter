import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { useSelector } from "react-redux";

import { Navbar } from "../components/layout/navbar";
import { ProfileHeader } from "../components/profile/profileCard";
import { PostCard } from "../components/posts/postCard";

import { profileService } from "../services/profileService";
import { followService } from "../services/followService";
import { postService } from "../services/postService";

import type { Profile, Post } from "../types";

import type { RootState } from "../store";
import { LoadingScreen } from "../components/layout/loading";

export function ProfilePage() {
  const currentUser = useSelector((state: RootState) => state.authSlice.user);
  const { username } = useParams();
  const normalizedUsername = username?.replace("@", "");

  const [profile, setProfile] = useState<Profile | null>(null);
  const [posts, setPosts] = useState<Post[]>([]);

  const [loadingFollow, setLoadingFollow] = useState(false);
  const [loading, setLoading] = useState(true);

  const isOwnProfile = currentUser?.username === normalizedUsername;

  const loadProfile = useCallback(async () => {
    if (!normalizedUsername && !currentUser?.username) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);

      const targetUsername = normalizedUsername || currentUser?.username;

      if (!targetUsername) return;

      const [profileData, postsData] = await Promise.all([
        profileService.getProfile(targetUsername),
        postService.getUserPosts(targetUsername),
      ]);

      setProfile(profileData);
      setPosts(postsData);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, [currentUser, normalizedUsername]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadProfile();
  }, [loadProfile]);

  async function handleFollow() {
    if (!normalizedUsername || !profile) return;

    try {
      setLoadingFollow(true);

      await followService.toggleFollow(normalizedUsername);

      setProfile((prev) => {
        if (!prev) return prev;

        return {
          ...prev,
          is_following: !prev.is_following,

          followers_count: prev.is_following
            ? prev.followers_count - 1
            : prev.followers_count + 1,
        };
      });
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingFollow(false);
    }
  }

  if (loading) {
    return <LoadingScreen />;
  }

  if (!profile) {
    return <LoadingScreen />;
  }

  return (
    <div className="min-h-screen bg-zinc-950">
      <Navbar />

      <div className="max-w-3xl mx-auto px-4 py-6 space-y-6">
        <ProfileHeader
          profile={profile}
          postsCount={posts.length}
          isOwnProfile={isOwnProfile}
          onFollow={handleFollow}
          loadingFollow={loadingFollow}
        />

        <div className="space-y-5">
          {posts.length === 0 ? (
            <div className="bg-zinc-900 rounded-2xl p-8 text-center text-zinc-400">
              No posts found.
            </div>
          ) : (
            posts.map((post) => (
              <PostCard
                key={post.id}
                post={post}
                isOwnPost={isOwnProfile}
                onDelete={() =>
                  setPosts((prev) => prev.filter((p) => p.id !== post.id))
                }
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
}

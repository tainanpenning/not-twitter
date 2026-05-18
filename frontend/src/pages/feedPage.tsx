import { useCallback, useEffect, useState } from "react";

import { Navbar } from "../components/layout/navbar";
import { CreatePostForm } from "../components/posts/createPostForm";
import { PostCard } from "../components/posts/postCard";

import { postService } from "../services/postService";

import type { Post } from "../types";

export function FeedPage() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  const loadFeed = useCallback(async () => {
    try {
      setLoading(true);

      const data = await postService.getFeed();

      setPosts(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadFeed();
  }, [loadFeed]);

  return (
    <div className="min-h-screen bg-zinc-950">
      <Navbar />

      <div className="max-w-2xl mx-auto px-4 py-6 space-y-6">
        <CreatePostForm onPostCreated={loadFeed} />

        {loading ? (
          <div className="text-center text-zinc-400">Loading feed...</div>
        ) : posts.length === 0 ? (
          <div className="bg-zinc-900 rounded-2xl p-8 text-center text-zinc-400">
            Your feed is empty.
          </div>
        ) : (
          posts.map((post) => (
            <PostCard
              key={post.id}
              post={post}
              isOwnPost={false}
              onDelete={() =>
                setPosts((prev) => prev.filter((p) => p.id !== post.id))
              }
            />
          ))
        )}
      </div>
    </div>
  );
}

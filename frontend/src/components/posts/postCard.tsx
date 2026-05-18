import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

import type { Post } from "../../types";

import { likeService, postService } from "../../services/postService";

import { CommentSection } from "./commentSection";

import { timeAgo } from "../../utils/timeAgo";
import { Heart, MessageSquareMore, Trash2 } from "lucide-react";

interface Props {
  post: Post;
  isOwnPost: boolean;
  onDelete: () => void;
}

export function PostCard({ post, isOwnPost, onDelete }: Props) {
  const location = useLocation();
  const profilePath = `/profile/@${post.author_username}`;
  const isCurrentProfile = location.pathname === profilePath;

  const [isLiked, setIsLiked] = useState(post.is_liked);
  const [likes, setLikes] = useState(post.likes_count);
  const [commentsCount, setCommentsCount] = useState(post.comments_count);
  const [showComments, setShowComments] = useState(false);
  const [selectedMedia, setSelectedMedia] = useState<string | null>(null);

  async function handleLike() {
    if (!isLiked) {
      try {
        await likeService.createLike(post.id);

        setLikes((prev) => prev + 1);
        setIsLiked(true);
      } catch (error) {
        console.error(error);
      }
    } else {
      try {
        await likeService.deleteLike(post.id);

        setLikes((prev) => prev - 1);
        setIsLiked(false);
      } catch (error) {
        console.error(error);
      }
    }
  }

  async function handleDelete() {
    if (isOwnPost) {
      try {
        await postService.deletePost(post.id);
        onDelete();
      } catch (error) {
        console.log(error);
      }
    }
  }

  return (
    <div className="bg-zinc-900 rounded-2xl p-5 space-y-5">
      <div className="flex-col">
        <div className="flex items-center justify-between">
          {isCurrentProfile ? (
            <div className="flex items-center gap-3">
              <img
                src={
                  post.author_avatar ||
                  "https://placehold.co/160x160/18181b/ffffff?text=?"
                }
                alt={`@${post.author_username}`}
                className="w-12 h-12 rounded-full object-cover"
              />

              <h2 className="font-semibold text-white">
                {post.author_display_name || `@${post.author_username}`}
              </h2>
              <p className="text-zinc-400">{timeAgo(post.created_at)}</p>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                className="flex items-center gap-3"
                to={`profile/@${post.author_username}`}
              >
                <img
                  src={
                    post.author_avatar ||
                    "https://placehold.co/160x160/18181b/ffffff?text=?"
                  }
                  alt={`@${post.author_username}`}
                  className="w-12 h-12 rounded-full object-cover"
                />

                <h2 className="font-semibold text-white">
                  {post.author_display_name || `@${post.author_username}`}
                </h2>
              </Link>
              <p className="text-zinc-400">{timeAgo(post.created_at)}</p>
            </div>
          )}

          {isOwnPost && (
            <button
              title="Delete post"
              onClick={handleDelete}
              className="bg-red-600 hover:bg-red-700 cursor-pointer transition px-2 py-1 rounded-lg text-white"
            >
              <Trash2 size={20} />
            </button>
          )}
        </div>
      </div>

      <p className="text-zinc-200 p-2 whitespace-pre-wrap">{post.content}</p>

      {post.media && (
        <img
          src={post.media}
          alt=""
          onClick={() => setSelectedMedia(post.media!)}
          className="rounded-xl max-h-[500px] w-auto max-w-full mx-auto object-contain cursor-zoom-in"
        />
      )}

      <div className="flex items-center gap-5">
        <button
          title="Like"
          onClick={handleLike}
          className={`
            flex items-center gap-1 cursor-pointer
            ${
              isLiked
                ? "text-pink-500 hover:text-pink-400 transition"
                : "text-zinc-400 hover:text-white transition"
            }
          `}
        >
          <Heart size={20} /> {likes}
        </button>

        <button
          title="Comments"
          onClick={() => setShowComments((prev) => !prev)}
          className="flex items-center gap-1 text-zinc-400 cursor-pointer hover:text-white transition"
        >
          <MessageSquareMore size={20} /> {commentsCount}
        </button>
      </div>

      {showComments && (
        <CommentSection
          postId={post.id}
          onCommentCreated={() => setCommentsCount((prev) => prev + 1)}
          onCommentDeleted={() => setCommentsCount((prev) => prev - 1)}
        />
      )}

      {selectedMedia && (
        <div
          onClick={() => setSelectedMedia(null)}
          className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
        >
          <img
            src={selectedMedia}
            alt=""
            className="max-w-full max-h-full rounded-xl object-contain cursor-zoom-out"
          />
        </div>
      )}
    </div>
  );
}

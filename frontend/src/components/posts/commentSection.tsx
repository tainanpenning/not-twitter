import { useCallback, useEffect, useState } from "react";
import { useSelector } from "react-redux";

import type { RootState } from "../../store";
import type { Comment } from "../../types";

import { commentService } from "../../services/postService";

import { timeAgo } from "../../utils/timeAgo";
import { Loader, SendHorizontal, Trash2 } from "lucide-react";
import { Link, useLocation } from "react-router-dom";

interface Props {
  postId: number;
  onCommentCreated: () => void;
  onCommentDeleted: () => void;
  onLoadingChange: (isLoading: boolean) => void;
}

export function CommentSection({
  postId,
  onCommentCreated,
  onCommentDeleted,
  onLoadingChange,
}: Props) {
  const currentUser = useSelector((state: RootState) => state.authSlice.user);

  const location = useLocation();
  const profilePath = `/profile/@${currentUser?.username}`;
  const isCurrentProfile = location.pathname === profilePath;

  const [isLoading, setIsLoading] = useState(false);
  const [comments, setComments] = useState<Comment[]>([]);
  const [content, setContent] = useState("");

  const loadComments = useCallback(async () => {
    try {
      setIsLoading(true);
      onLoadingChange(true);

      const data = await commentService.getComments(postId);

      setComments(data);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
      onLoadingChange(false);
    }
  }, [postId, onLoadingChange]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadComments();
  }, [loadComments]);

  async function handleComment(e: React.SubmitEvent) {
    e.preventDefault();

    if (!content.trim()) return;

    try {
      setIsLoading(true);
      const newComment = await commentService.createComment(postId, content);

      setComments((prev) => [newComment, ...prev]);

      setContent("");
      onCommentCreated();
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleDelete(commentId: number) {
    try {
      setIsLoading(true);
      await commentService.deleteComment(commentId);

      setComments((prev) => prev.filter((c) => c.id !== commentId));

      onCommentDeleted();
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="space-y-4 border-t border-zinc-800 pt-4">
      <form onSubmit={handleComment} className="flex gap-3">
        <input
          id="post-comment"
          type="text"
          placeholder="Leave a comment"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          className="flex-1 bg-zinc-800 rounded-lg p-3 text-white"
        />

        <button
          title="Send comment"
          type="submit"
          disabled={content.length === 0 || isLoading}
          className="bg-blue-600 cursor-pointer hover:bg-blue-700 disabled:opacity-50 transition px-4 rounded-lg text-white"
        >
          <SendHorizontal size={30} />
        </button>
      </form>

      <div className="space-y-4">
        {isLoading ? (
          <div className="flex items-center justify-center p-4 text-zinc-400">
            <Loader className="animate-spin mx-auto" size={24} />
          </div>
        ) : comments.length === 0 ? (
          <p className="text-zinc-400 text-center">No comments yet.</p>
        ) : (
          comments.map((comment) => (
            <div key={comment.id} className="flex gap-3">
              {isCurrentProfile ? (
                <img
                  src={
                    comment.author_avatar ||
                    "https://placehold.co/160x160/18181b/ffffff?text=?"
                  }
                  className="w-10 h-10 rounded-full object-cover"
                />
              ) : (
                <Link
                  to={profilePath}
                  className="w-10 h-10 rounded-full object-cover"
                >
                  <img
                    src={
                      comment.author_avatar ||
                      "https://placehold.co/160x160/18181b/ffffff?text=?"
                    }
                    className="w-10 h-10 rounded-full object-cover"
                  />
                </Link>
              )}

              <div className="flex flex-col bg-zinc-800 rounded-xl p-3 flex-1">
                <div className="flex justify-between items-center">
                  <div className="flex gap-2">
                    {isCurrentProfile ? (
                      <h3 className="font-semibold text-white">
                        {comment.author_display_name || comment.author_username}
                      </h3>
                    ) : (
                      <Link to={profilePath}>
                        <h3 className="font-semibold text-white">
                          {comment.author_display_name ||
                            comment.author_username}
                        </h3>
                      </Link>
                    )}
                    <p className="text-zinc-400">
                      {timeAgo(comment.created_at)}
                    </p>
                  </div>

                  {comment.author_username === currentUser?.username && (
                    <button
                      title="Delete comment"
                      onClick={() => handleDelete(comment.id)}
                      disabled={isLoading}
                      className="bg-red-600 cursor-pointer hover:bg-red-700 disabled:cursor-wait transition px-2 py-1 rounded-lg text-white"
                    >
                      <Trash2 size={20} />
                    </button>
                  )}
                </div>
                <p className="text-zinc-200 p-2">{comment.content}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

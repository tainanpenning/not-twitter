import { useEffect, useState } from "react";

import { postService } from "../../services/postService";

import { Ellipsis, ImagePlus, SendHorizontal, X } from "lucide-react";

interface Props {
  onPostCreated: () => void;
}

export function CreatePostForm({ onPostCreated }: Props) {
  const [content, setContent] = useState("");
  const [media, setMedia] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!media) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setPreview(null);
      return;
    }

    const objectUrl = URL.createObjectURL(media);

    setPreview(objectUrl);

    return () => URL.revokeObjectURL(objectUrl);
  }, [media]);

  async function handleSubmit(e: React.SubmitEvent) {
    e.preventDefault();

    if (!content.trim() && !media) return;

    try {
      setIsLoading(true);

      await postService.createPost({
        content,
        media,
      });

      setContent("");
      setMedia(null);
      setPreview(null);

      onPostCreated();
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  }

  function removeImage() {
    setMedia(null);
    setPreview(null);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-zinc-900 rounded-2xl p-5 space-y-4"
    >
      <div className="bg-zinc-800 rounded-2xl p-4 space-y-4">
        <div className="relative">
          <textarea
            id="post-content"
            placeholder="what's new?"
            maxLength={500}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            className="w-full min-h-[120px] bg-transparent text-white resize-none outline-none placeholder:text-zinc-500"
          />
          <span className="absolute bottom-0 right-1 text-sm text-zinc-400">
            {content.length}/500
          </span>
        </div>

        {preview && (
          <div className="relative">
            <img
              src={preview}
              alt="Preview"
              className="rounded-2xl w-full max-h-[400px] object-cover border border-zinc-700"
            />

            <button
              title="Remove"
              type="button"
              onClick={removeImage}
              className="absolute top-3 right-3 bg-black/70 cursor-pointer hover:bg-black text-white p-2 rounded-full transition"
            >
              <X size={18} />
            </button>
          </div>
        )}
      </div>

      <div className="flex items-center justify-between">
        <label
          htmlFor="post-media"
          className="flex items-center gap-2 cursor-pointer text-blue-400 hover:text-blue-300 transition"
        >
          <ImagePlus size={22} />

          <span>Add an image, video, gifs...</span>
        </label>

        <input
          id="post-media"
          type="file"
          accept="image/*"
          hidden
          onChange={(e) => {
            const file = e.target.files?.[0];

            if (file) {
              setMedia(file);
            }
          }}
        />

        <button
          title="Send post"
          type="submit"
          disabled={isLoading || content.length === 0}
          className="bg-blue-600 cursor-pointer hover:bg-blue-700 disabled:opacity-50 transition px-5 py-3 rounded-xl text-white font-medium"
        >
          {isLoading ? <Ellipsis size={26} /> : <SendHorizontal size={26} />}
        </button>
      </div>
    </form>
  );
}

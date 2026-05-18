import { api } from "./apiClient";

import type {
  Comment,
  CreatePostData,
  PaginatedResponse,
  Post,
} from "../types";

export const postService = {
  async getFeed(): Promise<Post[]> {
    const res = await api.get<PaginatedResponse<Post>>("/feed/");

    return res.data.results;
  },

  async getUserPosts(username: string): Promise<Post[]> {
    const res = await api.get<PaginatedResponse<Post>>(
      `/posts/?author=${username}`,
    );

    return res.data.results;
  },

  async createPost(data: CreatePostData): Promise<Post> {
    const formData = new FormData();

    formData.append("content", data.content);

    if (data.media) {
      formData.append("media", data.media);
    }

    const res = await api.post<Post>("/posts/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return res.data;
  },

  async deletePost(postId: number) {
    const res = await api.delete(`/posts/${postId}/`);

    return res.data;
  },
};

export const likeService = {
  async createLike(postId: number) {
    const res = await api.post(`/posts/${postId}/like/`);

    return res.data;
  },

  async deleteLike(postId: number) {
    const res = await api.delete(`/posts/${postId}/like/`);

    return res.data;
  },
};

export const commentService = {
  async getComments(postId: number): Promise<Comment[]> {
    const res = await api.get<PaginatedResponse<Comment>>(
      `/posts/${postId}/comments/`,
    );

    return res.data.results;
  },

  async createComment(postId: number, content: string) {
    const res = await api.post<Comment>(`/posts/${postId}/comments/`, {
      content,
    });

    return res.data;
  },

  async deleteComment(commentId: number) {
    const res = await api.delete(`/posts/comments/${commentId}/`);

    return res.data;
  },
};

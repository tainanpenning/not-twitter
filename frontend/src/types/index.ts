export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
  };
}

export interface RegisterData {
  username: string;
  email: string;
  birth_date: string;
  password: string;
  password_confirm: string;
}

export interface Profile {
  id: number;
  username: string;
  email: string;
  display_name?: string;
  bio?: string;
  birth_date?: string;
  avatar?: string;
  followers_count: number;
  following_count: number;
  is_following: boolean;
  created_at: string;
  updated_at: string;
}

export interface UpdateProfileData {
  display_name?: string;
  bio?: string;
  avatar?: File | null;
  birth_date?: string;
  email?: string;
  password?: string;
  password_confirm?: string;
}

export interface SearchUser {
  id: number;
  username: string;
  display_name: string;
  avatar: string;
}

export interface Post {
  id: number;
  author_username: string;
  author_display_name?: string;
  author_avatar?: string;
  content: string;
  media?: string;
  likes_count: number;
  comments_count: number;
  is_liked: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreatePostData {
  content: string;
  media?: File | null;
}

export interface Comment {
  id: number;
  post: number;
  content: string;
  created_at: string;
  updated_at: string;
  author_username: string;
  author_display_name?: string;
  author_avatar?: string;
}

export interface LikeResponse {
  status: "liked" | "unliked";
  likes_count: number;
}

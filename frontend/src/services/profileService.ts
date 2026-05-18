import { api } from "./apiClient";

import type {
  PaginatedResponse,
  Profile,
  SearchUser,
  UpdateProfileData,
} from "../types";

export const profileService = {
  async getProfile(username: string): Promise<Profile> {
    const res = await api.get<Profile>(`/profiles/${username}/`);

    return res.data;
  },

  async updateProfile(data: UpdateProfileData) {
    const formData = new FormData();

    if (data.display_name) {
      formData.append("display_name", data.display_name);
    }

    if (data.bio) {
      formData.append("bio", data.bio);
    }

    if (data.avatar) {
      formData.append("avatar", data.avatar);
    }

    if (data.birth_date) {
      formData.append("birth_date", data.birth_date);
    }

    if (data.email) {
      formData.append("email", data.email);
    }

    if (data.password) {
      formData.append("password", data.password);
    }

    if (data.password_confirm) {
      formData.append("password_confirm", data.password_confirm);
    }

    const res = await api.patch("/profiles/me/", formData);

    return res.data;
  },

  async searchUsers(query: string): Promise<PaginatedResponse<SearchUser>> {
    const res = await api.get<PaginatedResponse<SearchUser>>(
      `/profiles/?q=${query}`,
    );

    return res.data;
  },

  async getFollowers(username: string): Promise<PaginatedResponse<Profile>> {
    const res = await api.get<PaginatedResponse<Profile>>(
      `/profiles/${username}/followers/`,
    );

    return res.data;
  },

  async getFollowing(username: string): Promise<PaginatedResponse<Profile>> {
    const res = await api.get<PaginatedResponse<Profile>>(
      `/profiles/${username}/following/`,
    );

    return res.data;
  },
};

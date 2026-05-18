import { api } from "./apiClient";

export interface ToggleFollowResponse {
  is_following: boolean;
}

export const followService = {
  async toggleFollow(username: string): Promise<ToggleFollowResponse> {
    const res = await api.post<ToggleFollowResponse>(
      `/profiles/${username}/follow/`,
    );

    return res.data;
  },
};

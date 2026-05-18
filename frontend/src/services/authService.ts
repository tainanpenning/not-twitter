import { api, tokenService } from "./apiClient";

import type { LoginResponse, RegisterData } from "../types";

export const authService = {
  async login(identifier: string, password: string): Promise<LoginResponse> {
    const res = await api.post<LoginResponse>("auth/login/", {
      identifier,
      password,
    });

    tokenService.setTokens(res.data.access, res.data.refresh);

    return res.data;
  },

  async register(data: RegisterData) {
    const res = await api.post("auth/register/", data);

    return res.data;
  },

  async getCurrentUser() {
    const res = await api.get("profiles/me/");
    return res.data;
  },

  logout() {
    tokenService.clearTokens();
  },
};

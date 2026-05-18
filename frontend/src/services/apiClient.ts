import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL;

export const api = axios.create({
  baseURL: API_BASE_URL,
});

const ACCESS_KEY = "access_token";
const REFRESH_KEY = "refresh_token";

export const tokenService = {
  getAccessToken() {
    return localStorage.getItem(ACCESS_KEY);
  },

  getRefreshToken() {
    return localStorage.getItem(REFRESH_KEY);
  },

  setTokens(access: string, refresh: string) {
    localStorage.setItem(ACCESS_KEY, access);
    localStorage.setItem(REFRESH_KEY, refresh);
  },

  clearTokens() {
    localStorage.removeItem(ACCESS_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
};

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = tokenService.getAccessToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

let isRefreshing = false;
let refreshPromise: Promise<string> | null = null;

interface RetryQueueItem {
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
}

let failedQueue: RetryQueueItem[] = [];

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((promise) => {
    if (error) {
      promise.reject(error);
    } else if (token) {
      promise.resolve(token);
    }
  });

  failedQueue = [];
};

api.interceptors.response.use(
  (response) => response,

  async (error: AxiosError) => {
    const originalRequest = error.config as
      | (InternalAxiosRequestConfig & {
          _retry?: boolean;
        })
      | undefined;

    if (
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry
    ) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({
          resolve: (token: string) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(api(originalRequest));
          },

          reject: (err) => {
            reject(err);
          },
        });
      });
    }

    isRefreshing = true;

    try {
      const refreshToken = tokenService.getRefreshToken();

      if (!refreshToken) {
        throw new Error("No refresh token");
      }

      refreshPromise = axios
        .post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refreshToken,
        })
        .then((res) => {
          const access = res.data?.access;

          if (!access) {
            throw new Error("Invalid refresh response");
          }
          return access;
        });

      const newAccessToken = await refreshPromise;

      tokenService.setTokens(newAccessToken, refreshToken);

      processQueue(null, newAccessToken);

      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

      return api(originalRequest);
    } catch (refreshError) {
      processQueue(refreshError, null);

      tokenService.clearTokens();

      window.dispatchEvent(new CustomEvent("auth-expired"));

      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
      refreshPromise = null;
    }
  },
);

import { BrowserRouter, Routes, Route } from "react-router-dom";

import { LoginPage } from "../pages/loginPage";
import { RegisterPage } from "../pages/registerPage";
import { FeedPage } from "../pages/feedPage";
import { ProfilePage } from "../pages/profilePage";
import { EditProfilePage } from "../pages/editProfilePage";
import { FollowPage } from "../pages/followPage";

import { ProtectedRoute } from "./protectedRoutes";
import { PublicRoute } from "./publicRoutes";

export function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          }
        />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <FeedPage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/profile/:username"
          element={
            <ProtectedRoute>
              <ProfilePage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/profile/edit"
          element={
            <ProtectedRoute>
              <EditProfilePage />
            </ProtectedRoute>
          }
        />

        <Route
          path="/profile/:username/:type"
          element={
            <ProtectedRoute>
              <FollowPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

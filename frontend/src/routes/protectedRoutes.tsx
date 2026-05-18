import { Navigate } from "react-router-dom";
import { useSelector } from "react-redux";

import { LoadingScreen } from "../components/layout/loading";

import type { RootState } from "../store";

interface Props {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: Props) {
  const { isAuthenticated, initialized } = useSelector(
    (state: RootState) => state.authSlice,
  );

  if (!initialized) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

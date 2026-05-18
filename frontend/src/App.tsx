import { useDispatch } from "react-redux";
import { AppRoutes } from "./routes/appRoutes";
import { useEffect } from "react";
import { store, type AppDispatch } from "./store";
import { loadUser, logout } from "./store/slices/authSlice";
import { tokenService } from "./services/apiClient";

window.addEventListener("auth-expired", () => {
  store.dispatch(logout());
});

export default function App() {
  const dispatch = useDispatch<AppDispatch>();

  useEffect(() => {
    const token = tokenService.getAccessToken();

    if (token) {
      dispatch(loadUser());
    } else {
      dispatch(logout());
    }
  }, [dispatch]);

  return <AppRoutes />;
}

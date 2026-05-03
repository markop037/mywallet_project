import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import React from "react";
import ReactDOM from "react-dom/client";
import { Navigate, Route, BrowserRouter as Router, Routes } from "react-router-dom";
import { useAuth } from "./hooks/useAuth";
import { supabase } from "./lib/supabase";
import AuthCallbackPage from "./pages/AuthCallbackPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import "./styles.css";

// Clear local auth state when Supabase signs the user out.
// Token storage is handled exclusively by LoginPage and AuthCallbackPage —
// do NOT sync session.access_token here, as Supabase token refreshes would
// overwrite the backend JWT and cause immediate 401 logouts.
supabase.auth.onAuthStateChange((event) => {
  if (event === "SIGNED_OUT") {
    useAuth.getState().logout();
  }
});

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 30_000,
    },
  },
});

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { token } = useAuth();
  return token ? <>{children}</> : <Navigate to="/login" replace />;
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/auth/callback" element={<AuthCallbackPage />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  </React.StrictMode>
);

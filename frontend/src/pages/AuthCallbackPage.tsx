import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { supabase } from "../lib/supabase";

export default function AuthCallbackPage() {
  const navigate = useNavigate();
  const { setToken } = useAuth();

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      if (session?.access_token) {
        setToken(session.access_token);
        navigate("/dashboard", { replace: true });
      } else {
        navigate("/login", { replace: true });
      }
    });
  }, [navigate, setToken]);

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <p className="text-gray-400 text-sm animate-pulse">Signing you in...</p>
    </div>
  );
}

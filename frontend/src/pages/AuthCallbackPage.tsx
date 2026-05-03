import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { exchangeGoogleToken } from "../api/auth";
import { useAuth } from "../hooks/useAuth";
import { supabase } from "../lib/supabase";

export default function AuthCallbackPage() {
  const navigate = useNavigate();
  const { setToken } = useAuth();

  useEffect(() => {
    supabase.auth.getSession().then(async ({ data: { session } }) => {
      if (session?.access_token) {
        try {
          const res = await exchangeGoogleToken(session.access_token);
          setToken(res.data.access_token);
          navigate("/dashboard", { replace: true });
        } catch {
          navigate("/login", { replace: true });
        }
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

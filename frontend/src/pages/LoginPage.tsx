import { useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { login } from "../api/auth";
import { useAuth } from "../hooks/useAuth";
import { supabase } from "../lib/supabase";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { setToken } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await login({ username, password });
      queryClient.clear();
      setToken(res.data.access_token);
      navigate("/dashboard");
    } catch {
      setError("Invalid username or password.");
    } finally {
      setLoading(false);
    }
  }

  async function signInWithGoogle() {
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: { redirectTo: `${window.location.origin}/auth/callback` },
    });
  }

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-sm space-y-5 sm:space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white">MyWallet</h1>
          <p className="text-gray-400 mt-1">Sign in to your account</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-green-500"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-green-500"
            required
          />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg transition-colors disabled:opacity-50"
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-700" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="bg-gray-900 px-3 text-gray-400">Or continue with</span>
          </div>
        </div>

        <button
          onClick={signInWithGoogle}
          className="w-full flex items-center justify-center gap-2 bg-gray-800 hover:bg-gray-700 border border-gray-700 text-white py-2.5 rounded-lg transition-colors text-sm font-medium"
        >
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path fill="#EA4335" d="M5.27 9.76A7.08 7.08 0 0 1 19.07 12H12v3.46h6.74A6.97 6.97 0 0 1 5.27 9.76z" />
            <path fill="#4285F4" d="M19.07 12A7.08 7.08 0 1 1 5.27 9.76l-3.06-2.34A11.5 11.5 0 1 0 23.5 12z" />
            <path fill="#FBBC05" d="M5.27 9.76 2.21 7.42A11.5 11.5 0 0 0 .5 12h4.08a7 7 0 0 1 .69-2.24z" />
            <path fill="#34A853" d="M12 19.08a7 7 0 0 1-6.73-5.08H.5a11.5 11.5 0 0 0 11.5 9z" />
          </svg>
          Continue with Google
        </button>

        <p className="text-center text-gray-400 text-sm">
          Don't have an account?{" "}
          <Link to="/register" className="text-blue-400 hover:text-blue-300">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}

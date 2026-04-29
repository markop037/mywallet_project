import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { register } from "../api/auth";

export default function RegisterPage() {
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    username: "",
    password: "",
    confirmPassword: "",
    email: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      await register({
        first_name: form.first_name,
        last_name: form.last_name,
        username: form.username,
        password: form.password,
        email: form.email,
      });
      navigate("/login", { state: { message: "Registration successful! Please log in." } });
    } catch (err: unknown) {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(detail ?? "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white">Create Account</h1>
          <p className="text-gray-400 mt-1">Join MyWallet today</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          {[
            { name: "first_name", placeholder: "First Name" },
            { name: "last_name", placeholder: "Last Name" },
            { name: "username", placeholder: "Username" },
            { name: "email", placeholder: "Email", type: "email" },
            { name: "password", placeholder: "Password", type: "password" },
            { name: "confirmPassword", placeholder: "Confirm Password", type: "password" },
          ].map((field) => (
            <input
              key={field.name}
              type={field.type ?? "text"}
              name={field.name}
              placeholder={field.placeholder}
              value={form[field.name as keyof typeof form]}
              onChange={handleChange}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-green-500"
              required
            />
          ))}
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg transition-colors disabled:opacity-50"
          >
            {loading ? "Creating account..." : "Create Account"}
          </button>
        </form>

        <p className="text-center text-gray-400 text-sm">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-400 hover:text-blue-300">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}

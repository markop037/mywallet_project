import axios from "axios";

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL as string });

export interface RegisterPayload {
  first_name: string;
  last_name: string;
  username: string;
  password: string;
  email: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export const login = (data: LoginPayload) =>
  API.post<TokenResponse>("/auth/login", data);

export const register = (data: RegisterPayload) =>
  API.post<{ message: string }>("/auth/register", data);

export const exchangeGoogleToken = (supabaseToken: string) =>
  API.post<TokenResponse>("/auth/google", { access_token: supabaseToken });

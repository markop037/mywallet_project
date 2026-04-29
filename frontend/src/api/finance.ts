import axios from "axios";

const API = axios.create({ baseURL: import.meta.env.VITE_API_URL as string });

const authHeaders = (token: string) => ({
  headers: { Authorization: `Bearer ${token}` },
});

export interface Transaction {
  id: number;
  type: "Income" | "Expense";
  category: string;
  amount: number;
  description: string;
  created_at: string;
}

export interface SummaryItem {
  category: string;
  total: number;
}

export interface AddIncomePayload {
  category_id: number;
  amount: number;
  description?: string;
}

export interface AddExpensePayload {
  category_id: number;
  amount: number;
  description?: string;
}

export const getBalance = (token: string) =>
  API.get<{ balance: number }>("/finance/balance", authHeaders(token));

export const getTransactions = (token: string, limit = 20) =>
  API.get<Transaction[]>(`/finance/transactions?limit=${limit}`, authHeaders(token));

export const getIncomeSummary = (token: string) =>
  API.get<SummaryItem[]>("/finance/summary/incomes", authHeaders(token));

export const getExpenseSummary = (token: string) =>
  API.get<SummaryItem[]>("/finance/summary/expenses", authHeaders(token));

export const addIncome = (token: string, data: AddIncomePayload) =>
  API.post("/finance/incomes", data, authHeaders(token));

export const addExpense = (token: string, data: AddExpensePayload) =>
  API.post("/finance/expenses", data, authHeaders(token));

export const deleteTransaction = (token: string, txType: string, txId: number) =>
  API.delete(`/finance/transactions/${txType}/${txId}`, authHeaders(token));

export interface Category {
  id: number;
  name: string;
}

export const getIncomeCategories = (token: string) =>
  API.get<Category[]>("/finance/categories/incomes", authHeaders(token));

export const getExpenseCategories = (token: string) =>
  API.get<Category[]>("/finance/categories/expenses", authHeaders(token));

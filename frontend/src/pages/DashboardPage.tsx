import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  addExpense,
  addIncome,
  getBalance,
  getExpenseCategories,
  getExpenseSummary,
  getIncomeCategories,
  getIncomeSummary,
  getTransactions,
} from "../api/finance";
import { BalanceCard } from "../components/BalanceCard";
import { SummaryChart } from "../components/SummaryChart";
import { TransactionHistory } from "../components/TransactionHistory";
import { useAuth } from "../hooks/useAuth";


export default function DashboardPage() {
  const { token, logout } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [selectedIncomeCategory, setSelectedIncomeCategory] = useState(0);
  const [selectedExpenseCategory, setSelectedExpenseCategory] = useState(0);
  const [txError, setTxError] = useState("");
  const [activeChart, setActiveChart] = useState<"incomes" | "expenses" | null>(null);

  const { data: balanceData } = useQuery({
    queryKey: ["balance"],
    queryFn: () => getBalance(token!).then((r) => r.data),
    enabled: !!token,
  });

  const { data: transactions = [] } = useQuery({
    queryKey: ["transactions"],
    queryFn: () => getTransactions(token!).then((r) => r.data),
    enabled: !!token,
  });

  const { data: incomeSummary = [] } = useQuery({
    queryKey: ["incomeSummary"],
    queryFn: () => getIncomeSummary(token!).then((r) => r.data),
    enabled: !!token && activeChart === "incomes",
  });

  const { data: expenseSummary = [] } = useQuery({
    queryKey: ["expenseSummary"],
    queryFn: () => getExpenseSummary(token!).then((r) => r.data),
    enabled: !!token && activeChart === "expenses",
  });

  const { data: incomeCategories = [] } = useQuery({
    queryKey: ["incomeCategories"],
    queryFn: () => getIncomeCategories(token!).then((r) => r.data),
    enabled: !!token,
  });

  const { data: expenseCategories = [] } = useQuery({
    queryKey: ["expenseCategories"],
    queryFn: () => getExpenseCategories(token!).then((r) => r.data),
    enabled: !!token,
  });

  const incomeMutation = useMutation({
    mutationFn: (data: { category_id: number; amount: number; description: string }) =>
      addIncome(token!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["balance"] });
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      queryClient.invalidateQueries({ queryKey: ["incomeSummary"] });
      setAmount("");
      setDescription("");
      setSelectedIncomeCategory(0);
      setTxError("");
    },
    onError: (err: unknown) => {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setTxError(detail ?? "Failed to add income.");
    },
  });

  const expenseMutation = useMutation({
    mutationFn: (data: { category_id: number; amount: number; description: string }) =>
      addExpense(token!, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["balance"] });
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      queryClient.invalidateQueries({ queryKey: ["expenseSummary"] });
      setAmount("");
      setDescription("");
      setSelectedExpenseCategory(0);
      setTxError("");
    },
    onError: (err: unknown) => {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setTxError(detail ?? "Failed to add expense.");
    },
  });

  function handleAddIncome() {
    setTxError("");
    const parsed = parseFloat(amount);
    if (isNaN(parsed) || parsed <= 0) { setTxError("Amount must be a positive number."); return; }
    if (!selectedIncomeCategory) { setTxError("Please select an income category."); return; }
    incomeMutation.mutate({ category_id: selectedIncomeCategory, amount: parsed, description });
  }

  function handleAddExpense() {
    setTxError("");
    const parsed = parseFloat(amount);
    if (isNaN(parsed) || parsed <= 0) { setTxError("Amount must be a positive number."); return; }
    if (!selectedExpenseCategory) { setTxError("Please select an expense category."); return; }
    expenseMutation.mutate({ category_id: selectedExpenseCategory, amount: parsed, description });
  }

  function handleLogout() {
    logout();
    navigate("/login");
  }

  const incomeChartData = incomeSummary.map((s) => ({ name: s.category, value: s.total }));
  const expenseChartData = expenseSummary.map((s) => ({ name: s.category, value: s.total }));

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4 flex items-center justify-between">
        <h1 className="text-xl font-bold text-green-400">MyWallet</h1>
        <button
          onClick={handleLogout}
          className="text-gray-400 hover:text-white text-sm transition-colors"
        >
          Sign out
        </button>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8 space-y-8">
        {balanceData && <BalanceCard balance={balanceData.balance} />}

        {/* Chart toggle */}
        <div className="flex gap-3">
          <button
            onClick={() => setActiveChart(activeChart === "incomes" ? null : "incomes")}
            className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
              activeChart === "incomes"
                ? "bg-green-600 text-white"
                : "bg-gray-800 text-gray-300 hover:bg-gray-700"
            }`}
          >
            Income Summary
          </button>
          <button
            onClick={() => setActiveChart(activeChart === "expenses" ? null : "expenses")}
            className={`px-4 py-2 rounded-lg font-medium text-sm transition-colors ${
              activeChart === "expenses"
                ? "bg-orange-600 text-white"
                : "bg-gray-800 text-gray-300 hover:bg-gray-700"
            }`}
          >
            Expense Summary
          </button>
        </div>

        {activeChart === "incomes" && (
          <SummaryChart data={incomeChartData} title="Income by Category" />
        )}
        {activeChart === "expenses" && (
          <SummaryChart data={expenseChartData} title="Expenses by Category" />
        )}

        {/* Add transaction */}
        <div className="bg-gray-800 rounded-xl p-6 space-y-4">
          <h2 className="text-lg font-bold">Add Transaction</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <input
              type="number"
              step="0.01"
              min="0.01"
              placeholder="Amount *"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-green-500"
            />
            <input
              type="text"
              placeholder="Description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-green-500"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm text-gray-400">Income Category</label>
              <select
                value={selectedIncomeCategory}
                onChange={(e) => {
                  setSelectedIncomeCategory(Number(e.target.value));
                  setSelectedExpenseCategory(0);
                }}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-green-500"
              >
                <option value={0}>Select category…</option>
                {incomeCategories.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
              <button
                onClick={handleAddIncome}
                disabled={incomeMutation.isPending}
                className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 rounded-lg transition-colors disabled:opacity-50"
              >
                {incomeMutation.isPending ? "Adding…" : "Add Income"}
              </button>
            </div>

            <div className="space-y-2">
              <label className="text-sm text-gray-400">Expense Category</label>
              <select
                value={selectedExpenseCategory}
                onChange={(e) => {
                  setSelectedExpenseCategory(Number(e.target.value));
                  setSelectedIncomeCategory(0);
                }}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-green-500"
              >
                <option value={0}>Select category…</option>
                {expenseCategories.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
              <button
                onClick={handleAddExpense}
                disabled={expenseMutation.isPending}
                className="w-full bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 rounded-lg transition-colors disabled:opacity-50"
              >
                {expenseMutation.isPending ? "Adding…" : "Add Expense"}
              </button>
            </div>
          </div>

          {txError && <p className="text-red-400 text-sm">{txError}</p>}
        </div>

        {/* Transaction history */}
        <div className="space-y-3">
          <h2 className="text-lg font-bold">Recent Transactions</h2>
          <TransactionHistory transactions={transactions} />
        </div>
      </main>
    </div>
  );
}

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
  type Period,
} from "../api/finance";
import { BalanceCard } from "../components/BalanceCard";
import { SummaryChart } from "../components/SummaryChart";
import { TransactionHistory } from "../components/TransactionHistory";
import { useAuth } from "../hooks/useAuth";
import { supabase } from "../lib/supabase";

const PERIOD_LABELS: Record<Period, string> = {
  all: "All Time",
  day: "Today",
  week: "This Week",
  month: "This Month",
  year: "This Year",
};

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
  const [period, setPeriod] = useState<Period>("all");

  const { data: balanceData } = useQuery({
    queryKey: ["balance"],
    queryFn: () => getBalance(token!).then((r) => r.data),
    enabled: !!token,
  });

  const { data: transactions = [] } = useQuery({
    queryKey: ["transactions", period],
    queryFn: () => getTransactions(token!, period).then((r) => r.data),
    enabled: !!token,
  });

  const { data: incomeSummary = [] } = useQuery({
    queryKey: ["incomeSummary", period],
    queryFn: () => getIncomeSummary(token!, period).then((r) => r.data),
    enabled: !!token && activeChart === "incomes",
  });

  const { data: expenseSummary = [] } = useQuery({
    queryKey: ["expenseSummary", period],
    queryFn: () => getExpenseSummary(token!, period).then((r) => r.data),
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

  async function handleLogout() {
    await supabase.auth.signOut();
    queryClient.clear();
    logout();
    navigate("/login");
  }

  const incomeChartData = incomeSummary.map((s) => ({ name: s.category, value: s.total }));
  const expenseChartData = expenseSummary.map((s) => ({ name: s.category, value: s.total }));

  const periodIncome = transactions
    .filter((t) => t.type === "Income")
    .reduce((sum, t) => sum + t.amount, 0);
  const periodExpense = transactions
    .filter((t) => t.type === "Expense")
    .reduce((sum, t) => sum + t.amount, 0);

  const chartTitle = activeChart === "incomes"
    ? `Income by Category${period !== "all" ? ` — ${PERIOD_LABELS[period]}` : ""}`
    : `Expenses by Category${period !== "all" ? ` — ${PERIOD_LABELS[period]}` : ""}`;

  return (
    <div className="min-h-screen bg-gray-900 text-white">

      {/* ── Header ─────────────────────────────────────────────────── */}
      <header className="bg-gray-800/80 backdrop-blur border-b border-gray-700/60 px-4 sm:px-6 py-3 flex items-center justify-between sticky top-0 z-10">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center">
            <svg className="w-5 h-5 text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 12V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h7" />
              <path d="M16 2v4M8 2v4" />
              <circle cx="18" cy="18" r="3" />
              <path d="M18 16v2l1 1" />
            </svg>
          </div>
          <span className="text-lg font-bold text-white tracking-tight">MyWallet</span>
        </div>
        <button
          onClick={handleLogout}
          className="flex items-center gap-1.5 text-sm text-gray-400 hover:text-white transition-colors group"
        >
          <span>Sign out</span>
          <svg className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
        </button>
      </header>

      <main className="max-w-5xl mx-auto px-3 sm:px-4 py-6 sm:py-8 space-y-5 sm:space-y-6">

        {/* ── Balance card ───────────────────────────────────────────── */}
        {balanceData && <BalanceCard balance={balanceData.balance} />}

        {/* ── Period filter ──────────────────────────────────────────── */}
        <div className="overflow-x-auto -mx-3 sm:mx-0 px-3 sm:px-0 pb-0.5 sm:pb-0">
          <div className="bg-gray-800/60 border border-gray-700/50 rounded-2xl p-1 flex gap-1 min-w-max sm:min-w-0">
            {(["all", "day", "week", "month", "year"] as Period[]).map((p) => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={`flex-1 py-2 px-3 sm:px-4 rounded-xl text-xs sm:text-sm font-medium transition-all duration-150 whitespace-nowrap ${
                  period === p
                    ? "bg-gray-700 text-white shadow"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                {PERIOD_LABELS[p]}
              </button>
            ))}
          </div>
        </div>

        {/* ── Period stats row ───────────────────────────────────────── */}
        <div className="grid grid-cols-2 gap-3 sm:gap-4">
          <div className="bg-gray-800/60 border border-gray-700/50 rounded-2xl p-3 sm:p-4 flex items-center gap-3 sm:gap-4">
            <div className="hidden xs:flex w-10 h-10 rounded-xl bg-green-500/15 items-center justify-center shrink-0 sm:flex">
              <svg className="w-5 h-5 text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
                <polyline points="17 6 23 6 23 12" />
              </svg>
            </div>
            <div className="min-w-0">
              <p className="text-xs text-gray-500 uppercase tracking-wider font-medium">Income</p>
              <p className="text-base sm:text-xl font-bold text-green-400 truncate">+${periodIncome.toFixed(2)}</p>
              <p className="text-xs text-gray-500 mt-0.5 hidden sm:block">{PERIOD_LABELS[period]}</p>
            </div>
          </div>
          <div className="bg-gray-800/60 border border-gray-700/50 rounded-2xl p-3 sm:p-4 flex items-center gap-3 sm:gap-4">
            <div className="hidden xs:flex w-10 h-10 rounded-xl bg-orange-500/15 items-center justify-center shrink-0 sm:flex">
              <svg className="w-5 h-5 text-orange-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="23 18 13.5 8.5 8.5 13.5 1 6" />
                <polyline points="17 18 23 18 23 12" />
              </svg>
            </div>
            <div className="min-w-0">
              <p className="text-xs text-gray-500 uppercase tracking-wider font-medium">Expenses</p>
              <p className="text-base sm:text-xl font-bold text-orange-400 truncate">-${periodExpense.toFixed(2)}</p>
              <p className="text-xs text-gray-500 mt-0.5 hidden sm:block">{PERIOD_LABELS[period]}</p>
            </div>
          </div>
        </div>

        {/* ── Charts ─────────────────────────────────────────────────── */}
        <div className="bg-gray-800/60 border border-gray-700/50 rounded-2xl p-4 sm:p-5 space-y-4">
          <div className="flex items-center justify-between gap-2">
            <h2 className="font-semibold text-white">Summary Charts</h2>
            <div className="flex gap-2">
              <button
                onClick={() => setActiveChart(activeChart === "incomes" ? null : "incomes")}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeChart === "incomes"
                    ? "bg-green-500/20 text-green-400 ring-1 ring-green-500/40"
                    : "bg-gray-700 text-gray-400 hover:text-white"
                }`}
              >
                Income
              </button>
              <button
                onClick={() => setActiveChart(activeChart === "expenses" ? null : "expenses")}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeChart === "expenses"
                    ? "bg-orange-500/20 text-orange-400 ring-1 ring-orange-500/40"
                    : "bg-gray-700 text-gray-400 hover:text-white"
                }`}
              >
                Expenses
              </button>
            </div>
          </div>
          {activeChart ? (
            <SummaryChart
              data={activeChart === "incomes" ? incomeChartData : expenseChartData}
              title={chartTitle}
              type={activeChart}
            />
          ) : (
            <p className="text-center text-gray-500 text-sm py-6">
              Select <span className="text-green-400 font-medium">Income</span> or <span className="text-orange-400 font-medium">Expenses</span> above to view the breakdown chart.
            </p>
          )}
        </div>

        {/* ── Add transaction ────────────────────────────────────────── */}
        <div className="space-y-3">
          <h2 className="font-semibold text-white px-1">Add Transaction</h2>

          {/* Shared inputs */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 text-sm font-medium">$</span>
              <input
                type="number"
                step="0.01"
                min="0.01"
                placeholder="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                className="w-full bg-gray-800 border border-gray-700 rounded-xl pl-7 pr-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-500 transition"
              />
            </div>
            <input
              type="text"
              placeholder="Description (optional)"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-gray-500 focus:ring-1 focus:ring-gray-500 transition"
            />
          </div>

          {/* Income / Expense panels */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">

            {/* Income panel */}
            <div className="bg-green-950/30 border border-green-800/40 rounded-2xl p-4 space-y-3">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded-md bg-green-500/20 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5 text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
                  </svg>
                </div>
                <span className="text-sm font-semibold text-green-400">Income</span>
              </div>
              <select
                value={selectedIncomeCategory}
                onChange={(e) => {
                  setSelectedIncomeCategory(Number(e.target.value));
                  setSelectedExpenseCategory(0);
                }}
                className="w-full bg-gray-800/80 border border-gray-700 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-green-600 focus:ring-1 focus:ring-green-600/50 transition"
              >
                <option value={0}>Select category…</option>
                {incomeCategories.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
              <button
                onClick={handleAddIncome}
                disabled={incomeMutation.isPending}
                className="w-full bg-green-600 hover:bg-green-500 active:bg-green-700 text-white text-sm font-bold py-2.5 rounded-xl transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {incomeMutation.isPending ? "Adding…" : "Add Income"}
              </button>
            </div>

            {/* Expense panel */}
            <div className="bg-orange-950/30 border border-orange-800/40 rounded-2xl p-4 space-y-3">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 rounded-md bg-orange-500/20 flex items-center justify-center">
                  <svg className="w-3.5 h-3.5 text-orange-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="5" y1="12" x2="19" y2="12" />
                  </svg>
                </div>
                <span className="text-sm font-semibold text-orange-400">Expense</span>
              </div>
              <select
                value={selectedExpenseCategory}
                onChange={(e) => {
                  setSelectedExpenseCategory(Number(e.target.value));
                  setSelectedIncomeCategory(0);
                }}
                className="w-full bg-gray-800/80 border border-gray-700 rounded-xl px-3 py-2.5 text-sm text-white focus:outline-none focus:border-orange-600 focus:ring-1 focus:ring-orange-600/50 transition"
              >
                <option value={0}>Select category…</option>
                {expenseCategories.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
              <button
                onClick={handleAddExpense}
                disabled={expenseMutation.isPending}
                className="w-full bg-orange-600 hover:bg-orange-500 active:bg-orange-700 text-white text-sm font-bold py-2.5 rounded-xl transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                {expenseMutation.isPending ? "Adding…" : "Add Expense"}
              </button>
            </div>
          </div>

          {txError && (
            <div className="flex items-center gap-2 text-red-400 text-sm bg-red-950/40 border border-red-800/40 rounded-xl px-4 py-3">
              <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              {txError}
            </div>
          )}
        </div>

        {/* ── Transaction history ────────────────────────────────────── */}
        <div className="space-y-3 pb-8">
          <div className="flex items-center justify-between px-1">
            <h2 className="font-semibold text-white">
              Transactions
              {period !== "all" && (
                <span className="ml-2 text-sm font-normal text-gray-500">— {PERIOD_LABELS[period]}</span>
              )}
            </h2>
            {transactions.length > 0 && (
              <span className="text-xs text-gray-500 bg-gray-800 border border-gray-700 rounded-full px-2.5 py-1">
                {transactions.length} entries
              </span>
            )}
          </div>
          <TransactionHistory transactions={transactions} />
        </div>

      </main>

      {/* ── Footer ─────────────────────────────────────────────────── */}
      <footer className="border-t border-gray-800 mt-4">
        <div className="max-w-5xl mx-auto px-3 sm:px-4 py-5 sm:py-6 flex flex-col sm:flex-row items-center justify-between gap-2 sm:gap-3">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-md bg-green-500/20 flex items-center justify-center">
              <svg className="w-3.5 h-3.5 text-green-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="2" y="5" width="20" height="14" rx="2" />
                <path d="M2 10h20" />
              </svg>
            </div>
            <span className="text-sm font-semibold text-gray-400">MyWallet</span>
          </div>
          <p className="text-xs text-gray-600 text-center">
            Track your money. Stay in control.
          </p>
          <p className="text-xs text-gray-700">
            &copy; {new Date().getFullYear()} MyWallet. All rights reserved.
          </p>
        </div>
      </footer>

    </div>
  );
}

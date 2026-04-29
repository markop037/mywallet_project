import { useState } from "react";

interface Props {
  type: "Income" | "Expense";
  categoryId: number;
  onSubmit: (amount: number, description: string) => Promise<void>;
  isLoading?: boolean;
}

export function TransactionForm({ type, categoryId, onSubmit, isLoading }: Props) {
  const [amount, setAmount] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    const parsed = parseFloat(amount);
    if (isNaN(parsed) || parsed <= 0) {
      setError("Amount must be a positive number.");
      return;
    }
    try {
      await onSubmit(parsed, description);
      setAmount("");
      setDescription("");
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "Failed to add transaction.";
      setError(message);
    }
  }

  const isIncome = type === "Income";

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <input
        type="number"
        step="0.01"
        min="0.01"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-green-500"
        required
      />
      <input
        type="text"
        placeholder="Description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:border-green-500"
      />
      {error && <p className="text-red-400 text-sm">{error}</p>}
      <button
        type="submit"
        disabled={isLoading || !categoryId}
        className={`w-full py-2 rounded-lg font-bold text-white transition-colors ${
          isIncome
            ? "bg-green-600 hover:bg-green-700"
            : "bg-orange-600 hover:bg-orange-700"
        } disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        {isLoading ? "Adding..." : `Add ${type}`}
      </button>
    </form>
  );
}

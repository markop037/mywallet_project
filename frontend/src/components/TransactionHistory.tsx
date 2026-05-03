import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteTransaction, type Transaction } from "../api/finance";
import { useAuth } from "../hooks/useAuth";

interface Props {
  transactions: Transaction[];
}

function DeleteButton({
  onClick,
  disabled,
}: {
  onClick: () => void;
  disabled: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      title="Delete transaction"
      className="text-gray-600 hover:text-red-400 transition-colors disabled:cursor-not-allowed"
    >
      <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="3 6 5 6 21 6" />
        <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
        <path d="M10 11v6M14 11v6" />
        <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2" />
      </svg>
    </button>
  );
}

function TypeBadge({ type }: { type: "Income" | "Expense" }) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold ${
        type === "Income"
          ? "bg-green-500/15 text-green-400"
          : "bg-orange-500/15 text-orange-400"
      }`}
    >
      {type}
    </span>
  );
}

function AmountText({ tx }: { tx: Transaction }) {
  return (
    <span
      className={`font-semibold font-mono ${
        tx.type === "Income" ? "text-green-400" : "text-orange-400"
      }`}
    >
      {tx.type === "Income" ? "+" : "−"}${tx.amount.toFixed(2)}
    </span>
  );
}

export function TransactionHistory({ transactions }: Props) {
  const { token } = useAuth();
  const queryClient = useQueryClient();

  const deleteMutation = useMutation({
    mutationFn: ({ txType, txId }: { txType: string; txId: number }) =>
      deleteTransaction(token!, txType, txId),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      queryClient.invalidateQueries({ queryKey: ["balance"] });
      if (variables.txType === "Income") {
        queryClient.invalidateQueries({ queryKey: ["incomeSummary"] });
      } else {
        queryClient.invalidateQueries({ queryKey: ["expenseSummary"] });
      }
    },
  });

  function handleDelete(tx: Transaction) {
    if (window.confirm("Are you sure you want to delete this transaction?")) {
      deleteMutation.mutate({ txType: tx.type, txId: tx.id });
    }
  }

  if (!transactions.length) {
    return (
      <div className="bg-gray-800/40 border border-gray-700/50 rounded-2xl px-6 py-12 text-center">
        <div className="w-12 h-12 rounded-2xl bg-gray-700/60 flex items-center justify-center mx-auto mb-3">
          <svg className="w-6 h-6 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
          </svg>
        </div>
        <p className="text-gray-400 font-medium text-sm">No transactions yet</p>
        <p className="text-gray-600 text-xs mt-1">Add your first income or expense above.</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-800/40 border border-gray-700/50 rounded-2xl overflow-hidden">

      {/* ── Desktop table (md and up) ─────────────────────────────── */}
      <div className="hidden md:block">
        {/* Header row */}
        <div className="grid grid-cols-[1fr_90px_1fr_110px_80px] gap-3 px-4 py-2.5 bg-gray-800/80 border-b border-gray-700/50">
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Description</span>
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Type</span>
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Category</span>
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Amount</span>
          <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider text-right">Date</span>
        </div>
        {/* Data rows */}
        <div className="divide-y divide-gray-700/40">
          {transactions.map((tx) => (
            <div
              key={`${tx.type}-${tx.id}`}
              className="grid grid-cols-[1fr_90px_1fr_110px_80px] gap-3 items-center px-4 py-3 hover:bg-gray-700/20 transition-colors group"
            >
              <span className="text-sm text-gray-300 truncate">
                {tx.description || <span className="text-gray-600 italic">—</span>}
              </span>
              <TypeBadge type={tx.type} />
              <span className="text-sm text-gray-400 truncate">{tx.category}</span>
              <div className="text-sm text-right">
                <AmountText tx={tx} />
              </div>
              <div className="flex items-center justify-end gap-2">
                <span className="text-xs text-gray-600 whitespace-nowrap">
                  {new Date(tx.created_at).toLocaleDateString("en-US", { month: "short", day: "numeric" })}
                </span>
                <span className="opacity-0 group-hover:opacity-100 transition-opacity">
                  <DeleteButton onClick={() => handleDelete(tx)} disabled={deleteMutation.isPending} />
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Mobile card list (below md) ───────────────────────────── */}
      <div className="md:hidden divide-y divide-gray-700/40">
        {transactions.map((tx) => (
          <div key={`${tx.type}-${tx.id}`} className="px-4 py-3 space-y-1.5">
            {/* Top row: badge + amount + delete */}
            <div className="flex items-center justify-between gap-2">
              <div className="flex items-center gap-2 min-w-0">
                <TypeBadge type={tx.type} />
                <span className="text-xs text-gray-500 truncate">{tx.category}</span>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <AmountText tx={tx} />
                <DeleteButton onClick={() => handleDelete(tx)} disabled={deleteMutation.isPending} />
              </div>
            </div>
            {/* Bottom row: description + date */}
            <div className="flex items-center justify-between gap-2">
              <span className="text-sm text-gray-400 truncate">
                {tx.description || <span className="text-gray-600 italic">No description</span>}
              </span>
              <span className="text-xs text-gray-600 whitespace-nowrap shrink-0">
                {new Date(tx.created_at).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
              </span>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}

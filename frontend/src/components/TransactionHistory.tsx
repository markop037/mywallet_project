import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteTransaction, type Transaction } from "../api/finance";
import { useAuth } from "../hooks/useAuth";

interface Props {
  transactions: Transaction[];
}

export function TransactionHistory({ transactions }: Props) {
  const { token } = useAuth();
  const queryClient = useQueryClient();

  const deleteMutation = useMutation({
    mutationFn: ({ txType, txId }: { txType: string; txId: number }) =>
      deleteTransaction(token!, txType, txId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
      queryClient.invalidateQueries({ queryKey: ["balance"] });
    },
  });

  function handleDelete(tx: Transaction) {
    if (window.confirm("Are you sure you want to delete this transaction?")) {
      deleteMutation.mutate({ txType: tx.type, txId: tx.id });
    }
  }

  if (!transactions.length) {
    return (
      <p className="text-center text-gray-400 py-6">
        No transactions yet. Add your first income or expense!
      </p>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-700">
      <table className="w-full text-sm text-left text-gray-300">
        <thead className="bg-gray-800 text-gray-400 uppercase text-xs">
          <tr>
            <th className="px-4 py-3">Date</th>
            <th className="px-4 py-3">Type</th>
            <th className="px-4 py-3">Category</th>
            <th className="px-4 py-3">Amount</th>
            <th className="px-4 py-3">Description</th>
            <th className="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-700">
          {transactions.map((tx) => (
            <tr key={`${tx.type}-${tx.id}`} className="bg-gray-900 hover:bg-gray-800 transition-colors">
              <td className="px-4 py-3 whitespace-nowrap">
                {new Date(tx.created_at).toLocaleDateString()}
              </td>
              <td className="px-4 py-3">
                <span
                  className={`px-2 py-0.5 rounded-full text-xs font-semibold ${
                    tx.type === "Income"
                      ? "bg-green-900 text-green-300"
                      : "bg-orange-900 text-orange-300"
                  }`}
                >
                  {tx.type}
                </span>
              </td>
              <td className="px-4 py-3">{tx.category}</td>
              <td className="px-4 py-3 font-mono">
                <span
                  className={
                    tx.type === "Income" ? "text-green-400" : "text-orange-400"
                  }
                >
                  {tx.type === "Income" ? "+" : "-"}${tx.amount.toFixed(2)}
                </span>
              </td>
              <td className="px-4 py-3 text-gray-400">{tx.description}</td>
              <td className="px-4 py-3">
                <button
                  onClick={() => handleDelete(tx)}
                  disabled={deleteMutation.isPending}
                  className="text-gray-500 hover:text-red-400 transition-colors text-xs"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

interface Props {
  balance: number;
}

export function BalanceCard({ balance }: Props) {
  const isNegative = balance < 0;
  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-gray-800 to-gray-800/60 border border-gray-700/60 p-4 sm:p-6 shadow-xl">
      {/* decorative glow */}
      <div
        className={`absolute -top-10 -right-10 w-40 h-40 rounded-full blur-3xl opacity-20 ${
          isNegative ? "bg-red-500" : "bg-green-500"
        }`}
      />

      <div className="relative flex items-start justify-between gap-4">
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-widest font-semibold mb-2">
            Current Balance
          </p>
          <p
        className={`text-3xl sm:text-5xl font-extrabold tracking-tight ${
          isNegative ? "text-red-400" : "text-green-400"
        }`}
      >
        {isNegative ? "-" : ""}${Math.abs(balance).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
      </p>
      <p className="text-xs text-gray-600 mt-2">All-time net balance</p>
        </div>

        <div className={`shrink-0 w-12 h-12 rounded-2xl flex items-center justify-center ${
          isNegative ? "bg-red-500/15" : "bg-green-500/15"
        }`}>
          <svg
            className={`w-6 h-6 ${isNegative ? "text-red-400" : "text-green-400"}`}
            viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75"
            strokeLinecap="round" strokeLinejoin="round"
          >
            <rect x="2" y="5" width="20" height="14" rx="2" />
            <path d="M2 10h20" />
            <circle cx="7" cy="15" r="1" fill="currentColor" stroke="none" />
            <path d="M11 15h6" />
          </svg>
        </div>
      </div>
    </div>
  );
}

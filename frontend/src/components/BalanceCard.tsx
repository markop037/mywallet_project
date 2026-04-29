interface Props {
  balance: number;
}

export function BalanceCard({ balance }: Props) {
  const isNegative = balance < 0;
  return (
    <div className="bg-gray-800 rounded-xl p-6 shadow-lg">
      <p className="text-gray-400 text-sm mb-1">Current Balance</p>
      <p
        className={`text-4xl font-bold ${
          isNegative ? "text-red-400" : "text-teal-400"
        }`}
      >
        ${balance.toFixed(2)}
      </p>
    </div>
  );
}

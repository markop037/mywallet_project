import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const INCOME_COLORS  = ["#4ade80", "#34d399", "#2dd4bf", "#60a5fa", "#a78bfa", "#f472b6"];
const EXPENSE_COLORS = ["#fb923c", "#f87171", "#facc15", "#a78bfa", "#38bdf8", "#4ade80"];

interface Props {
  data: { name: string; value: number }[];
  title: string;
  type?: "incomes" | "expenses";
}

export function SummaryChart({ data, title, type = "incomes" }: Props) {
  const colors = type === "incomes" ? INCOME_COLORS : EXPENSE_COLORS;

  if (!data.length) {
    return (
      <div className="flex flex-col items-center justify-center py-10 text-center">
        <div className="w-12 h-12 rounded-2xl bg-gray-700/50 flex items-center justify-center mb-3">
          <svg className="w-6 h-6 text-gray-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
            <path d="M22 12A10 10 0 0 0 12 2v10z" />
          </svg>
        </div>
        <p className="text-gray-400 text-sm font-medium">No data for this period</p>
        <p className="text-gray-600 text-xs mt-1">Transactions will appear here once added.</p>
      </div>
    );
  }

  return (
    <div>
      <p className="text-sm text-gray-400 text-center mb-4">{title}</p>
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={95}
            paddingAngle={2}
            label={({ percent }) =>
              percent > 0.05 ? `${(percent * 100).toFixed(0)}%` : ""
            }
            labelLine={false}
          >
            {data.map((_, i) => (
              <Cell key={i} fill={colors[i % colors.length]} strokeWidth={0} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ backgroundColor: "#1f2937", border: "1px solid #374151", borderRadius: "12px", color: "#f9fafb" }}
            formatter={(v: number) => [`$${v.toFixed(2)}`, ""]}
          />
          <Legend
            iconType="circle"
            iconSize={8}
            formatter={(value) => <span style={{ color: "#9ca3af", fontSize: "12px" }}>{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

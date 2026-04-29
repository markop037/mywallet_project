import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const COLORS = ["#4CAF50", "#03A9F4", "#FF5722", "#9C27B0", "#FF9800", "#03DAC6"];

interface Props {
  data: { name: string; value: number }[];
  title: string;
}

export function SummaryChart({ data, title }: Props) {
  if (!data.length) {
    return (
      <p className="text-center text-gray-400 py-8">No data yet.</p>
    );
  }

  return (
    <div className="bg-gray-800 rounded-xl p-4">
      <h3 className="text-white font-bold text-center mb-4 text-lg">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={({ name, percent }) =>
              `${name} ${(percent * 100).toFixed(1)}%`
            }
          >
            {data.map((_, i) => (
              <Cell key={i} fill={COLORS[i % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(v: number) => `$${v.toFixed(2)}`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

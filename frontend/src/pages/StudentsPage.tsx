import React from "react";
import { Student, studentService } from "../services/studentService";
import StudentList from "../components/StudentList";

export default function StudentsPage() {
  const [stats, setStats] = React.useState({
    total: 0,
    pending: 0,
    approved: 0,
  });

  React.useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const students = await studentService.getAllStudents();
      setStats({
        total: students.length,
        pending: students.filter((s) => s.student.state !== "none").length,
        approved: students.filter((s) => s.student.state === "none").length,
      });
    } catch (err) {
      console.error("Error loading stats:", err);
    }
  };

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Student Applications
          </h1>
          <p className="text-gray-500 mt-1">
            Manage and review student enrollment applications
          </p>
        </div>
        <button className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors">
          New Application
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard
          title="Total Applications"
          value={stats.total.toString()}
          change="+12%"
          trend="up"
        />
        <StatCard
          title="Pending Review"
          value={stats.pending.toString()}
          change="-5%"
          trend="down"
        />
        <StatCard
          title="Approved Today"
          value={stats.approved.toString()}
          change="+3"
          trend="up"
        />
      </div>

      <StudentList />
    </div>
  );
}

function StatCard({
  title,
  value,
  change,
  trend,
}: {
  title: string;
  value: string;
  change: string;
  trend: "up" | "down";
}) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 className="text-gray-500 text-sm font-medium">{title}</h3>
      <div className="mt-2 flex items-baseline gap-2">
        <span className="text-2xl font-semibold text-gray-900">{value}</span>
        <span
          className={`text-sm font-medium ${
            trend === "up" ? "text-green-600" : "text-red-600"
          }`}
        >
          {change}
        </span>
      </div>
    </div>
  );
}

import { Outlet, Link, useLocation } from "react-router-dom";
import { authService } from "../services/authService";
import { useNavigate } from "react-router-dom";
import { Users, FileText, Bell, Settings } from "lucide-react";

export default function Layout() {
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    authService.logout();
    navigate("/login");
  };

  const navItems = [
    {
      path: "/students",
      label: "Students",
      icon: <Users className="w-4 h-4" />,
    },
    {
      path: "/applications",
      label: "Applications",
      icon: <FileText className="w-4 h-4" />,
    },
    {
      path: "/notifications",
      label: "Notifications",
      icon: <Bell className="w-4 h-4" />,
    },
    {
      path: "/settings",
      label: "Settings",
      icon: <Settings className="w-4 h-4" />,
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex space-x-4">
              {navItems.map((item) => (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium gap-2 ${
                    location.pathname === item.path
                      ? "border-emerald-500 text-emerald-600"
                      : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  }`}
                >
                  {item.icon}
                  {item.label}
                </Link>
              ))}
            </div>
            <div className="flex items-center">
              <button
                onClick={handleLogout}
                className="text-gray-500 hover:text-gray-700 px-3 py-2 rounded-md text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Page Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
}

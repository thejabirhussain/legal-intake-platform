import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard, Users, MessageSquare, LogOut } from 'lucide-react';

const Layout: React.FC = () => {
    const { logout, user } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="flex h-screen bg-gray-50">
            {/* Sidebar */}
            <aside className="w-64 bg-slate-900 text-white flex flex-col">
                <div className="p-6 border-b border-slate-800">
                    <h1 className="text-xl font-bold">Smart Lawyer</h1>
                    <p className="text-xs text-slate-400 mt-1">Intake & Workflow</p>
                </div>

                <nav className="flex-1 p-4 space-y-2">
                    <Link to="/" className="flex items-center space-x-3 px-4 py-3 bg-slate-800 rounded-lg text-blue-400">
                        <LayoutDashboard size={20} />
                        <span>Cases Dashboard</span>
                    </Link>
                    <Link to="/clients" className="flex items-center space-x-3 px-4 py-3 hover:bg-slate-800 rounded-lg text-slate-300 transition">
                        <Users size={20} />
                        <span>Clients (Soon)</span>
                    </Link>
                    <div className="flex items-center space-x-3 px-4 py-3 text-slate-500 cursor-not-allowed">
                        <MessageSquare size={20} />
                        <span>Messages</span>
                    </div>
                </nav>

                <div className="p-4 border-t border-slate-800">
                    <div className="mb-4 px-4">
                        <p className="text-sm font-medium">{user?.full_name}</p>
                        <p className="text-xs text-slate-400">{user?.role}</p>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="flex items-center space-x-3 px-4 py-2 w-full hover:bg-red-900/20 text-red-400 rounded-lg transition"
                    >
                        <LogOut size={18} />
                        <span>Sign Out</span>
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 overflow-auto">
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Plus, FileText, Smartphone, MoreVertical, LayoutGrid, List, ArrowRight } from 'lucide-react';
import api from '../services/api';

const Dashboard: React.FC = () => {
    const [cases, setCases] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [viewMode, setViewMode] = useState<'list' | 'grid'>('list');

    useEffect(() => {
        // Mock data for now
        const mockCases = [
            { id: 1, client: "Ahmed Al-Farsi", type: "Personal Injury", status: "PENDING_REVIEW", urgency: "High", date: "2023-10-25" },
            { id: 2, client: "Sarah Johnson", type: "Family Law", status: "INTAKE_IN_PROGRESS", urgency: "Medium", date: "2023-10-26" },
            { id: 3, client: "Tech Corp LLC", type: "Corporate", status: "APPROVED", urgency: "Low", date: "2023-10-24" },
            { id: 4, client: "John Doe", type: "Criminal Defense", status: "REJECTED", urgency: "High", date: "2023-10-23" },
        ];
        setTimeout(() => {
            setCases(mockCases);
            setLoading(false);
        }, 500);
    }, []);

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'APPROVED': return 'bg-emerald-500/10 text-emerald-600 border-emerald-200';
            case 'PENDING_REVIEW': return 'bg-amber-500/10 text-amber-600 border-amber-200';
            case 'REJECTED': return 'bg-red-500/10 text-red-600 border-red-200';
            default: return 'bg-blue-500/10 text-blue-600 border-blue-200';
        }
    };

    const getUrgencyColor = (urgency: string) => {
        return urgency === 'High' ? 'text-red-500 font-semibold' : 'text-slate-500';
    }

    return (
        <div className="p-8 max-w-7xl mx-auto">
            <header className="flex flex-col md:flex-row md:justify-between md:items-center mb-10 gap-4">
                <div>
                    <h1 className="text-4xl font-bold text-slate-900 tracking-tight">Case Dashboard</h1>
                    <p className="text-slate-500 mt-2 text-lg">Manage intake and review new potential cases.</p>
                </div>
                <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl flex items-center space-x-2 transition shadow-lg shadow-blue-600/20 font-medium">
                    <Plus size={20} />
                    <span>New Case</span>
                </button>
            </header>

            {/* Metrics Cards (Optional addition for 'World Class' feel) */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <div className="text-slate-500 text-sm font-medium uppercase tracking-wider mb-2">Total Cases</div>
                    <div className="text-3xl font-bold text-slate-900">124</div>
                    <div className="text-emerald-600 text-sm mt-1 flex items-center">
                        <span className="bg-emerald-100 px-1.5 py-0.5 rounded text-xs font-bold mr-2">+12%</span> from last month
                    </div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <div className="text-slate-500 text-sm font-medium uppercase tracking-wider mb-2">Pending Review</div>
                    <div className="text-3xl font-bold text-slate-900">8</div>
                    <div className="text-amber-600 text-sm mt-1">Requires attention</div>
                </div>
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
                    <div className="text-slate-500 text-sm font-medium uppercase tracking-wider mb-2">Approval Rate</div>
                    <div className="text-3xl font-bold text-slate-900">68%</div>
                    <div className="text-slate-400 text-sm mt-1">Based on intake quality</div>
                </div>
            </div>

            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
                <div className="p-5 border-b border-slate-100 flex flex-col sm:flex-row justify-between items-center bg-slate-50/50 gap-4">
                    <div className="relative w-full sm:w-96">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                        <input
                            type="text"
                            placeholder="Search client name, case type..."
                            className="w-full pl-11 pr-4 py-3 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all shadow-sm"
                        />
                    </div>
                    <div className="flex space-x-3 w-full sm:w-auto">
                        <button className="flex-1 sm:flex-none flex items-center justify-center space-x-2 px-4 py-2.5 bg-white border border-slate-200 rounded-xl text-sm font-medium text-slate-600 hover:bg-slate-50 hover:text-slate-900 transition-colors shadow-sm">
                            <Filter size={18} />
                            <span>Filter</span>
                        </button>
                        <div className="bg-slate-100 p-1 rounded-xl flex border border-slate-200">
                            <button
                                onClick={() => setViewMode('list')}
                                className={`p-2 rounded-lg transition-all ${viewMode === 'list' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}
                            >
                                <List size={18} />
                            </button>
                            <button
                                onClick={() => setViewMode('grid')}
                                className={`p-2 rounded-lg transition-all ${viewMode === 'grid' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}
                            >
                                <LayoutGrid size={18} />
                            </button>
                        </div>
                    </div>
                </div>

                {loading ? (
                    <div className="p-20 text-center">
                        <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
                        <p className="mt-4 text-slate-500 font-medium">Loading cases...</p>
                    </div>
                ) : (
                    <>
                        <table className="w-full text-left border-collapse">
                            <thead className="bg-slate-50 border-b border-slate-100">
                                <tr>
                                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Client Name</th>
                                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Case Type</th>
                                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Urgency</th>
                                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Date</th>
                                    <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {cases.map((c) => (
                                    <tr key={c.id} className="hover:bg-slate-50/80 transition-colors group">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center">
                                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 text-white flex items-center justify-center font-bold text-sm shadow-md shadow-blue-500/20 mr-4">
                                                    {c.client.split(' ').map((n: string) => n[0]).join('')}
                                                </div>
                                                <div>
                                                    <div className="font-semibold text-slate-900">{c.client}</div>
                                                    <div className="text-xs text-slate-500 flex items-center mt-0.5">
                                                        <Smartphone size={10} className="mr-1" /> WhatsApp
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="text-sm text-slate-700 font-medium bg-slate-100 inline-block px-2.5 py-1 rounded-md border border-slate-200">{c.type}</div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`px-3 py-1 rounded-full text-xs font-bold border ${getStatusColor(c.status)}`}>
                                                {c.status.replace('_', ' ')}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className={`text-sm ${getUrgencyColor(c.urgency)} flex items-center`}>
                                                {c.urgency === 'High' && <span className="w-2 h-2 rounded-full bg-red-500 mr-2 animate-pulse"></span>}
                                                {c.urgency}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-slate-500 text-sm font-medium">{c.date}</td>
                                        <td className="px-6 py-4 text-right">
                                            <Link
                                                to={`/cases/${c.id}`}
                                                className="inline-flex items-center text-blue-600 hover:text-blue-800 font-semibold text-sm hover:underline decoration-2 underline-offset-2 transition-all opacity-0 group-hover:opacity-100 transform translate-x-2 group-hover:translate-x-0"
                                            >
                                                View Details <ArrowRight size={14} className="ml-1" />
                                            </Link>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {cases.length === 0 && (
                            <div className="p-12 text-center text-slate-500 bg-slate-50/50">
                                <FileText size={48} className="mx-auto text-slate-300 mb-4" />
                                <h3 className="text-lg font-medium text-slate-900">No cases found</h3>
                                <p>Waiting for new intakes via WhatsApp.</p>
                            </div>
                        )}
                    </>
                )}
            </div>

            {/* Pagination / Footer */}
            <div className="mt-6 flex justify-between items-center text-slate-500 text-sm">
                <div>Showing 1 to {cases.length} of {cases.length} entries</div>
                <div className="flex space-x-2">
                    <button className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50" disabled>Previous</button>
                    <button className="px-4 py-2 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50" disabled>Next</button>
                </div>
            </div>
        </div>
    );
};


export default Dashboard;

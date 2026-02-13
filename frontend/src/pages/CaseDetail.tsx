import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, MessageSquare, FileText, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

const CaseDetail: React.FC = () => {
    const { id } = useParams();

    // Mock Data
    const caseDetails = {
        id,
        client: "Ahmed Al-Farsi",
        type: "Personal Injury",
        status: "PENDING_REVIEW",
        summary: "Client was involved in a car accident on Sheikh Zayed Road. The other driver ran a red light. Client suffered minor injuries and vehicle damage. Seeking compensation.",
        history: [
            { sender: "USER", text: "Hi, I need help with a car accident claim.", time: "10:00 AM" },
            { sender: "AGENT", text: "I can help with that. Could you please provide your full name?", time: "10:00 AM" },
            { sender: "USER", text: "Ahmed Al-Farsi", time: "10:01 AM" },
            { sender: "AGENT", text: "Thank you Ahmed. When did this incident occur?", time: "10:01 AM" },
            { sender: "USER", text: "Yesterday, on Sheikh Zayed Road.", time: "10:02 AM" },
        ]
    };

    return (
        <div className="p-8 max-w-6xl mx-auto h-screen flex flex-col">
            <div className="mb-6">
                <Link to="/" className="text-gray-500 hover:text-gray-700 flex items-center space-x-1 mb-2">
                    <ArrowLeft size={16} />
                    <span>Back to Dashboard</span>
                </Link>
                <div className="flex justify-between items-start">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Case #{id}: {caseDetails.client}</h1>
                        <p className="text-gray-500 mt-1 flex items-center space-x-2">
                            <span>{caseDetails.type}</span>
                            <span>•</span>
                            <span className="text-yellow-600 font-medium">{caseDetails.status.replace('_', ' ')}</span>
                        </p>
                    </div>
                    <div className="flex space-x-3">
                        <button className="bg-red-50 text-red-700 border border-red-200 px-4 py-2 rounded-lg hover:bg-red-100 flex items-center space-x-2">
                            <XCircle size={18} />
                            <span>Reject</span>
                        </button>
                        <button className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 flex items-center space-x-2 shadow-sm">
                            <CheckCircle size={18} />
                            <span>Approve Intake</span>
                        </button>
                    </div>
                </div>
            </div>

            <div className="flex-1 grid grid-cols-3 gap-6 overflow-hidden pb-4">
                {/* Left: Case Info & Summary */}
                <div className="col-span-2 overflow-y-auto space-y-6">
                    {/* AI Summary Card */}
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                        <h2 className="text-lg font-bold text-gray-800 mb-4 flex items-center space-x-2">
                            <FileText size={20} className="text-blue-600" />
                            <span>AI Case Summary</span>
                        </h2>
                        <div className="bg-blue-50 p-4 rounded-lg text-gray-700 leading-relaxed border border-blue-100">
                            {caseDetails.summary}
                        </div>
                    </div>

                    {/* Extracted Entities */}
                    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                        <h2 className="text-lg font-bold text-gray-800 mb-4">Extracted Data</h2>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-3 bg-gray-50 rounded-lg">
                                <p className="text-xs text-gray-500 uppercase font-semibold">Incident Date</p>
                                <p className="text-gray-800 font-medium">Yesterday</p>
                            </div>
                            <div className="p-3 bg-gray-50 rounded-lg">
                                <p className="text-xs text-gray-500 uppercase font-semibold">Location</p>
                                <p className="text-gray-800 font-medium">Sheikh Zayed Road</p>
                            </div>
                            <div className="p-3 bg-gray-50 rounded-lg">
                                <p className="text-xs text-gray-500 uppercase font-semibold">Injury Type</p>
                                <p className="text-gray-800 font-medium">Minor</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right: Chat History */}
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col h-full overflow-hidden">
                    <div className="p-4 border-b border-gray-100 bg-gray-50/50 flex items-center justify-between">
                        <h3 className="font-bold text-gray-700 flex items-center space-x-2">
                            <MessageSquare size={18} />
                            <span>Conversation History</span>
                        </h3>
                        <span className="text-xs text-green-600 font-medium bg-green-100 px-2 py-1 rounded-full">Active</span>
                    </div>
                    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50/30">
                        {caseDetails.history.map((msg, i) => (
                            <div key={i} className={`flex ${msg.sender === 'USER' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm shadow-sm ${msg.sender === 'USER'
                                        ? 'bg-blue-600 text-white rounded-br-none'
                                        : 'bg-white text-gray-700 border border-gray-200 rounded-bl-none'
                                    }`}>
                                    <p>{msg.text}</p>
                                    <p className={`text-[10px] mt-1 ${msg.sender === 'USER' ? 'text-blue-200' : 'text-gray-400'}`}>
                                        {msg.time}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="p-3 border-t border-gray-200 bg-white">
                        <input
                            disabled
                            placeholder="Intervention agent only (Read Only)"
                            className="w-full bg-gray-100 border-none rounded-lg text-sm px-4 py-2 cursor-not-allowed"
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CaseDetail;

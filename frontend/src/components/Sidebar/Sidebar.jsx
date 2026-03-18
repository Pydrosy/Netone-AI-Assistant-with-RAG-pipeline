import React from 'react';
import { MessageSquare, Settings, HelpCircle, X } from 'lucide-react';
import ConversationHistory from './ConversationHistory';

const Sidebar = ({ isOpen, onClose }) => {
  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out z-50 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      } lg:translate-x-0`}>
        <div className="p-4">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Netone AI</h2>
            <button 
              onClick={onClose}
              className="lg:hidden p-1 hover:bg-gray-100 rounded"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <nav className="space-y-1">
            <button className="w-full flex items-center gap-2 px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors">
              <MessageSquare className="w-5 h-5" />
              <span>New Chat</span>
            </button>
            <button className="w-full flex items-center gap-2 px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors">
              <Settings className="w-5 h-5" />
              <span>Settings</span>
            </button>
            <button className="w-full flex items-center gap-2 px-3 py-2 text-gray-700 rounded-lg hover:bg-gray-100 transition-colors">
              <HelpCircle className="w-5 h-5" />
              <span>Help & FAQ</span>
            </button>
          </nav>

          <div className="mt-8">
            <h3 className="text-sm font-medium text-gray-500 mb-3 px-3">Recent Chats</h3>
            <ConversationHistory />
          </div>

          <div className="absolute bottom-4 left-4 right-4">
            <div className="px-3 py-2 bg-gray-50 rounded-lg">
              <p className="text-xs text-gray-500">Connected to Netone</p>
              <p className="text-xs text-green-600 mt-1">● Online</p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;

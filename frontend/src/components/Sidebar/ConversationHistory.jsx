import React, { useState, useEffect } from 'react';
import { Clock, Trash2 } from 'lucide-react';

const ConversationHistory = () => {
  const [conversations, setConversations] = useState([]);

  // Load conversations from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('netone-conversations');
    if (saved) {
      try {
        setConversations(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to load conversations:', e);
      }
    }
  }, []);

  const deleteConversation = (id, e) => {
    e.stopPropagation();
    const updated = conversations.filter(conv => conv.id !== id);
    setConversations(updated);
    localStorage.setItem('netone-conversations', JSON.stringify(updated));
  };

  if (conversations.length === 0) {
    return (
      <div className="px-3 py-4 text-center">
        <Clock className="w-8 h-8 text-gray-300 mx-auto mb-2" />
        <p className="text-sm text-gray-500">No recent chats</p>
        <p className="text-xs text-gray-400 mt-1">Start a conversation to see it here</p>
      </div>
    );
  }

  return (
    <div className="space-y-1">
      {conversations.map((conv) => (
        <div
          key={conv.id}
          className="group flex items-start gap-2 p-2 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
        >
          <Clock className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 truncate">{conv.title}</p>
            <p className="text-xs text-gray-500">{conv.date}</p>
          </div>
          <button
            onClick={(e) => deleteConversation(conv.id, e)}
            className="opacity-0 group-hover:opacity-100 p-1 hover:bg-gray-200 rounded transition-opacity"
          >
            <Trash2 className="w-3 h-3 text-gray-500" />
          </button>
        </div>
      ))}
    </div>
  );
};

export default ConversationHistory;

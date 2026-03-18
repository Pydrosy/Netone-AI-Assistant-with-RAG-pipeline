import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, Check, Copy } from 'lucide-react';

const MessageBubble = ({ message }) => {
  const [copied, setCopied] = React.useState(false);
  const isUser = message.role === 'user';

  const copyToClipboard = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex gap-3 mb-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
        isUser ? 'bg-primary-600' : 'bg-gray-300'
      }`}>
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-gray-700" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex-1 max-w-[80%] ${isUser ? 'flex justify-end' : ''}`}>
        <div
          className={`group relative ${
            isUser
              ? 'bg-primary-600 text-white rounded-2xl rounded-tr-none'
              : 'bg-white border border-gray-200 rounded-2xl rounded-tl-none'
          } px-4 py-2 shadow-sm`}
        >
          {/* Copy button */}
          <button
            onClick={copyToClipboard}
            className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
          >
            {copied ? (
              <Check className="w-4 h-4 text-green-500" />
            ) : (
              <Copy className="w-4 h-4 text-gray-400 hover:text-gray-600" />
            )}
          </button>

          {/* Message text with markdown support */}
          <div className={`prose prose-sm max-w-none ${
            isUser ? 'prose-invert' : ''
          }`}>
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>

          {/* Timestamp */}
          <div className={`text-xs mt-1 ${
            isUser ? 'text-primary-200' : 'text-gray-400'
          }`}>
            {new Date(message.timestamp).toLocaleTimeString()}
          </div>
        </div>

        {/* Sources */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-2 space-y-1">
            <p className="text-xs text-gray-500">Sources:</p>
            <div className="flex flex-wrap gap-2">
              {message.sources.map((source, idx) => (
                <span
                  key={idx}
                  className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full"
                  title={`Relevance: ${source.relevance}`}
                >
                  {source.title}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;

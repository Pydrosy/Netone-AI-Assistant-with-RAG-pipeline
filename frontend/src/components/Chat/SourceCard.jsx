import React from 'react';
import { FileText, ExternalLink } from 'lucide-react';

const SourceCard = ({ source }) => {
  return (
    <div className="source-card group">
      <div className="flex items-start gap-2">
        <FileText className="w-4 h-4 text-gray-400 mt-0.5 flex-shrink-0" />
        <div className="flex-1 min-w-0">
          <p className="font-medium text-gray-900 truncate">{source.title}</p>
          <p className="text-xs text-gray-500 mt-1">
            Relevance: {source.relevance} • {source.category}
          </p>
          {source.excerpt && (
            <p className="text-xs text-gray-600 mt-2 line-clamp-2">
              {source.excerpt}
            </p>
          )}
        </div>
        <ExternalLink className="w-4 h-4 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
      </div>
    </div>
  );
};

export default SourceCard;

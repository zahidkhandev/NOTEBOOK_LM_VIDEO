/**
 * File list component showing uploaded sources
 */

import React from "react";
import { Source } from "../../services/types";
import { Button } from "../Common/Button";

interface FileListProps {
  sources: Source[];
  onDelete: (sourceId: number) => void;
}

const statusConfig = {
  pending: {
    icon: "⏳",
    color: "text-yellow-600 dark:text-yellow-400",
    bg: "bg-yellow-50 dark:bg-yellow-900/20",
  },
  processing: {
    icon: "⚙️",
    color: "text-blue-600 dark:text-blue-400",
    bg: "bg-blue-50 dark:bg-blue-900/20",
  },
  ready: {
    icon: "✅",
    color: "text-green-600 dark:text-green-400",
    bg: "bg-green-50 dark:bg-green-900/20",
  },
  failed: {
    icon: "❌",
    color: "text-red-600 dark:text-red-400",
    bg: "bg-red-50 dark:bg-red-900/20",
  },
};

export const FileList: React.FC<FileListProps> = ({ sources, onDelete }) => {
  if (sources.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-5xl mb-4">📭</div>
        <p className="text-gray-600 dark:text-gray-400">
          No documents uploaded yet
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">
          Uploaded Sources
        </h2>
        <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
          {sources.length} file(s)
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {sources.map((source) => {
          const status =
            statusConfig[source.status as keyof typeof statusConfig];
          return (
            <div
              key={source.id}
              className={`p-4 rounded-lg border border-gray-200 dark:border-slate-700 ${status.bg}`}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <span className="text-2xl">📄</span>
                  <div className="min-w-0 flex-1">
                    <p className="font-semibold text-gray-900 dark:text-white truncate">
                      {source.filename}
                    </p>
                    <p
                      className={`text-sm font-medium flex items-center gap-1 ${status.color}`}
                    >
                      <span>{status.icon}</span>
                      <span className="capitalize">{source.status}</span>
                    </p>
                  </div>
                </div>
              </div>

              <div className="space-y-1 mb-4 text-sm text-gray-600 dark:text-gray-400">
                {source.word_count && (
                  <p>📝 {source.word_count.toLocaleString()} words</p>
                )}
                {source.page_count && <p>📄 {source.page_count} pages</p>}
                <p className="text-xs">
                  Added {new Date(source.created_at).toLocaleDateString()}
                </p>
              </div>

              <Button
                variant="danger"
                size="sm"
                onClick={() => onDelete(source.id)}
                className="w-full"
              >
                🗑️ Delete
              </Button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

/**
 * Progress bar component for video generation
 */

import React from "react";
import { GenerationStatus } from "../../services/types";

interface ProgressBarProps {
  status: GenerationStatus | null | undefined;
  videoId: number | null;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  status,
  videoId,
}) => {
  if (!videoId || !status) return null;

  const isComplete = status.status === "completed";
  const isFailed = status.status === "failed";
  const isCancelled = status.status === "cancelled";

  const statusMessages = {
    pending: "⏳ Waiting to start...",
    processing: "⚙️ Generating video...",
    completed: "✅ Video generated successfully!",
    failed: "❌ Generation failed",
    cancelled: "⚠️ Generation cancelled",
  };

  const statusColors = {
    pending:
      "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-200",
    processing:
      "bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-200",
    completed:
      "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-200",
    failed: "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-200",
    cancelled:
      "bg-orange-100 text-orange-800 dark:bg-orange-900/20 dark:text-orange-200",
  };

  return (
    <div className="space-y-4 p-6 bg-gray-50 dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700">
      {/* Status Badge */}
      <div
        className={`inline-block px-4 py-2 rounded-full text-sm font-semibold ${
          statusColors[status.status]
        }`}
      >
        {statusMessages[status.status]}
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium text-gray-900 dark:text-white">
            Progress
          </span>
          <span className="text-sm font-bold text-blue-600 dark:text-blue-400">
            {status.progress}%
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-3 overflow-hidden">
          <div
            className={`h-3 transition-all duration-500 ${
              isFailed
                ? "bg-red-600"
                : isComplete
                ? "bg-green-600"
                : isCancelled
                ? "bg-orange-600"
                : "bg-blue-600"
            }`}
            style={{ width: `${status.progress}%` }}
          />
        </div>
      </div>

      {/* Details */}
      <div className="space-y-1 text-sm">
        <p className="text-gray-700 dark:text-gray-300">
          <span className="font-semibold">Video ID:</span> {videoId}
        </p>
        {status.error && (
          <p className="text-red-600 dark:text-red-400">
            <span className="font-semibold">Error:</span> {status.error}
          </p>
        )}
        {status.message && (
          <p className="text-gray-700 dark:text-gray-300">
            <span className="font-semibold">Message:</span> {status.message}
          </p>
        )}
      </div>
    </div>
  );
};

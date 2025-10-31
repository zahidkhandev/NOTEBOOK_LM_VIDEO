/**
 * Individual video card component
 */

import React from "react";
import { Video } from "../../services/types";
import { Button } from "../Common/Button";

interface VideoCardProps {
  video: Video;
  onDelete: (videoId: number) => void;
  onDownload: (videoId: number) => void;
  onView: (videoId: number) => void;
  isDeletingId?: number | null;
  isDownloadingId?: number | null;
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
  completed: {
    icon: "✅",
    color: "text-green-600 dark:text-green-400",
    bg: "bg-green-50 dark:bg-green-900/20",
  },
  failed: {
    icon: "❌",
    color: "text-red-600 dark:text-red-400",
    bg: "bg-red-50 dark:bg-red-900/20",
  },
  cancelled: {
    icon: "⚠️",
    color: "text-orange-600 dark:text-orange-400",
    bg: "bg-orange-50 dark:bg-orange-900/20",
  },
};

export const VideoCard: React.FC<VideoCardProps> = ({
  video,
  onDelete,
  onDownload,
  onView,
  isDeletingId,
  isDownloadingId,
}) => {
  const status = statusConfig[video.status as keyof typeof statusConfig];
  const isDeleting = isDeletingId === video.id;
  const isDownloading = isDownloadingId === video.id;

  return (
    <div className="bg-white dark:bg-slate-800 rounded-lg border border-gray-200 dark:border-slate-700 overflow-hidden hover:shadow-lg transition-shadow">
      {/* Header with status */}
      <div
        className={`p-4 border-b border-gray-200 dark:border-slate-700 ${status.bg}`}
      >
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-bold text-lg text-gray-900 dark:text-white truncate flex-1">
            {video.title}
          </h3>
          <span className={`text-2xl ml-2 ${status.color}`}>{status.icon}</span>
        </div>
        <p className={`text-sm font-medium ${status.color}`}>
          {video.status.toUpperCase()}
        </p>
      </div>

      {/* Content */}
      <div className="p-4 space-y-3">
        {/* Description */}
        {video.description && (
          <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
            {video.description}
          </p>
        )}

        {/* Video details */}
        <div className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
          <p>
            <span className="font-medium">Duration:</span> {video.duration}s
          </p>
          <p>
            <span className="font-medium">Style:</span> {video.visual_style}
          </p>
          {video.target_audience && (
            <p>
              <span className="font-medium">Audience:</span>{" "}
              {video.target_audience}
            </p>
          )}
          {video.quality_score !== undefined && (
            <p>
              <span className="font-medium">Quality:</span>{" "}
              {video.quality_score.toFixed(1)}/10
            </p>
          )}
          <p className="text-xs">
            <span className="font-medium">Created:</span>{" "}
            {new Date(video.created_at).toLocaleDateString()}
          </p>
        </div>

        {/* Progress bar (if processing) */}
        {video.status === "processing" && (
          <div className="space-y-1">
            <div className="flex justify-between items-center text-xs">
              <span className="text-gray-600 dark:text-gray-400">Progress</span>
              <span className="font-bold text-blue-600">{video.progress}%</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${video.progress}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="px-4 py-3 border-t border-gray-200 dark:border-slate-700 bg-gray-50 dark:bg-slate-900 space-y-2">
        {video.status === "completed" && (
          <>
            <Button
              variant="primary"
              size="sm"
              onClick={() => onView(video.id)}
              className="w-full"
            >
              👁️ View Video
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => onDownload(video.id)}
              isLoading={isDownloading}
              disabled={isDownloading}
              className="w-full"
            >
              ⬇️ Download
            </Button>
          </>
        )}
        <Button
          variant="danger"
          size="sm"
          onClick={() => onDelete(video.id)}
          isLoading={isDeleting}
          disabled={isDeleting}
          className="w-full"
        >
          🗑️ Delete
        </Button>
      </div>
    </div>
  );
};

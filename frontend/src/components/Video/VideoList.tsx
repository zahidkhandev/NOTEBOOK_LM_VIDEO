/**
 * Video list component with filtering and pagination
 */

import React, { useState } from "react";
import { useVideos } from "../../services/hooks/useVideos";
import { LoadingSpinner } from "../Common/LoadingSpinner";
import { Button } from "../Common/Button";
import { VideoCard } from "./VideoCard";

export const VideoList: React.FC = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [statusFilter, setStatusFilter] = useState<string | undefined>();
  const itemsPerPage = 12;
  const skip = (currentPage - 1) * itemsPerPage;

  const {
    videos,
    total,
    isLoadingVideos,
    deleteVideo,
    isDeletingVideo,
    downloadVideo,
    isDownloading,
  } = useVideos(skip, itemsPerPage, statusFilter);

  const totalPages = Math.ceil(total / itemsPerPage);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Generated Videos
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          View, download, and manage your generated videos
        </p>
      </div>

      {/* Filters */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-3">
            Filter by Status
          </label>
          <div className="flex flex-wrap gap-2">
            <Button
              variant={!statusFilter ? "primary" : "outline"}
              size="sm"
              onClick={() => {
                setStatusFilter(undefined);
                setCurrentPage(1);
              }}
            >
              All Videos
            </Button>
            {["pending", "processing", "completed", "failed", "cancelled"].map(
              (status) => (
                <Button
                  key={status}
                  variant={statusFilter === status ? "primary" : "outline"}
                  size="sm"
                  onClick={() => {
                    setStatusFilter(status);
                    setCurrentPage(1);
                  }}
                >
                  {status.charAt(0).toUpperCase() + status.slice(1)}
                </Button>
              )
            )}
          </div>
        </div>

        {/* Results count */}
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Showing {videos.length > 0 ? skip + 1 : 0} -{" "}
          {Math.min(skip + itemsPerPage, total)} of {total} videos
        </p>
      </div>

      {/* Loading */}
      {isLoadingVideos ? (
        <div className="flex justify-center py-12">
          <LoadingSpinner text="Loading videos..." />
        </div>
      ) : videos.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-5xl mb-4">🎬</div>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            No videos generated yet
          </p>
          <p className="text-sm text-gray-500 dark:text-gray-500">
            Upload documents and generate videos to see them here
          </p>
        </div>
      ) : (
        <>
          {/* Video Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {videos.map((video) => (
              <VideoCard
                key={video.id}
                video={video}
                onDelete={deleteVideo}
                onDownload={downloadVideo}
                onView={(videoId) => {
                  // Navigate to video player page if needed
                  console.log("View video:", videoId);
                }}
                isDeletingId={isDeletingVideo ? video.id : null}
                isDownloadingId={isDownloading ? video.id : null}
              />
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-4 mt-8">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
              >
                ← Previous
              </Button>

              <div className="flex gap-2">
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(
                  (page) => (
                    <button
                      key={page}
                      onClick={() => setCurrentPage(page)}
                      className={`w-8 h-8 rounded font-medium transition-colors ${
                        currentPage === page
                          ? "bg-blue-600 text-white"
                          : "bg-gray-200 dark:bg-slate-700 text-gray-900 dark:text-white hover:bg-gray-300 dark:hover:bg-slate-600"
                      }`}
                    >
                      {page}
                    </button>
                  )
                )}
              </div>

              <Button
                variant="outline"
                size="sm"
                onClick={() =>
                  setCurrentPage((prev) => Math.min(totalPages, prev + 1))
                }
                disabled={currentPage === totalPages}
              >
                Next →
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

/**
 * Video player component
 */

import React from "react";
import { Video } from "../../services/types";

interface VideoPlayerProps {
  video: Video;
  onClose: () => void;
}

export const VideoPlayer: React.FC<VideoPlayerProps> = ({ video, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80">
      {/* Close button */}
      <button
        onClick={onClose}
        className="absolute top-4 right-4 text-white hover:text-gray-300 text-3xl z-10"
      >
        ✕
      </button>

      {/* Player container */}
      <div className="w-full max-w-4xl mx-4">
        {video.url ? (
          <>
            <video
              controls
              className="w-full rounded-lg shadow-2xl"
              controlsList="nodownload"
            >
              <source src={video.url} type="video/mp4" />
              Your browser does not support the video tag.
            </video>

            {/* Video Info */}
            <div className="mt-4 text-white space-y-2">
              <h2 className="text-2xl font-bold">{video.title}</h2>
              {video.description && (
                <p className="text-gray-300">{video.description}</p>
              )}
              <div className="text-sm text-gray-400 space-y-1">
                <p>Duration: {video.duration}s</p>
                <p>Style: {video.visual_style}</p>
                {video.quality_score !== undefined && (
                  <p>Quality Score: {video.quality_score.toFixed(1)}/10</p>
                )}
              </div>
            </div>
          </>
        ) : (
          <div className="bg-gray-900 rounded-lg p-12 text-center text-white">
            <div className="text-5xl mb-4">🚫</div>
            <p>Video URL not available</p>
            <p className="text-sm text-gray-400 mt-2">
              The video file may still be processing
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

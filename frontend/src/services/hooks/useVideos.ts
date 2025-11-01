/**
 * Custom hook for video management
 */

import { useCallback } from "react";
import { useMutation, useQuery, useQueryClient } from "react-query";
import { videoAPI } from "../api";
import { useToast } from "./useToast";

export const useVideos = (
  skip: number = 0,
  limit: number = 20,
  statusFilter?: string
) => {
  const queryClient = useQueryClient();
  const { success: successToast, error: errorToast } = useToast();

  // Fetch videos list
  const videosQuery = useQuery(
    ["videos", skip, limit, statusFilter],
    () => {
      const filters = statusFilter ? { statusFilter } : undefined;
      return videoAPI.list(skip, limit, filters);
    },
    {
      refetchInterval: 5000,
      staleTime: 2000,
    }
  );

  const getVideo = useCallback(
    (videoId: number) => {
      return queryClient.fetchQuery(["video", videoId], () =>
        videoAPI.get(videoId)
      );
    },
    [queryClient]
  );

  // Delete video mutation
  const deleteVideoMutation = useMutation(
    (videoId: number) => videoAPI.delete(videoId),
    {
      onSuccess: () => {
        successToast("Video deleted successfully");
        queryClient.invalidateQueries("videos");
      },
      onError: (error: Error) => {
        // ✅ TYPED ERROR
        errorToast(error.message || "Failed to delete video");
      },
    }
  );

  // Download video mutation
  const downloadVideoMutation = useMutation(
    (videoId: number) => videoAPI.getDownloadUrl(videoId),
    {
      onSuccess: (data) => {
        if (data.download_url) {
          // ✅ CORRECT FIELD NAME
          const link = document.createElement("a");
          link.href = data.download_url;
          link.download = `video-${Date.now()}.mp4`;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          successToast("Download started");
        }
      },
      onError: (error: Error) => {
        // ✅ TYPED ERROR
        errorToast(error.message || "Failed to download video");
      },
    }
  );

  const deleteVideo = useCallback(
    (videoId: number) => {
      if (window.confirm("Are you sure you want to delete this video?")) {
        deleteVideoMutation.mutate(videoId);
      }
    },
    [deleteVideoMutation]
  );

  const downloadVideo = useCallback(
    (videoId: number) => {
      downloadVideoMutation.mutate(videoId);
    },
    [downloadVideoMutation]
  );

  return {
    videos: videosQuery.data?.videos || [],
    total: videosQuery.data?.total || 0,
    isLoadingVideos: videosQuery.isLoading,
    refetchVideos: videosQuery.refetch,
    getVideo,
    deleteVideo,
    isDeletingVideo: deleteVideoMutation.isLoading,
    downloadVideo,
    isDownloading: downloadVideoMutation.isLoading,
  };
};

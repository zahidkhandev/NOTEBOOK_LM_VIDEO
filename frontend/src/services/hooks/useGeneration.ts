/**
 * Custom hook for video generation
 */

import { useState, useCallback } from "react";
import { useMutation, useQuery, useQueryClient } from "react-query";
import { generationAPI } from "../api";
import {
  GenerationRequest,
  GenerationResponse,
  GenerationStatus,
} from "../types";
import { useToast } from "./useToast";

export const useGeneration = () => {
  const queryClient = useQueryClient();
  const { success: successToast, error: errorToast } = useToast();
  const [generatedVideoId, setGeneratedVideoId] = useState<number | null>(null);
  const [isPolling, setIsPolling] = useState(false);

  // Fetch templates
  const templatesQuery = useQuery(
    ["templates"],
    () => generationAPI.getTemplates(),
    {
      staleTime: 60000,
    }
  );

  // Start generation mutation
  const startGenerationMutation = useMutation(
    (payload: GenerationRequest) => generationAPI.start(payload),
    {
      onSuccess: (data: GenerationResponse) => {
        setGeneratedVideoId(data.video_id);
        setIsPolling(true);
        successToast("Video generation started");
        queryClient.invalidateQueries("videos");
      },
      onError: (error: any) => {
        errorToast(error.message || "Failed to start generation");
      },
    }
  );

  // Fetch generation status
  const statusQuery = useQuery(
    ["generationStatus", generatedVideoId],
    () => (generatedVideoId ? generationAPI.getStatus(generatedVideoId) : null),
    {
      enabled: !!generatedVideoId && isPolling,
      refetchInterval: 2000,
      staleTime: 500,
      onSuccess: (data: GenerationStatus | null) => {
        if (
          data &&
          (data.status === "completed" ||
            data.status === "failed" ||
            data.status === "cancelled")
        ) {
          setIsPolling(false);
          if (data.status === "completed") {
            successToast("Video generation completed!");
          } else if (data.status === "failed") {
            errorToast(`Generation failed: ${data.error || "Unknown error"}`);
          }
        }
      },
    }
  );

  // Cancel generation mutation
  const cancelMutation = useMutation(
    (videoId: number) => generationAPI.cancel(videoId),
    {
      onSuccess: () => {
        setIsPolling(false);
        setGeneratedVideoId(null);
        successToast("Generation cancelled");
        queryClient.invalidateQueries("videos");
      },
      onError: (error: any) => {
        errorToast(error.message || "Failed to cancel generation");
      },
    }
  );

  const startGeneration = useCallback(
    (payload: GenerationRequest) => {
      startGenerationMutation.mutate(payload);
    },
    [startGenerationMutation]
  );

  const cancelGeneration = useCallback(() => {
    if (generatedVideoId) {
      cancelMutation.mutate(generatedVideoId);
    }
  }, [generatedVideoId, cancelMutation]);

  const reset = useCallback(() => {
    setGeneratedVideoId(null);
    setIsPolling(false);
  }, []);

  return {
    templates: templatesQuery.data || [],
    isLoadingTemplates: templatesQuery.isLoading,
    startGeneration,
    isGenerating: startGenerationMutation.isLoading,
    generatedVideoId,
    generationStatus: statusQuery.data,
    isPolling,
    cancelGeneration,
    isCancelling: cancelMutation.isLoading,
    reset,
  };
};

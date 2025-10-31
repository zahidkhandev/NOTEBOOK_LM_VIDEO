/**
 * Custom hook for file upload functionality
 */

import { useState, useCallback } from "react";
import { useMutation, useQuery, useQueryClient } from "react-query";
import { sourceAPI } from "../api";
import { UploadProgress } from "../types";
import { useToast } from "./useToast";

export const useUpload = () => {
  const queryClient = useQueryClient();
  const { error: errorToast } = useToast();
  const [uploadProgress, setUploadProgress] = useState<
    Record<string, UploadProgress>
  >({});

  // Upload mutation
  const uploadMutation = useMutation(
    (file: File) =>
      sourceAPI.upload(file, (progress) => {
        setUploadProgress((prev) => ({
          ...prev,
          [file.name]: { filename: file.name, progress, status: "uploading" },
        }));
      }),
    {
      onSuccess: (data) => {
        setUploadProgress((prev) => ({
          ...prev,
          [data.filename]: {
            filename: data.filename,
            progress: 100,
            status: "completed",
          },
        }));
        queryClient.invalidateQueries("sources");
        setTimeout(() => {
          setUploadProgress((prev) => {
            const newProgress = { ...prev };
            delete newProgress[data.filename];
            return newProgress;
          });
        }, 2000);
      },
      onError: (error: any, file) => {
        setUploadProgress((prev) => ({
          ...prev,
          [file.name]: { filename: file.name, progress: 0, status: "failed" },
        }));
        errorToast(error.message || "Upload failed");
      },
    }
  );

  // Fetch sources list
  const sourcesQuery = useQuery(["sources"], () => sourceAPI.list(0, 100), {
    refetchInterval: 5000,
    staleTime: 2000,
  });

  // Delete source mutation
  const deleteSourceMutation = useMutation(
    (sourceId: number) => sourceAPI.delete(sourceId),
    {
      onSuccess: () => {
        queryClient.invalidateQueries("sources");
      },
      onError: (error: any) => {
        errorToast(error.message || "Failed to delete source");
      },
    }
  );

  const upload = useCallback(
    (file: File) => {
      const validExtensions = [".pdf", ".docx", ".txt"];
      const isValidFile = validExtensions.some((ext) =>
        file.name.toLowerCase().endsWith(ext)
      );

      if (!isValidFile) {
        errorToast("Only PDF, DOCX, and TXT files are supported");
        return;
      }

      if (file.size > 50 * 1024 * 1024) {
        errorToast("File size must be less than 50MB");
        return;
      }

      uploadMutation.mutate(file);
    },
    [uploadMutation, errorToast]
  );

  return {
    upload,
    isUploading: uploadMutation.isLoading,
    uploadProgress: Object.values(uploadProgress),
    sources: sourcesQuery.data?.sources || [],
    isLoadingSources: sourcesQuery.isLoading,
    deleteSource: deleteSourceMutation.mutate,
    isDeletingSource: deleteSourceMutation.isLoading,
  };
};

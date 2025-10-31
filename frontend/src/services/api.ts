/**
 * API client for NotebookLM Video Generator
 * Handles all HTTP requests to backend
 */

import axios, { AxiosInstance, AxiosError } from "axios";
import {
  Source,
  Video,
  GenerationRequest,
  GenerationResponse,
  GenerationStatus,
  Template,
  ApiResponse,
} from "./types";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      console.error("Unauthorized");
    }
    if (error.response?.status === 500) {
      console.error("Server error");
    }
    return Promise.reject(error);
  }
);

/**
 * Source API endpoints
 */
export const sourceAPI = {
  /**
   * Upload a source document
   */
  upload: async (
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<Source> => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post<Source>("/sources/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onProgress(percentCompleted);
          }
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(`Upload failed: ${extractErrorMessage(error)}`);
    }
  },

  /**
   * List all sources with pagination
   */
  list: async (
    skip: number = 0,
    limit: number = 20
  ): Promise<{ sources: Source[]; total: number }> => {
    try {
      const response = await api.get<
        ApiResponse<{ sources: Source[]; total: number }>
      >("/sources/", {
        params: { skip, limit },
      });
      return response.data.data || { sources: [], total: 0 };
    } catch (error) {
      throw new Error(`Failed to list sources: ${extractErrorMessage(error)}`);
    }
  },

  /**
   * Get source details
   */
  get: async (sourceId: number): Promise<Source> => {
    try {
      const response = await api.get<Source>(`/sources/${sourceId}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch source: ${extractErrorMessage(error)}`);
    }
  },

  /**
   * Delete source
   */
  delete: async (sourceId: number): Promise<void> => {
    try {
      await api.delete(`/sources/${sourceId}`);
    } catch (error) {
      throw new Error(`Failed to delete source: ${extractErrorMessage(error)}`);
    }
  },
};

/**
 * Video API endpoints
 */
export const videoAPI = {
  /**
   * List all videos with filters
   */
  list: async (
    skip: number = 0,
    limit: number = 20,
    statusFilter?: string
  ): Promise<{ videos: Video[]; total: number }> => {
    try {
      const params: Record<string, any> = { skip, limit };
      if (statusFilter) params.status_filter = statusFilter;

      const response = await api.get<
        ApiResponse<{ videos: Video[]; total: number }>
      >("/videos/", { params });
      return response.data.data || { videos: [], total: 0 };
    } catch (error) {
      throw new Error(`Failed to list videos: ${extractErrorMessage(error)}`);
    }
  },

  /**
   * Get video details
   */
  get: async (videoId: number): Promise<Video> => {
    try {
      const response = await api.get<Video>(`/videos/${videoId}`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch video: ${extractErrorMessage(error)}`);
    }
  },

  /**
   * Get video download URL
   */
  getDownloadUrl: async (videoId: number): Promise<{ url: string }> => {
    try {
      const response = await api.get<{ url: string }>(
        `/videos/${videoId}/download`
      );
      return response.data;
    } catch (error) {
      throw new Error(
        `Failed to get download URL: ${extractErrorMessage(error)}`
      );
    }
  },

  /**
   * Delete video
   */
  delete: async (videoId: number): Promise<void> => {
    try {
      await api.delete(`/videos/${videoId}`);
    } catch (error) {
      throw new Error(`Failed to delete video: ${extractErrorMessage(error)}`);
    }
  },
};

/**
 * Generation API endpoints
 */
export const generationAPI = {
  /**
   * Start video generation
   */
  start: async (payload: GenerationRequest): Promise<GenerationResponse> => {
    try {
      const response = await api.post<GenerationResponse>(
        "/generate/start",
        payload
      );
      return response.data;
    } catch (error) {
      throw new Error(
        `Failed to start generation: ${extractErrorMessage(error)}`
      );
    }
  },

  /**
   * Get generation status
   */
  getStatus: async (videoId: number): Promise<GenerationStatus> => {
    try {
      const response = await api.get<GenerationStatus>(
        `/generate/status/${videoId}`
      );
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch status: ${extractErrorMessage(error)}`);
    }
  },

  /**
   * Cancel generation
   */
  cancel: async (videoId: number): Promise<void> => {
    try {
      await api.post(`/generate/cancel/${videoId}`);
    } catch (error) {
      throw new Error(
        `Failed to cancel generation: ${extractErrorMessage(error)}`
      );
    }
  },

  /**
   * Analyze content
   */
  analyze: async (sourceId: number): Promise<any> => {
    try {
      const response = await api.post(`/generate/analyze/${sourceId}`);
      return response.data;
    } catch (error) {
      throw new Error(
        `Failed to analyze content: ${extractErrorMessage(error)}`
      );
    }
  },

  /**
   * Get available templates/styles
   */
  getTemplates: async (): Promise<Template[]> => {
    try {
      const response = await api.get<Template[]>("/generate/templates");
      return Array.isArray(response.data) ? response.data : [];
    } catch (error) {
      throw new Error(
        `Failed to fetch templates: ${extractErrorMessage(error)}`
      );
    }
  },
};

/**
 * Utility function to extract error messages
 */
function extractErrorMessage(error: any): string {
  if (axios.isAxiosError(error)) {
    return (
      error.response?.data?.message ||
      error.response?.data?.error ||
      error.message ||
      "Unknown error"
    );
  }
  return error?.message || "Unknown error occurred";
}

export default api;

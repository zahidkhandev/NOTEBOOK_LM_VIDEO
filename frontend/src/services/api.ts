/**
 * API client for NotebookLM Video Generator
 * Handles all HTTP requests to backend - 5 CHANNEL SUPPORT
 */

import axios, { AxiosInstance, AxiosError } from "axios";
import {
  Source,
  Video,
  GenerationRequest,
  GenerationResponse,
  GenerationStatus,
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

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      console.error("❌ Unauthorized - please log in");
    }
    if (error.response?.status === 500) {
      console.error("❌ Server error");
    }
    return Promise.reject(error);
  }
);

// Error response type
interface ErrorResponse {
  message?: string;
  detail?: string;
  error?: string;
}

// Utility function to extract error messages
function extractErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as ErrorResponse | undefined;
    return (
      data?.message ||
      data?.detail ||
      data?.error ||
      error.message ||
      "Unknown error"
    );
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "Unknown error occurred";
}

// ═════════════════════════════════════════════════════════════════════════════
// SOURCE API - Upload & manage documents
// ═════════════════════════════════════════════════════════════════════════════

interface SourceListResponse {
  sources?: Source[];
  total: number;
  skip: number;
  limit: number;
}

export const sourceAPI = {
  /**
   * List all uploaded sources
   */
  list: async (skip: number = 0, limit: number = 100): Promise<Source[]> => {
    try {
      const response = await api.get<SourceListResponse>("/sources/", {
        params: { skip, limit },
      });
      return response.data.sources || [];
    } catch (error) {
      throw new Error(`Failed to list sources: ${extractErrorMessage(error)}`);
    }
  },

  /**
   * Upload a new source document (PDF, DOCX, TXT)
   */
  upload: async (
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<Source> => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post<Source>("/sources/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (event) => {
          if (event.total && onProgress) {
            const progress = Math.round((event.loaded * 100) / event.total);
            onProgress(progress);
          }
        },
      });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to upload source: ${extractErrorMessage(error)}`);
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
   * Delete a source
   */
  delete: async (sourceId: number): Promise<void> => {
    try {
      await api.delete(`/sources/${sourceId}`);
    } catch (error) {
      throw new Error(`Failed to delete source: ${extractErrorMessage(error)}`);
    }
  },
};

// ═════════════════════════════════════════════════════════════════════════════
// VIDEO API - Manage generated videos
// ═════════════════════════════════════════════════════════════════════════════

interface VideoListResponse {
  videos: Video[];
  total: number;
  skip: number;
  limit: number;
  channel_id?: string;
}

interface VideoFilters {
  channelId?: string;
  statusFilter?: string;
}

export const videoAPI = {
  /**
   * List all videos with optional filtering by channel or status
   */
  list: async (
    skip: number = 0,
    limit: number = 20,
    filters?: VideoFilters
  ): Promise<VideoListResponse> => {
    try {
      const params: Record<string, unknown> = { skip, limit };
      if (filters?.channelId) params.channel_id = filters.channelId;
      if (filters?.statusFilter) params.status_filter = filters.statusFilter;

      const response = await api.get<VideoListResponse>("/videos/", {
        params,
      });

      return response.data;
    } catch (error) {
      throw new Error(`Failed to list videos: ${extractErrorMessage(error)}`);
    }
  },

  /**
   * Get video details by ID
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
  getDownloadUrl: async (
    videoId: number
  ): Promise<{ download_url: string; filename: string }> => {
    try {
      const response = await api.get<{
        download_url: string;
        filename: string;
      }>(`/videos/${videoId}/download`);
      return response.data;
    } catch (error) {
      throw new Error(
        `Failed to get download URL: ${extractErrorMessage(error)}`
      );
    }
  },

  /**
   * Delete a video
   */
  delete: async (videoId: number): Promise<void> => {
    try {
      await api.delete(`/videos/${videoId}`);
    } catch (error) {
      throw new Error(`Failed to delete video: ${extractErrorMessage(error)}`);
    }
  },
};

// ═════════════════════════════════════════════════════════════════════════════
// GENERATION API - Generate videos for 5 channels
// ═════════════════════════════════════════════════════════════════════════════

interface ConceptType {
  name: string;
  confidence: number;
  category?: string;
  description?: string;
}

interface AnalysisResponse {
  source_id: number;
  concepts: ConceptType[];
  total_concepts: number;
}

interface Channel {
  id: string;
  name: string;
  description: string;
  default_duration: number;
  video_style: string;
  tone: string;
  audience: string[];
}

interface TemplatesResponse {
  channels: Channel[];
}

export const generationAPI = {
  /**
   * Start video generation for one of 5 channels
   * - research_papers: AI/Tech/Biotech research
   * - space_exploration: Animated space stories
   * - brainrot_grandfather: Grandfather brain rot
   * - brainrot_stories: Afirmax-style character stories
   * - kids_brainrot: Kids silly stories
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
   * Get video generation status with real-time progress
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
   * Cancel ongoing video generation
   */
  cancel: async (
    videoId: number
  ): Promise<{ status: string; video_id: number }> => {
    try {
      const response = await api.post<{
        status: string;
        video_id: number;
      }>(`/generate/cancel/${videoId}`);
      return response.data;
    } catch (error) {
      throw new Error(
        `Failed to cancel generation: ${extractErrorMessage(error)}`
      );
    }
  },

  /**
   * Analyze content from source to extract concepts
   */
  analyze: async (sourceId: number): Promise<AnalysisResponse> => {
    try {
      const response = await api.post<AnalysisResponse>(
        `/generate/analyze/${sourceId}`
      );
      return response.data;
    } catch (error) {
      throw new Error(
        `Failed to analyze content: ${extractErrorMessage(error)}`
      );
    }
  },

  /**
   * Get all available channels and their configurations
   */
  getTemplates: async (): Promise<TemplatesResponse> => {
    try {
      const response = await api.get<TemplatesResponse>("/generate/templates");
      return response.data;
    } catch (error) {
      throw new Error(
        `Failed to fetch templates: ${extractErrorMessage(error)}`
      );
    }
  },

  /**
   * Upload character image for grandfather channel
   * LOCAL STORAGE ONLY - no cloud uploads
   */
  uploadCharacterImage: async (
    channelId: string,
    file: File
  ): Promise<{ channel_id: string; image_path: string; message: string }> => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post<{
        channel_id: string;
        image_path: string;
        message: string;
      }>(`/generate/upload-character/${channelId}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      return response.data;
    } catch (error) {
      throw new Error(
        `Failed to upload character image: ${extractErrorMessage(error)}`
      );
    }
  },
};

// ═════════════════════════════════════════════════════════════════════════════
// CHARACTER API - Manage reusable characters (local storage)
// ═════════════════════════════════════════════════════════════════════════════

interface CharacterUploadResponse {
  channel_id: string;
  character: string;
  image_path: string;
}

export const characterAPI = {
  /**
   * Upload character image for local storage
   * For: brainrot_grandfather, brainrot_stories, kids_brainrot
   */
  uploadImage: async (
    channelId: string,
    file: File
  ): Promise<CharacterUploadResponse> => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post<CharacterUploadResponse>(
        `/generate/upload-character/${channelId}`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      return response.data;
    } catch (error) {
      throw new Error(
        `Failed to upload character: ${extractErrorMessage(error)}`
      );
    }
  },
};

export default api;

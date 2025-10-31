/**
 * TypeScript types for NotebookLM Video Generator frontend
 */

export interface Source {
  id: number;
  filename: string;
  file_type: string;
  status: "pending" | "processing" | "ready" | "failed";
  word_count?: number;
  page_count?: number;
  created_at: string;
  updated_at: string;
}

export interface Video {
  id: number;
  title: string;
  description?: string;
  duration: number;
  status: "pending" | "processing" | "completed" | "failed" | "cancelled";
  progress: number;
  visual_style: "classic" | "whiteboard" | "watercolor" | "anime";
  url?: string;
  quality_score?: number;
  created_at: string;
  completed_at?: string;
  source_ids?: number[];
  target_audience?: "child" | "teen" | "adult";
}

export interface GenerationRequest {
  title: string;
  description?: string;
  duration: number;
  visual_style: "classic" | "whiteboard" | "watercolor" | "anime";
  source_ids: number[];
  target_audience?: "child" | "teen" | "adult";
  learning_objectives?: string[];
}

export interface GenerationResponse {
  video_id: number;
  status: string;
  progress: number;
  job_id?: string;
  message: string;
}

export interface GenerationStatus {
  video_id: number;
  status: "pending" | "processing" | "completed" | "failed" | "cancelled";
  progress: number;
  error?: string;
  message?: string;
}

export interface Template {
  name: string;
  id: string;
  description: string;
  thumbnail?: string;
  icon?: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
  status?: number;
}

export interface ToastMessage {
  id: string;
  type: "success" | "error" | "info" | "warning";
  message: string;
  duration?: number;
}

export interface UploadProgress {
  filename: string;
  progress: number;
  status: "uploading" | "completed" | "failed";
}

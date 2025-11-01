/**
 * TypeScript types for NotebookLM Video Generator frontend
 * UPDATED FOR 5-CHANNEL SUPPORT
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
  visual_style?: "classic" | "whiteboard" | "watercolor" | "anime";
  channel_id?: string;
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
  source_ids: number[];

  // 5-CHANNEL SUPPORT
  channel_id: string; // NEW: research_papers|space_exploration|brainrot_grandfather|brainrot_stories|kids_brainrot
  custom_prompt?: string; // NEW: custom prompt overlay

  // OPTIONAL (for backwards compatibility)
  visual_style?: "classic" | "whiteboard" | "watercolor" | "anime";
  target_audience?: "child" | "teen" | "adult";
  learning_objectives?: string[];
}

export interface GenerationResponse {
  video_id: number;
  channel_id: string;
  status: string;
  progress: number;
  job_id?: string;
  message: string;
}

export interface GenerationStatus {
  video_id: number;
  channel_id?: string;
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

// NEW: Channel info type
export interface Channel {
  id: string;
  label: string;
  description: string;
  icon: string;
  duration: number;
  hasCharacterUpload?: boolean;
}

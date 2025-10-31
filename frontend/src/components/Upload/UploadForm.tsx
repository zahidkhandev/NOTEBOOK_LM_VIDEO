/**
 * File upload form component with drag-drop
 */

import React, { useRef, useState } from "react";
import { useUpload } from "../../services/hooks/useUpload";
import { LoadingSpinner } from "../Common/LoadingSpinner";
import { FileList } from "./FileList";

export const UploadForm: React.FC = () => {
  const { upload, uploadProgress, sources, isLoadingSources, deleteSource } =
    useUpload();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(e.type === "dragenter" || e.type === "dragover");
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    files.forEach((file) => upload(file));
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    files.forEach((file) => upload(file));
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Upload Documents
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Upload PDF, DOCX, or TXT files to create video content from
        </p>
      </div>

      {/* Drag Drop Area */}
      <div
        className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${
          dragActive
            ? "border-blue-600 bg-blue-50 dark:bg-blue-900/20"
            : "border-gray-300 dark:border-slate-600 hover:border-blue-400 dark:hover:border-blue-500"
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.docx,.txt"
          onChange={handleFileSelect}
          style={{ display: "none" }}
        />

        <div className="space-y-3">
          <div className="text-5xl">📁</div>
          <div>
            <p className="text-lg font-semibold text-gray-900 dark:text-white">
              Drop files here to upload
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              or click to browse your computer
            </p>
          </div>
          <p className="text-xs text-gray-400 dark:text-gray-500">
            Supported formats: PDF, DOCX, TXT (Max 50MB per file)
          </p>
        </div>
      </div>

      {/* Upload Progress */}
      {uploadProgress.length > 0 && (
        <div className="space-y-3">
          <h3 className="font-semibold text-gray-900 dark:text-white">
            Uploading...
          </h3>
          {uploadProgress.map((progress) => (
            <div key={progress.filename} className="space-y-1">
              <div className="flex justify-between items-center">
                <p className="text-sm text-gray-700 dark:text-gray-300">
                  {progress.filename}
                </p>
                <span className="text-sm font-medium text-blue-600">
                  {progress.progress}%
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-slate-700 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress.progress}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Files List */}
      {isLoadingSources ? (
        <LoadingSpinner text="Loading sources..." />
      ) : (
        <FileList sources={sources} onDelete={deleteSource} />
      )}
    </div>
  );
};

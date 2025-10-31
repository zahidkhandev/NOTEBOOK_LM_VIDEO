/**
 * Video generation form component
 */

import React, { useState, useEffect } from "react";
import { useUpload } from "../../services/hooks/useUpload";
import { useGeneration } from "../../services/hooks/useGeneration";
import { useToast } from "../../services/hooks/useToast";
import { Button } from "../Common/Button";
import { LoadingSpinner } from "../Common/LoadingSpinner";
import { StyleSelector } from "./StyleSelector";
import { ProgressBar } from "./ProgressBar";
import { GenerationRequest } from "../../services/types";

export const GenerationForm: React.FC = () => {
  const { sources } = useUpload();
  const {
    templates,
    isLoadingTemplates,
    startGeneration,
    isGenerating,
    generatedVideoId,
    generationStatus,
    isPolling,
    cancelGeneration,
    isCancelling,
    reset,
  } = useGeneration();
  const { warning } = useToast();

  const [formData, setFormData] = useState<GenerationRequest>({
    title: "",
    description: "",
    duration: 300,
    visual_style: "classic",
    source_ids: [],
    target_audience: "adult",
  });

  const [showSourceSelect, setShowSourceSelect] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.source_ids.length === 0) {
      warning("Please select at least one source document");
      return;
    }

    if (!formData.title.trim()) {
      warning("Please enter a video title");
      return;
    }

    startGeneration(formData);
  };

  const handleSourceToggle = (sourceId: number) => {
    setFormData((prev) => ({
      ...prev,
      source_ids: prev.source_ids.includes(sourceId)
        ? prev.source_ids.filter((id) => id !== sourceId)
        : [...prev.source_ids, sourceId],
    }));
  };

  const handleReset = () => {
    reset();
    setFormData({
      title: "",
      description: "",
      duration: 300,
      visual_style: "classic",
      source_ids: [],
      target_audience: "adult",
    });
  };

  // Auto-scroll to progress bar
  useEffect(() => {
    if (generatedVideoId) {
      document
        .getElementById("progress-section")
        ?.scrollIntoView({ behavior: "smooth" });
    }
  }, [generatedVideoId]);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Generate Video
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Create an educational video from your uploaded documents
        </p>
      </div>

      {/* Progress Section */}
      {generatedVideoId && (
        <div id="progress-section">
          <ProgressBar status={generationStatus} videoId={generatedVideoId} />
        </div>
      )}

      {/* Form */}
      {!isPolling && (
        <form
          onSubmit={handleSubmit}
          className="space-y-6 bg-white dark:bg-slate-800 p-6 rounded-lg border border-gray-200 dark:border-slate-700"
        >
          {/* Title */}
          <div>
            <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
              Video Title *
            </label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) =>
                setFormData({ ...formData, title: e.target.value })
              }
              placeholder="Enter video title"
              className="w-full px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600"
              required
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
              Description
            </label>
            <textarea
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
              placeholder="Enter video description (optional)"
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-600"
            />
          </div>

          {/* Duration */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                Duration (seconds)
              </label>
              <input
                type="number"
                min="60"
                max="600"
                step="10"
                value={formData.duration}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    duration: parseInt(e.target.value),
                  })
                }
                className="w-full px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
              />
              <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
                Between 1-10 minutes
              </p>
            </div>

            {/* Target Audience */}
            <div>
              <label className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                Target Audience
              </label>
              <select
                value={formData.target_audience || "adult"}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    target_audience: e.target.value as any,
                  })
                }
                className="w-full px-4 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-600"
              >
                <option value="child">Child (5-11)</option>
                <option value="teen">Teen (12-17)</option>
                <option value="adult">Adult (18+)</option>
              </select>
            </div>
          </div>

          {/* Style Selector */}
          {isLoadingTemplates ? (
            <LoadingSpinner size="sm" text="Loading styles..." />
          ) : (
            <StyleSelector
              selected={formData.visual_style}
              templates={templates}
              onChange={(style) =>
                setFormData({ ...formData, visual_style: style })
              }
            />
          )}

          {/* Source Selection */}
          <div>
            <div className="flex justify-between items-center mb-3">
              <label className="block text-sm font-semibold text-gray-900 dark:text-white">
                Source Documents * ({formData.source_ids.length} selected)
              </label>
              <button
                type="button"
                onClick={() => setShowSourceSelect(!showSourceSelect)}
                className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
              >
                {showSourceSelect ? "Hide" : "Select"}
              </button>
            </div>

            {showSourceSelect && (
              <div className="space-y-2 mb-4">
                {sources.length === 0 ? (
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    No sources available. Please upload documents first.
                  </p>
                ) : (
                  sources
                    .filter((s) => s.status === "ready")
                    .map((source) => (
                      <label
                        key={source.id}
                        className="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-700 cursor-pointer"
                      >
                        <input
                          type="checkbox"
                          checked={formData.source_ids.includes(source.id)}
                          onChange={() => handleSourceToggle(source.id)}
                          className="w-4 h-4 rounded cursor-pointer"
                        />
                        <div className="flex-1">
                          <p className="font-medium text-gray-900 dark:text-white">
                            {source.filename}
                          </p>
                          <p className="text-xs text-gray-500 dark:text-gray-400">
                            {source.word_count} words
                          </p>
                        </div>
                      </label>
                    ))
                )}
              </div>
            )}

            {formData.source_ids.length > 0 && (
              <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <p className="text-sm text-blue-800 dark:text-blue-200">
                  Selected:{" "}
                  {sources
                    .filter((s) => formData.source_ids.includes(s.id))
                    .map((s) => s.filename)
                    .join(", ")}
                </p>
              </div>
            )}
          </div>

          {/* Buttons */}
          <div className="flex gap-3 pt-4">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              isLoading={isGenerating}
              disabled={isGenerating}
              className="flex-1"
            >
              🎬 Generate Video
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={handleReset}
              disabled={isGenerating}
              className="flex-1"
            >
              Reset
            </Button>
          </div>
        </form>
      )}

      {/* Cancel Button */}
      {isPolling && (
        <Button
          variant="danger"
          size="lg"
          onClick={cancelGeneration}
          isLoading={isCancelling}
          className="w-full"
        >
          Cancel Generation
        </Button>
      )}
    </div>
  );
};

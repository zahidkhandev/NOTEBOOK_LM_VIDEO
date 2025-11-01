import React, { useState } from "react";
import { useMutation, useQuery } from "react-query";
import { generationAPI, sourceAPI } from "../../services/api";
import { GenerationRequest, Source } from "../../services/types";

interface ChannelConfig {
  id: string;
  label: string;
  description: string;
  icon: string;
  duration: number;
  hasCharacterUpload?: boolean;
}

const CHANNELS: ChannelConfig[] = [
  {
    id: "research_papers",
    label: "🔬 Research Papers",
    description: "AI/Tech/Biotech research explained",
    icon: "🔬",
    duration: 60,
  },
  {
    id: "space_exploration",
    label: "🚀 Space & Exploration",
    description: "Animated space stories",
    icon: "🚀",
    duration: 60,
  },
  {
    id: "brainrot_grandfather",
    label: "👴 Brain Rot: Grandpa",
    description: "Absurd grandfather stories",
    icon: "👴",
    duration: 45,
    hasCharacterUpload: true,
  },
  {
    id: "brainrot_stories",
    label: "🎭 Brain Rot: Stories",
    description: "Quirky character stories",
    icon: "🎭",
    duration: 60,
  },
  {
    id: "kids_brainrot",
    label: "🎈 Kids Edition",
    description: "Silly funny stories",
    icon: "🎈",
    duration: 45,
  },
];

export const GenerationForm: React.FC = () => {
  const [formData, setFormData] = useState<GenerationRequest>({
    title: "",
    channel_id: "research_papers",
    custom_prompt: "",
    duration: 60,
    source_ids: [],
  });

  const [selectedChannel, setSelectedChannel] = useState<ChannelConfig>(
    CHANNELS[0]
  );
  const [characterImage, setCharacterImage] = useState<File | null>(null);
  const [characterImagePreview, setCharacterImagePreview] =
    useState<string>("");
  const [generatedVideoId, setGeneratedVideoId] = useState<number | null>(null);
  const [progress, setProgress] = useState(0);

  const sourcesQuery = useQuery(["sources"], () => sourceAPI.list());

  const uploadCharacterMutation = useMutation(
    async (file: File) =>
      generationAPI.uploadCharacterImage(formData.channel_id, file),
    {
      onSuccess: () => {
        alert("✅ Character image stored!");
        setCharacterImage(null);
        setCharacterImagePreview("");
      },
    }
  );

  const generateMutation = useMutation(
    (payload: GenerationRequest) => generationAPI.start(payload),
    {
      onSuccess: (data) => {
        setGeneratedVideoId(data.video_id);
        pollProgress(data.video_id);
      },
      onError: (error: Error) => {
        alert("❌ " + (error.message || "Generation failed"));
      },
    }
  );

  const pollProgress = async (videoId: number): Promise<void> => {
    const interval = setInterval(async () => {
      try {
        const status = await generationAPI.getStatus(videoId);
        setProgress(status.progress);
        if (["completed", "failed", "cancelled"].includes(status.status)) {
          clearInterval(interval);
        }
      } catch (error) {
        clearInterval(interval);
      }
    }, 2000);
  };

  const handleChannelChange = (channelId: string): void => {
    const channel = CHANNELS.find((c) => c.id === channelId);
    if (channel) {
      setSelectedChannel(channel);
      setFormData({
        ...formData,
        channel_id: channelId,
        duration: channel.duration,
      });
    }
  };

  const handleCharacterImageChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ): void => {
    const file = e.target.files?.[0];
    if (file) {
      setCharacterImage(file);
      setCharacterImagePreview(URL.createObjectURL(file));
    }
  };

  const handleUploadCharacter = async (): Promise<void> => {
    if (!characterImage) {
      alert("Please select an image");
      return;
    }
    uploadCharacterMutation.mutate(characterImage);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
    if (formData.source_ids.length === 0) {
      alert("Please select at least one source document");
      return;
    }
    generateMutation.mutate(formData);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="mb-12 text-center">
          <h1 className="text-5xl font-bold text-white mb-3 drop-shadow-lg">
            🎬 Generate Your Video
          </h1>
          <p className="text-lg text-slate-300">
            Create educational videos with AI-powered scripts
          </p>
        </div>

        {!generatedVideoId ? (
          <>
            <div className="mb-12">
              <h2 className="text-3xl font-bold text-white mb-6">
                Choose Your Channel
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3">
                {CHANNELS.map((channel) => (
                  <button
                    key={channel.id}
                    onClick={() => handleChannelChange(channel.id)}
                    className={`p-5 rounded-xl border-2 transition-all duration-300 transform hover:scale-110 flex flex-col items-center gap-2 ${
                      selectedChannel.id === channel.id
                        ? "border-blue-400 bg-blue-600 shadow-xl shadow-blue-500/50"
                        : "border-slate-600 bg-slate-700 hover:border-blue-400"
                    }`}
                  >
                    <span className="text-3xl">{channel.icon}</span>
                    <p className="font-bold text-white text-sm">
                      {channel.label.split(" ")[0]}
                    </p>
                    <p className="text-xs text-slate-200">
                      {channel.description}
                    </p>
                  </button>
                ))}
              </div>
            </div>

            {selectedChannel.hasCharacterUpload && (
              <div className="mb-12 bg-gradient-to-br from-amber-900 to-amber-800 border-2 border-amber-500 rounded-2xl p-8 shadow-xl">
                <h3 className="text-2xl font-bold text-white mb-2">
                  👴 Upload Grandfather Character
                </h3>
                <p className="text-amber-100 mb-6">
                  Upload an image to use as your grandfather character
                </p>
                <label className="block">
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleCharacterImageChange}
                    className="hidden"
                    id="character-image-input"
                  />
                  <div className="border-3 border-dashed border-amber-400 rounded-xl p-8 text-center cursor-pointer hover:bg-amber-700/50 transition bg-amber-800/30">
                    <div className="text-5xl mb-3">📸</div>
                    <label
                      htmlFor="character-image-input"
                      className="cursor-pointer font-bold text-amber-300"
                    >
                      {characterImage
                        ? "✅ Image Selected"
                        : "Click to select image"}
                    </label>
                    <p className="text-sm text-amber-200 mt-2">
                      PNG, JPG, GIF up to 10MB
                    </p>
                  </div>
                </label>
                {characterImagePreview && (
                  <div className="mt-6 text-center">
                    <img
                      src={characterImagePreview}
                      alt="preview"
                      className="w-40 h-40 mx-auto rounded-xl shadow-lg mb-4 object-cover"
                    />
                    <button
                      onClick={handleUploadCharacter}
                      disabled={uploadCharacterMutation.isLoading}
                      className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition disabled:bg-gray-600"
                    >
                      {uploadCharacterMutation.isLoading
                        ? "⏳ Storing..."
                        : "✅ Store Character"}
                    </button>
                  </div>
                )}
              </div>
            )}

            <form
              onSubmit={handleSubmit}
              className="bg-slate-800 rounded-2xl shadow-2xl p-10 border border-slate-700 space-y-8"
            >
              <div>
                <label className="block text-lg font-bold text-white mb-3">
                  Video Title
                </label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) =>
                    setFormData({ ...formData, title: e.target.value })
                  }
                  placeholder="e.g., End-to-End Language Models"
                  required
                  className="w-full px-4 py-3 bg-slate-700 border-2 border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 transition"
                />
              </div>

              <div>
                <label className="block text-lg font-bold text-white mb-3">
                  Duration (seconds)
                </label>
                <input
                  type="number"
                  min="30"
                  max="600"
                  value={formData.duration}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      duration: parseInt(e.target.value, 10),
                    })
                  }
                  className="w-full px-4 py-3 bg-slate-700 border-2 border-slate-600 rounded-lg text-white focus:outline-none focus:border-blue-500 transition"
                />
              </div>

              <div>
                <label className="block text-lg font-bold text-white mb-3">
                  📄 Select Source Documents
                </label>
                <div className="border-2 border-slate-600 rounded-lg bg-slate-700 max-h-64 overflow-y-auto">
                  {sourcesQuery.isLoading ? (
                    <p className="text-slate-400 p-4">Loading sources...</p>
                  ) : !sourcesQuery.data?.length ? (
                    <p className="text-slate-400 p-4">
                      No sources uploaded yet. Upload one first!
                    </p>
                  ) : (
                    <div className="p-4 space-y-3">
                      {sourcesQuery.data?.map((source: Source) => (
                        <label
                          key={source.id}
                          className="flex items-center gap-3 p-4 hover:bg-slate-600 rounded-lg cursor-pointer transition bg-slate-800"
                        >
                          <input
                            type="checkbox"
                            checked={formData.source_ids.includes(source.id)}
                            onChange={(e) => {
                              setFormData({
                                ...formData,
                                source_ids: e.target.checked
                                  ? [...formData.source_ids, source.id]
                                  : formData.source_ids.filter(
                                      (id) => id !== source.id
                                    ),
                              });
                            }}
                            className="w-5 h-5 text-blue-600 rounded cursor-pointer"
                          />
                          <div className="flex-1">
                            <p className="font-semibold text-white">
                              {source.filename}
                            </p>
                            <p className="text-xs text-slate-400">
                              {source.word_count?.toLocaleString()} words
                            </p>
                          </div>
                        </label>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              <div>
                <label className="block text-lg font-bold text-white mb-3">
                  Custom Prompt (Optional)
                </label>
                <textarea
                  value={formData.custom_prompt || ""}
                  onChange={(e) =>
                    setFormData({ ...formData, custom_prompt: e.target.value })
                  }
                  placeholder="Add custom instructions..."
                  rows={4}
                  className="w-full px-4 py-3 bg-slate-700 border-2 border-slate-600 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 transition resize-none"
                />
              </div>

              <button
                type="submit"
                disabled={
                  generateMutation.isLoading ||
                  !formData.title ||
                  formData.source_ids.length === 0
                }
                className="w-full py-4 px-6 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-bold text-lg rounded-lg transition transform hover:scale-105 disabled:bg-gray-600 disabled:cursor-not-allowed disabled:scale-100 shadow-lg hover:shadow-xl"
              >
                {generateMutation.isLoading
                  ? "⏳ Generating Video..."
                  : "🎬 Generate Video"}
              </button>
            </form>
          </>
        ) : (
          <div className="bg-slate-800 rounded-2xl shadow-2xl p-12 text-center border border-slate-700 max-w-2xl mx-auto">
            <h2 className="text-4xl font-bold text-white mb-8">
              ⏳ Generating Your Video
            </h2>
            <div className="mb-10">
              <div className="w-full bg-slate-700 rounded-full h-12 overflow-hidden mb-4 shadow-lg">
                <div
                  className="bg-gradient-to-r from-blue-500 to-blue-400 h-full flex items-center justify-center text-white font-bold text-xl transition-all duration-300 shadow-inner"
                  style={{ width: `${progress}%` }}
                >
                  {progress}%
                </div>
              </div>
              <p className="text-slate-300 text-sm">
                {progress < 30 && "🔄 Analyzing content..."}
                {progress >= 30 && progress < 60 && "✍️ Generating script..."}
                {progress >= 60 && progress < 90 && "🎬 Rendering video..."}
                {progress >= 90 && "🎉 Finalizing..."}
              </p>
            </div>
            <div className="space-y-4 text-slate-300 mb-8">
              <p>
                <span className="font-bold text-white">Video ID:</span>{" "}
                <span className="text-blue-400">#{generatedVideoId}</span>
              </p>
              <p>
                <span className="font-bold text-white">Channel:</span>{" "}
                {selectedChannel.label}
              </p>
              <p className="text-sm pt-4">
                This typically takes 2-5 minutes. You can close this page!
              </p>
            </div>
            <button
              onClick={() => (window.location.href = `/videos`)}
              className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition shadow-lg hover:shadow-xl"
            >
              📹 View All Videos
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

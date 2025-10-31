/**
 * Home page - Landing page
 */

import React from "react";
import { Link } from "react-router-dom";
import { Button } from "../components/Common/Button";

export const HomePage: React.FC = () => {
  const features = [
    {
      icon: "📁",
      title: "Upload Documents",
      description: "Upload PDF, DOCX, and TXT files to extract content",
    },
    {
      icon: "🎬",
      title: "Generate Videos",
      description: "Create educational videos with AI-powered generation",
    },
    {
      icon: "🎨",
      title: "Choose Styles",
      description:
        "Select from multiple visual styles (classic, whiteboard, watercolor, anime)",
    },
    {
      icon: "📊",
      title: "Track Progress",
      description:
        "Monitor video generation in real-time with live progress updates",
    },
    {
      icon: "⬇️",
      title: "Download Videos",
      description: "Download your generated videos in high quality",
    },
    {
      icon: "👥",
      title: "Target Audiences",
      description: "Customize content for children, teens, or adults",
    },
  ];

  const steps = [
    {
      number: "1️⃣",
      title: "Upload Your Content",
      description: "Start by uploading your source documents (PDF, DOCX, TXT)",
    },
    {
      number: "2️⃣",
      title: "Configure Video",
      description: "Set title, duration, style, and target audience",
    },
    {
      number: "3️⃣",
      title: "Generate Video",
      description: "AI generates the video from your content",
    },
    {
      number: "4️⃣",
      title: "Download & Share",
      description: "Download your video and share with others",
    },
  ];

  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <section className="text-center space-y-6 py-12">
        <div className="text-6xl">🎬</div>
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white">
          Transform Documents into Videos
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          NotebookLM Video Generator uses AI to create engaging educational
          videos from your documents
        </p>
        <div className="flex gap-4 justify-center flex-wrap">
          <Link to="/upload">
            <Button variant="primary" size="lg">
              📁 Get Started
            </Button>
          </Link>
          <a href="#features">
            <Button variant="outline" size="lg">
              Learn More
            </Button>
          </a>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
            Features
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Everything you need to generate amazing videos
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div
              key={index}
              className="p-6 rounded-lg border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:shadow-lg transition-shadow"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
            How It Works
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Simple 4-step process to create your video
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {steps.map((step, index) => (
            <div key={index} className="relative">
              <div className="p-6 rounded-lg border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-center">
                <div className="text-5xl mb-4">{step.number}</div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                  {step.title}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {step.description}
                </p>
              </div>

              {/* Arrow between steps */}
              {index < steps.length - 1 && (
                <div className="hidden lg:flex absolute -right-3 top-1/2 transform -translate-y-1/2 text-2xl text-blue-600">
                  →
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl p-12 text-center text-white space-y-4">
        <h2 className="text-3xl font-bold">Ready to Create?</h2>
        <p className="text-xl opacity-90 max-w-xl mx-auto">
          Start generating amazing educational videos from your documents right
          now
        </p>
        <Link to="/upload">
          <Button
            variant="secondary"
            size="lg"
            className="!bg-white !text-blue-600 hover:!bg-gray-100"
          >
            📁 Upload Documents
          </Button>
        </Link>
      </section>

      {/* Stats Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 py-12 text-center">
        <div className="space-y-2">
          <p className="text-3xl font-bold text-blue-600">∞</p>
          <p className="text-gray-600 dark:text-gray-400">Unlimited Videos</p>
        </div>
        <div className="space-y-2">
          <p className="text-3xl font-bold text-blue-600">4</p>
          <p className="text-gray-600 dark:text-gray-400">Visual Styles</p>
        </div>
        <div className="space-y-2">
          <p className="text-3xl font-bold text-blue-600">3</p>
          <p className="text-gray-600 dark:text-gray-400">Target Audiences</p>
        </div>
      </section>
    </div>
  );
};

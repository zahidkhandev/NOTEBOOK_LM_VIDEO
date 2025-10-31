/**
 * Header component with navigation
 */

import React from "react";
import { Link } from "react-router-dom";
import { useDarkMode } from "../../services/hooks/useDarkMode";

export const Header: React.FC = () => {
  const { isDark, toggle } = useDarkMode();

  return (
    <header className="sticky top-0 z-40 bg-white dark:bg-slate-800 border-b border-gray-200 dark:border-slate-700 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link
            to="/"
            className="flex items-center gap-2 text-2xl font-bold text-blue-600"
          >
            <span>🎬</span>
            <span className="hidden sm:inline">NotebookLM Video</span>
            <span className="sm:hidden">NBLMVideo</span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <Link
              to="/"
              className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              Home
            </Link>
            <Link
              to="/upload"
              className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              Upload
            </Link>
            <Link
              to="/generate"
              className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              Generate
            </Link>
            <Link
              to="/videos"
              className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              Videos
            </Link>
          </nav>

          {/* Dark mode toggle */}
          <button
            onClick={toggle}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-slate-700 transition-colors"
            aria-label="Toggle dark mode"
          >
            {isDark ? "☀️" : "🌙"}
          </button>
        </div>

        {/* Mobile navigation */}
        <nav className="md:hidden pb-4 flex gap-4 overflow-x-auto">
          <Link to="/" className="px-3 py-2 text-sm font-medium text-blue-600">
            Home
          </Link>
          <Link
            to="/upload"
            className="px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Upload
          </Link>
          <Link
            to="/generate"
            className="px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Generate
          </Link>
          <Link
            to="/videos"
            className="px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300"
          >
            Videos
          </Link>
        </nav>
      </div>
    </header>
  );
};

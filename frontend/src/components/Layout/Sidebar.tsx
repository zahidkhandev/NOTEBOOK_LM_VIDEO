/**
 * Sidebar component
 */

import React from "react";
import { Link, useLocation } from "react-router-dom";

interface SidebarLink {
  label: string;
  href: string;
  icon: string;
}

const links: SidebarLink[] = [
  { label: "Dashboard", href: "/", icon: "📊" },
  { label: "Upload", href: "/upload", icon: "📁" },
  { label: "Generate", href: "/generate", icon: "🎬" },
  { label: "Videos", href: "/videos", icon: "🎥" },
];

export const Sidebar: React.FC = () => {
  const location = useLocation();

  return (
    <aside className="hidden lg:flex flex-col w-64 bg-white dark:bg-slate-800 border-r border-gray-200 dark:border-slate-700 h-[calc(100vh-4rem)]">
      <nav className="flex-1 px-4 py-8 space-y-2">
        {links.map((link) => {
          const isActive = location.pathname === link.href;
          return (
            <Link
              key={link.href}
              to={link.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200"
                  : "text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-slate-700"
              }`}
            >
              <span className="text-xl">{link.icon}</span>
              <span className="font-medium">{link.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer info */}
      <div className="px-4 py-4 border-t border-gray-200 dark:border-slate-700">
        <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
          © 2025 NotebookLM Video Generator
        </p>
      </div>
    </aside>
  );
};

/**
 * Video style selector component
 */

import React from "react";
import { Template } from "../../services/types";

type VisualStyle = "classic" | "whiteboard" | "watercolor" | "anime";

interface StyleSelectorProps {
  selected: VisualStyle;
  templates: Template[];
  onChange: (style: VisualStyle) => void;
  isLoading?: boolean;
}

const defaultStyles: Array<{
  id: VisualStyle;
  name: string;
  description: string;
  icon: string;
}> = [
  {
    id: "classic",
    name: "Classic",
    description: "Traditional presentation style with smooth transitions",
    icon: "📊",
  },
  {
    id: "whiteboard",
    name: "Whiteboard",
    description: "Hand-drawn whiteboard animation style",
    icon: "✏️",
  },
  {
    id: "watercolor",
    name: "Watercolor",
    description: "Artistic watercolor painting aesthetic",
    icon: "🎨",
  },
  {
    id: "anime",
    name: "Anime",
    description: "Anime-inspired animation style",
    icon: "🎌",
  },
];

export const StyleSelector: React.FC<StyleSelectorProps> = ({
  selected,
  templates,
  onChange,
  isLoading = false,
}) => {
  const styles = templates.length > 0 ? templates : defaultStyles;

  return (
    <div className="space-y-3">
      <label className="block text-sm font-semibold text-gray-900 dark:text-white">
        Visual Style
      </label>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {styles.map((style) => (
          <button
            key={style.id}
            onClick={() => onChange(style.id as VisualStyle)}
            disabled={isLoading}
            type="button"
            className={`p-4 rounded-lg border-2 transition-all ${
              selected === style.id
                ? "border-blue-600 bg-blue-50 dark:bg-blue-900/20"
                : "border-gray-200 dark:border-slate-700 hover:border-blue-400 dark:hover:border-blue-500"
            } ${
              isLoading ? "opacity-50 cursor-not-allowed" : "cursor-pointer"
            }`}
          >
            <div className="text-3xl mb-2">{style.icon}</div>
            <p className="font-semibold text-gray-900 dark:text-white text-sm">
              {style.name}
            </p>
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
              {style.description || style.id}
            </p>
          </button>
        ))}
      </div>
    </div>
  );
};

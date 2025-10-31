/**
 * Toast notification component
 */

import React, { useEffect } from "react";
import { ToastMessage } from "../../services/types";

interface ToastProps extends ToastMessage {
  onRemove: (id: string) => void;
}

export const Toast: React.FC<ToastProps> = ({
  id,
  type,
  message,
  duration,
  onRemove,
}) => {
  useEffect(() => {
    if (duration && duration > 0) {
      const timer = setTimeout(() => onRemove(id), duration);
      return () => clearTimeout(timer);
    }
  }, [id, duration, onRemove]);

  const bgColorMap = {
    success: "bg-green-100 text-green-800 border-green-300",
    error: "bg-red-100 text-red-800 border-red-300",
    info: "bg-blue-100 text-blue-800 border-blue-300",
    warning: "bg-yellow-100 text-yellow-800 border-yellow-300",
  };

  const iconMap = {
    success: "✅",
    error: "❌",
    info: "ℹ️",
    warning: "⚠️",
  };

  return (
    <div
      className={`${bgColorMap[type]} border-l-4 p-4 rounded-md shadow-md flex items-center gap-3 animate-slide-in`}
      role="alert"
    >
      <span className="text-xl">{iconMap[type]}</span>
      <p className="flex-1 font-medium">{message}</p>
      <button
        onClick={() => onRemove(id)}
        className="text-xl hover:opacity-70 transition-opacity"
      >
        ✕
      </button>
    </div>
  );
};

interface ToastContainerProps {
  toasts: ToastMessage[];
  onRemove: (id: string) => void;
}

export const ToastContainer: React.FC<ToastContainerProps> = ({
  toasts,
  onRemove,
}) => {
  return (
    <div className="fixed bottom-4 right-4 space-y-3 z-50 max-w-md">
      {toasts.map((toast) => (
        <Toast key={toast.id} {...toast} onRemove={onRemove} />
      ))}
    </div>
  );
};

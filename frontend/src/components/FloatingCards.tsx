import React, { useEffect, useState } from "react";

const messages = [
  {
    title: "📈 Increase Yields",
    body: "Boost productivity by 15-25% through precision agriculture and data-driven decisions.",
    color: "from-green-100 to-green-200",
  },
  {
    title: "💰 Reduce Costs",
    body: "Save on inputs with optimized resource allocation and targeted applications.",
    color: "from-blue-100 to-blue-200",
  },
  {
    title: "🌱 Early Detection",
    body: "Detect stress before it's visible with continuous satellite monitoring.",
    color: "from-yellow-100 to-yellow-200",
  },
  {
    title: "📊 Smart Decisions",
    body: "Actionable insights backed by satellite data, AI, and historical trends.",
    color: "from-purple-100 to-purple-200",
  },
];

const FloatingCards: React.FC = () => {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const t = setInterval(() => {
      setIndex((i) => (i + 1) % messages.length);
    }, 4500);
    return () => clearInterval(t);
  }, []);

  const msg = messages[index];

  return (
    <div
      aria-hidden
      className="fixed right-6 bottom-10 z-50 w-80 pointer-events-none"
    >
      <div
        className={`pointer-events-auto rounded-lg shadow-xl overflow-hidden transform transition-all duration-500 ease-out`}
        style={{ willChange: "transform, opacity" }}
      >
        <div
          className={`p-4 bg-linear-to-r ${msg.color} border border-gray-200`}
        >
          <h4 className="text-sm font-semibold text-gray-800">{msg.title}</h4>
          <p className="text-xs text-gray-700 mt-2">{msg.body}</p>
        </div>
      </div>
    </div>
  );
};

export default FloatingCards;

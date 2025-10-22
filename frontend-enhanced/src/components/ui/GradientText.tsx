import React from "react";

interface Props {
  text: string;
  className?: string;
  from?: string;
  to?: string;
}

export const GradientText: React.FC<Props> = ({
  text,
  className = "",
  from = "#41ff2c",
  to = "#2eb9ff",
}) => {
  return (
    <span
      className={className}
      style={{
        background: `linear-gradient(90deg, ${from}, ${to})`,
        WebkitBackgroundClip: "text",
        backgroundClip: "text",
        color: "transparent",
      }}
    >
      {text}
    </span>
  );
};

export default GradientText;

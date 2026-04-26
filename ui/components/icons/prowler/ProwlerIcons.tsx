import React from "react";

import { IconSvgProps } from "../../../types/index";

// AzCSPM wordmark logo (full). Uses currentColor so it inherits the
// existing `text-prowler-black dark:text-prowler-white` theme tokens that the
// surrounding layout relies on.
export const ProwlerExtended: React.FC<IconSvgProps> = ({
  size,
  width = 216,
  height,
  ...props
}) => {
  return (
    <svg
      className="text-prowler-black dark:text-prowler-white"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 540 120"
      fill="none"
      height={size || height}
      width={size || width}
      {...props}
    >
      <text
        x="0"
        y="92"
        fontFamily="Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
        fontWeight="800"
        fontSize="100"
        letterSpacing="-3"
        fill="currentColor"
      >
        AzCSPM
      </text>
    </svg>
  );
};

// AzCSPM short mark used in collapsed sidebar / avatars.
export const ProwlerShort: React.FC<IconSvgProps> = ({
  size,
  width = 30,
  height,
  ...props
}) => (
  <svg
    className="text-prowler-black dark:text-prowler-white"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 120 120"
    fill="none"
    height={size || height}
    width={size || width}
    {...props}
  >
    <rect
      x="4"
      y="4"
      width="112"
      height="112"
      rx="22"
      fill="currentColor"
    />
    <text
      x="60"
      y="84"
      textAnchor="middle"
      fontFamily="Inter, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
      fontWeight="800"
      fontSize="78"
      letterSpacing="-2"
      fill="white"
      className="dark:fill-black"
    >
      A
    </text>
  </svg>
);

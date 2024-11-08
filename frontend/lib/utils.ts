import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

type Keypoint = [number, number, number]; // x, y, confidence
type FrameKeypoints = Keypoint[];

const limbConnections: [number, number][] = [
  [0, 1],
  [0, 2],
  [1, 3],
  [2, 4],
  [5, 6],
  [5, 7],
  [7, 9],
  [6, 8],
  [8, 10],
  [11, 12],
  [5, 11],
  [6, 12],
  [11, 13],
  [13, 15],
  [12, 14],
  [14, 16],
];

const normalizeKeypoints = (
  keypoints: [number, number][],
  width: number,
  height: number,
  padding: number
): [number, number][] => {
  const allX = keypoints.map((kp) => kp[0]);
  const allY = keypoints.map((kp) => kp[1]);

  const minX = Math.min(...allX);
  const maxX = Math.max(...allX);
  const minY = Math.min(...allY);
  const maxY = Math.max(...allY);

  // Reduce the drawing area by padding and calculate aspect ratio
  const availableWidth = width - 2 * padding;
  const availableHeight = height - 2 * padding;

  const scaleX = availableWidth / (maxX - minX);
  const scaleY = availableHeight / (maxY - minY);
  const scale = Math.min(scaleX, scaleY); // Use the smaller scale to maintain aspect ratio

  // Center the skeleton within the available area
  const offsetX = (availableWidth - (maxX - minX) * scale) / 2 + padding;
  const offsetY = (availableHeight - (maxY - minY) * scale) / 2 + padding;

  return keypoints.map(([x, y]) => [
    (x - minX) * scale + offsetX, // Scale and offset x
    (y - minY) * scale + offsetY, // Scale and offset y
  ]);
};


export {cn, limbConnections, normalizeKeypoints};
export type {Keypoint, FrameKeypoints}
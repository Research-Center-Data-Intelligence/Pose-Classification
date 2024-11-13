import { useState, useRef, useEffect } from "react";
import { InputFile } from "./file-picker";
import { Button } from "./ui/button";
import { select } from "d3";
import { Slider } from "@/components/ui/slider";
import { Label } from "./ui/label";
import {
  limbConnections,
  normalizeKeypoints,
  FrameKeypoints,
  Keypoint,
} from "@/lib/utils";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const VisualizeCard = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const [keypoints, setKeypoints] = useState<FrameKeypoints[]>([]);
  const [animationSpeed, setAnimationSpeed] = useState<number>(120);
  const animationRef = useRef<number | null>(null);

  const handleClearClick = () => {
    setKeypoints([]);
    if (svgRef.current) {
      select(svgRef.current).selectAll("*").remove();
    }
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleVisualizeClick = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://127.0.0.1:8000/keypoints", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload and process the file");
      }

      const data = await response.json();
      if (data.keypoints) {
        setKeypoints(data.keypoints);
        console.log(data.keypoints);
      } else {
        console.error("Error loading keypoints:", data.error);
      }
    } catch (error) {
      console.error("Failed to upload file:", error);
    }
  };

  useEffect(() => {
    if (!keypoints.length || !svgRef.current) return;

    const svg = select(svgRef.current);
    const width = 500;
    const height = 500;

    // Clear previous content
    svg.selectAll("*").remove();

    svg
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("width", width)
      .attr("height", height);

    const drawFrame = (frameKeypoints: Keypoint[]) => {
      const normalizedKeypoints = normalizeKeypoints(
        frameKeypoints.map((kp) => [kp[0], kp[1]]), // Take only the x and y coordinates
        width,
        height,
        24
      );

      svg.selectAll("*").remove();

      // Draw points
      svg
        .selectAll("circle")
        .data(normalizedKeypoints)
        .join("circle")
        .attr("r", 5)
        .attr("fill", "red")
        .attr("cx", (d) => d[0])
        .attr("cy", (d) => d[1]);

      // Draw limbs
      limbConnections.forEach(([start, end]) => {
        svg
          .append("line")
          .attr("x1", normalizedKeypoints[start][0])
          .attr("y1", normalizedKeypoints[start][1])
          .attr("x2", normalizedKeypoints[end][0])
          .attr("y2", normalizedKeypoints[end][1])
          .attr("stroke", "blue")
          .attr("stroke-width", 2);

        svg
          .append("text")
          .attr("x", 10)
          .attr("y", height - 10)
          .attr("fill", "red")
          .attr("font-size", "12px")
          .text(`FRAME: ${frameIndex + 1}`);
      });
    };

    let frameIndex = 0;
    let lastTime = 0;

    const animate = (timestamp: number) => {
      const timeSinceLastFrame = timestamp - lastTime;

      if (timeSinceLastFrame >= 1000 / animationSpeed) {
        drawFrame(keypoints[frameIndex]);
        frameIndex = (frameIndex + 1) % keypoints.length;
        lastTime = timestamp;
      }

      animationRef.current = requestAnimationFrame(animate);
    };

    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
    }

    animationRef.current = requestAnimationFrame(animate);

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, [keypoints, animationSpeed]);

  return (
    <div className="flex space-x-4">
      <Card className="w-[350px] h-[252px] overflow-hidden">
        <CardHeader>
          <CardTitle>3D Keypoint Sequence Visualizer</CardTitle>
          <CardDescription>
            Upload sequence data to visualize human motion.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <InputFile onFileChange={handleFileChange} />
              </div>
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="ghost" onClick={handleClearClick}>
            Clear
          </Button>
          <Button onClick={handleVisualizeClick} className="w-full ml-4">
            Visualize
          </Button>
        </CardFooter>
      </Card>
      <div className="flex-shrink-0">
        {keypoints.length > 0 && (
          <>
            <svg ref={svgRef} className="border rounded-xl mb-4"></svg>
            <div className="flex items-center space-x-2">
              <Label htmlFor="speed">FPS</Label>
              <Slider
                id="speed"
                defaultValue={[animationSpeed]}
                min={2}
                max={240}
                step={1}
                onValueChange={(value) => setAnimationSpeed(value[0])}
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export { VisualizeCard };

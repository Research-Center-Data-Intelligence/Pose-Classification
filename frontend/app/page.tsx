"use client";

import { Button } from "@/components/ui/button";
import { ModeToggle } from "@/components/mode-toggle";
import { PredictCard } from "@/components/predict-card";
import { VisualizeCard } from "@/components/visualize-card";
import { useState } from "react";

const Home = () => {
  const [selectedComponent, setSelectedComponent] = useState<
    "predict" | "visualize"
  >("predict");

  return (
    <main className="h-screen flex flex-col">
      <div className="flex flex-row p-4 justify-between">
        <div className="space-x-2">
          <Button
            variant="ghost"
            disabled={selectedComponent === "predict"}
            onClick={() => setSelectedComponent("predict")}
          >
            Predict
          </Button>
          <Button
            variant="ghost"
            disabled={selectedComponent === "visualize"}
            onClick={() => setSelectedComponent("visualize")}
          >
            Visualize
          </Button>
        </div>
        <div>
          <ModeToggle />
        </div>
      </div>
      <div className="flex-grow flex items-center justify-center p-4">
        {selectedComponent === "predict" && <PredictCard />}
        {selectedComponent === "visualize" && <VisualizeCard />}
      </div>
    </main>
  );
};

export default Home;

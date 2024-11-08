import { useState } from "react";
import { InputFile } from "./file-picker";
import { Button } from "./ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const predictionMapping: { [key: string]: string } = {
  HEAD_LIFT: "Head lift",
  LEG_RAISE: "Leg raise",
  ARM_RAISE: "Arm raise",
  SUPINE_TO_PRONE: "Supine to prone",
  CHAIR_RAISE_AND_STEP: "Chair raise and step",
  PICK_UP: "Pick up",
  SIT_ALL_FOURS_RISE: "Seated to all fours to rise",
  SIT_UP: "Sit up",
};

const PredictCard = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedNN, setSelectedNN] = useState<string>("lstm");
  const [prediction, setPrediction] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handlePredictClick = async () => {
    setPrediction(null);
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("architecture", selectedNN);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed upload failed.");
      }

      const data = await response.json();
      const mappedPrediction =
        predictionMapping[data.prediction] || data.prediction;
      setPrediction(mappedPrediction);
    } catch (error) {
      console.error(error);
      setPrediction("Error");
    }
  };

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>CMAS Exercise Recognition</CardTitle>
        <CardDescription>
          Upload your data and get a prediction.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="nn">Neural network architecture</Label>
              <Select onValueChange={setSelectedNN} value={selectedNN}>
                <SelectTrigger id="nn">
                  <SelectValue placeholder="Select" />
                </SelectTrigger>
                <SelectContent position="popper">
                  <SelectItem value="lstm">
                    Long short-term memory (LSTM)
                  </SelectItem>
                  <SelectItem value="gnn">
                    Graph neural network (GNN)
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="flex flex-col space-y-1.5">
              <InputFile onFileChange={handleFileChange} />
            </div>
          </div>
        </form>
      </CardContent>
      <CardFooter className="flex justify-between">
        <p style={{ visibility: prediction ? "visible" : "hidden" }}>
          Prediction:{" "}
          <span
            className={`font-bold mr-4 inline-block ${
              prediction === "Error" ? "text-red-500" : "text-green-500"
            }`}
          >
            {prediction}
          </span>
        </p>
        <Button onClick={handlePredictClick}>Predict</Button>
      </CardFooter>
    </Card>
  );
};

export { PredictCard };

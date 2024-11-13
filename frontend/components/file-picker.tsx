import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface InputFileProps {
  onFileChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const InputFile = ({ onFileChange }: InputFileProps) => {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5">
      <Label htmlFor="pth-file">
        Sequence file <span className="font-bold">(.pth)</span>
      </Label>
      <Input id="pth-file" type="file" accept=".pth" onChange={onFileChange} />
    </div>
  );
};

export { InputFile };

from utils import load_sequence, normalize_keypoints, label_map
from model_utils import load_model, prepare_input
import torch
from torch.nn.utils.rnn import pack_padded_sequence


def predict(sequence_path, model_weights, device="cpu"):
    sequence = load_sequence(sequence_path)
    normalized_keypoints = normalize_keypoints(sequence)

    keypoints_padded, sequence_length, perm_idx = prepare_input(
        normalized_keypoints, device
    )

    model = load_model(
        input_size=34,
        hidden_size=512,
        num_classes=8,
        model_weights=model_weights,
        device=device,
    )
    model.eval()

    packed_input = pack_padded_sequence(
        keypoints_padded, sequence_length.cpu(), batch_first=True
    )

    with torch.no_grad():
        output = model(packed_input)
        _, predicted_class = torch.max(output.data, 1)

    index_to_label = {v: k for k, v in label_map.items()}
    predicted_label = index_to_label[predicted_class.item()]
    return predicted_label


def api_prediction(target):
    model_weights = "weights/512M100_Model.pth"
    device = "cpu"

    return predict(sequence_path=target, model_weights=model_weights, device=device)


def main():
    target = "unseen_kps/1_Q.pth"
    model_weights = "weights/512M100_Model.pth"

    device = "cpu"
    predicted_label = predict(
        sequence_path=target, model_weights=model_weights, device=device
    )

    print(f"Prediction: {predicted_label}")


if __name__ == "__main__":
    main()

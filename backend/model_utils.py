import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_sequence


class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, packed_seq):
        packed_output, (hn, cn) = self.lstm(packed_seq)
        out = self.fc(hn[-1])
        return out


def load_model(input_size, hidden_size, num_classes, model_weights, device):
    model = LSTMModel(input_size, hidden_size, num_classes)
    model.load_state_dict(
        torch.load(model_weights, weights_only=True, map_location=device)
    )
    model.to(device)
    return model


def prepare_input(normalized_keypoints, device):
    keypoints_tensor = [torch.tensor(normalized_keypoints, dtype=torch.float32)]
    keypoints_tensor = [kp.view(len(kp), -1) for kp in keypoints_tensor]
    sequence_length = torch.tensor([len(keypoints_tensor[0])], dtype=torch.long)
    keypoints_padded = pad_sequence(keypoints_tensor, batch_first=True)

    # Sorting sequences by length (needed for packing)
    sequence_length, perm_idx = sequence_length.sort(0, descending=True)
    keypoints_padded = keypoints_padded[perm_idx]

    keypoints_padded = keypoints_padded.to(device)
    sequence_length = sequence_length.to(device)

    return keypoints_padded, sequence_length, perm_idx

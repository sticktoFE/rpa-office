import torch
from transformers import AutoTokenizer, AutoModel


def torch_gc():
    if torch.cuda.is_available():
        # with torch.cuda.device(DEVICE):
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    elif torch.backends.mps.is_available():
        try:
            from torch.mps import empty_cache

            empty_cache()
        except Exception as e:
            print(e)
            print("如果您使用的是 macOS 建议将 pytorch 版本升级至 2.0.0 或更高版本，以支持及时清理 torch 产生的内存占用。")


class similarities_model:
    def __init__(self, model_path=None) -> None:
        # Load model from HuggingFace Hub
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModel.from_pretrained(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device).eval()

    # Mean Pooling - Take attention mask into account for correct averaging
    def mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[
            0
        ]  # First element of model_output contains all token embeddings
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    def get_score(self, sentences: list):
        # Tokenize sentences
        encoded_input = self.tokenizer(
            sentences,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=10000,
        )
        encoded_input.to(self.device)
        # Compute token embeddings
        with torch.no_grad():
            model_output = self.model(**encoded_input)
        # Perform pooling. In this case, mean pooling.
        sentence_embeddings = self.mean_pooling(
            model_output, encoded_input["attention_mask"]
        )
        # print("Sentence embeddings:")
        # print(sentence_embeddings)
        # 计算余弦相似度
        similarity = torch.nn.functional.cosine_similarity(
            sentence_embeddings[0], sentence_embeddings[1], dim=0
        )
        return round(similarity.item(), 2)

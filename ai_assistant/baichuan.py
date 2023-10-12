import os

from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
import torch

PRE_TRAINED_MODEL_PATH = r"D:\leichui\workspace\rpa-ocr_dev\model\llm\Baichuan-7B"


# 程序入口
def main():
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    tokenizer = AutoTokenizer.from_pretrained(
        PRE_TRAINED_MODEL_PATH, trust_remote_code=True
    )
    tokenizer.pad_token_id = (
        0 if tokenizer.pad_token_id is None else tokenizer.pad_token_id
    )  # set as the <unk> token
    if tokenizer.pad_token_id == 64000:
        tokenizer.pad_token_id = 0  # for baichuan model (need fix)

    config = AutoConfig.from_pretrained(PRE_TRAINED_MODEL_PATH, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        PRE_TRAINED_MODEL_PATH,
        config=config,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        device_map="auto",
        low_cpu_mem_usage=True,
    )
    with torch.autocast("cuda"):
        while True:
            try:
                input_txt = input("user:")
                inputs = tokenizer(input_txt, return_tensors="pt")
                inputs = inputs.to("cuda:0")
                response = model.generate(
                    **inputs, max_new_tokens=2048, repetition_penalty=1.1
                )
                response = tokenizer.decode(response.cpu()[0], skip_special_tokens=True)
                print("bot:", response)
                torch.cuda.empty_cache()
            except Exception as e:
                print(e)
                break


if __name__ == "__main__":
    main()

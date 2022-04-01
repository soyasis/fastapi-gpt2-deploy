import re
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


def clean_response(user_prompt, response):
    """
    """
    response = re.sub("(?<=\.)[^.]*$", "", response)  # finish at last sentence dot
    response = (
        response.replace("[WP]", "").replace(user_prompt, "").replace("[RESPONSE]", "")
    )
    response = response.lstrip()
    return response


def generate_response(user_prompt: str):
    """
    """
    prompt = f"<|startoftext|>[WP] {user_prompt} [RESPONSE]"
    generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0)
    sample_outputs = model.generate(
        generated,
        do_sample=True,
        top_k=50,
        max_length=300,
        top_p=0.95,
        num_return_sequences=1,
    )
    data = []
    for i, sample_output in enumerate(sample_outputs):
        response = clean_response(
            user_prompt, tokenizer.decode(sample_output, skip_special_tokens=True)
        )
        response_dict = {"key": i, "response": response}
        data.append(response_dict)
    # output = tokenizer.decode(sample_outputs, skip_special_tokens=True)
    # output = tokenizer.decode(sample_output, skip_special_tokens=True)
    return {"data": data[0]["response"]}

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("google/electra-small-discriminator")
model = AutoModelForSequenceClassification.from_pretrained("google/electra-small-discriminator")


def decode_query(query):
    # Ultra-efficient parameter extraction (<10 tokens)
    inputs = tokenizer(query, return_tensors="pt", max_length=32, truncation=True)
    outputs = model(**inputs)
    predicted_tags = torch.argmax(outputs.logits, dim=-1)

    # Mapping to insurance ontology
    param_map = {
        0: "age", 1: "gender", 2: "procedure",
        3: "location", 4: "policy_age", 5: "distance"
    }
    return {param_map[i]: tokenizer.decode(inputs.input_ids[0][i]) for i in range(len(predicted_tags))}
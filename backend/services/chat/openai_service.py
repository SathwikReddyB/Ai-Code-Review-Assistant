from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto"
)

def generate_answer(prompt):

    result = generator(
        prompt,
        max_new_tokens=120,
        do_sample=False,
        return_full_text=False
    )

    return result[0]["generated_text"].strip()
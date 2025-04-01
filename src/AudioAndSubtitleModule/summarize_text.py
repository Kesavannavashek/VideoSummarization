from transformers import T5ForConditionalGeneration, T5Tokenizer
from extract_video_info import chunks
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import PegasusTokenizer, PegasusForConditionalGeneration

print(chunks)
print("before")
# model = T5ForConditionalGeneration.from_pretrained("t5-base")
# tokenizer = T5Tokenizer.from_pretrained("t5-base",legacy=False)
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
# model_name = "facebook/bart-large-cnn"
# tokenizer = BartTokenizer.from_pretrained(model_name)
# model = BartForConditionalGeneration.from_pretrained(model_name)
print("after")
print(len(chunks))

device = "cuda" if torch.cuda.is_available() else "cpu"

final_summary = ""
for chunk in chunks:
    print("Input Chunk:", chunk)

    inputs = tokenizer(
        chunk,
        max_length=1024,
        truncation=True,
        return_tensors="pt"
    ).to(device)

    summary_ids = model.generate(
        inputs.input_ids,
        max_length=150,
        min_length=50,
        length_penalty=2.0,
        num_beams=8,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("Summary:", summary)
    final_summary += summary + "\n"

print("Final Summary:", final_summary)

# import torch.cuda
# from transformers import T5ForConditionalGeneration, T5Tokenizer
# from extract_video_info import chunks
# from transformers import BartForConditionalGeneration, BartTokenizer
# from transformers import PegasusTokenizer, PegasusForConditionalGeneration
#
# print(chunks)
# print("before")
# # model = T5ForConditionalGeneration.from_pretrained("t5-base")
# # tokenizer = T5Tokenizer.from_pretrained("t5-base",legacy=False)
# # tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
# # model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
# model_name = "facebook/bart-large-cnn"
# tokenizer = BartTokenizer.from_pretrained(model_name)
# model = BartForConditionalGeneration.from_pretrained(model_name)
# print("after")
# print(len(chunks))
# device = "cuda" if torch.cuda.is_available() else "cpu"
# final_summary = ""
# for chunk in chunks:
#     print("Input Chunk:", chunk)
#
#     # Pegasus doesn't require task prefixes - just pass raw text
#     inputs = tokenizer(
#         "summarization of : ",chunk,
#         max_length=1024,  # Pegasus handles longer inputs
#         truncation=True,
#         return_tensors="pt"
#     ).to(device)
#
#     # Generate summary with appropriate parameters
#     summary_ids = model.generate(
#         inputs.input_ids,
#         max_length=150,  # More concise than T5/BART
#         min_length=50,
#         length_penalty=2.0,  # Favor longer summaries (2.0) or shorter (0.5)
#         num_beams=8,  # Better results with more beams
#         early_stopping=True
#     )
#
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     print("Summary:", summary)
#     final_summary += summary + "\n"
#
# print("Final Summary:", final_summary)

import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from extract_video_info import chunks  # Ensure chunks contain the video transcript

# Choose a model: T5, BART, or Pegasus
MODEL_NAME = "facebook/bart-large-cnn"  # Options: "t5-base", "google/pegasus-xsum"

device = "cuda" if torch.cuda.is_available() else "cpu"

if "t5" in MODEL_NAME:
    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME, legacy=False)
    model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)
    add_prefix = True
elif "bart" in MODEL_NAME:
    tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
    model = BartForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)
    add_prefix = False
elif "pegasus" in MODEL_NAME:
    tokenizer = PegasusTokenizer.from_pretrained(MODEL_NAME)
    model = PegasusForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)
    add_prefix = False
else:
    raise ValueError("Invalid model choice!")

final_summary = ""

for chunk in chunks:
    print("Processing Chunk:", chunk[:100])  # Show first 100 characters for debugging

    input_text = "summarize: " + chunk if add_prefix else chunk

    inputs = tokenizer(input_text, max_length=1024, truncation=True, return_tensors="pt").to(device)

    summary_ids = model.generate(
        inputs.input_ids,
        max_length=150,
        min_length=50,
        length_penalty=1.0,
        num_beams=4,
        early_stopping=False
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("Summary:", summary)
    final_summary += summary + "\n"

print("\nFinal Summary:\n", final_summary)


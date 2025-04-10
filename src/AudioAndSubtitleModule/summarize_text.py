# import torch.cuda
# from transformers import T5ForConditionalGeneration, T5Tokenizer
from extract_video_info import chunks
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

# import torch
# from transformers import BartTokenizer, BartForConditionalGeneration
#
# # Your subtitle/transcript chunks
# # chunks = [
# #     "In today's episode, we're diving deep into the world of artificial intelligence. "
# #     "We'll explore how AI is shaping industries and changing lives.",
# #     "Next, we discuss the ethical implications of AI and what researchers are doing to ensure fairness and transparency.",
# # ]
#
# # Load DistilBART model and tokenizer
# model_name = "sshleifer/distilbart-cnn-12-6"
# tokenizer = BartTokenizer.from_pretrained(model_name)
# model = BartForConditionalGeneration.from_pretrained(model_name)
#
# # Device setup
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = model.to(device)
#
# # Summarize each chunk
# final_summary = ""
# for i, chunk in enumerate(chunks):
#     print(f"\n🔹 Chunk {i+1}: {chunk[:100]}...")
#
#     inputs = tokenizer(chunk, return_tensors="pt", max_length=1024, truncation=True).to(device)
#
#     summary_ids = model.generate(
#         inputs["input_ids"],
#         max_length=130,
#         min_length=30,
#         num_beams=4,
#         length_penalty=2.0,
#         early_stopping=True
#     )
#
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
#     print(f"✅ Summary {i+1}: {summary}")
#     final_summary += summary + "\n"
#
# print("\n🔸 Final Combined Summary 🔸")
# print(final_summary)




import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Your chosen model (can also try: "meta-llama/Llama-2-7b-chat-hf", "tiiuae/falcon-7b-instruct", etc.)
model_id = "mistralai/Mistral-7B-Instruct-v0.1"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",  # Automatically uses GPU if available
    torch_dtype=torch.float16  # Efficient on GPU
)

# Create pipeline
summarizer = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Example text chunks (from subtitles, OCR, or ASR)
# chunks = [
#     "Today we explore how artificial intelligence is changing education. From virtual tutors to smart content generation, AI is making learning more personalized.",
#     "However, there are concerns over student data privacy, ethical implications of AI-based assessments, and the need for transparent systems."
# ]

final_summary = ""

for idx, chunk in enumerate(chunks):
    print(f"\n🔹 Chunk {idx+1}: {chunk[:80]}...")

    # Prompt engineering for better LLM output
    prompt = f"Summarize the following passage:\n{chunk}\nSummary:"

    response = summarizer(
        prompt,
        max_new_tokens=150,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        num_return_sequences=1
    )

    summary = response[0]["generated_text"].split("Summary:")[-1].strip()
    print(f"✅ Summary {idx+1}: {summary}")
    final_summary += summary + "\n"

print("\n🔸 Final Combined Summary 🔸\n")
print(final_summary)


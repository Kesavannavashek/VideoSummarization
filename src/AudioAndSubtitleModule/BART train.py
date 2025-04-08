# import torch
# from datasets import load_dataset
# from transformers import BartForConditionalGeneration, BartTokenizer
# from transformers import Trainer, TrainingArguments
# from torch.utils.data import DataLoader
#
# # 🚀 Step 1: Enable GPU
# device = "cuda" if torch.cuda.is_available() else "cpu"
#
# # 🚀 Step 2: Load the ArXiv dataset
# dataset = load_dataset("ccdv/arxiv-summarization")
#
# # 🚀 Step 3: Initialize tokenizer & model
# model_name = "facebook/bart-large-cnn"
# tokenizer = BartTokenizer.from_pretrained(model_name)
# model = BartForConditionalGeneration.from_pretrained(model_name).to(device)  # Move to GPU
#
# # 🚀 Step 4: Preprocessing function
# def preprocess_function(examples):
#     inputs = tokenizer(
#         examples["article"], max_length=1024, truncation=True, padding="max_length"
#     )
#     labels = tokenizer(
#         examples["abstract"], max_length=150, truncation=True, padding="max_length"
#     )
#     inputs["labels"] = labels["input_ids"]
#     return inputs
#
# # 🚀 Step 5: Apply preprocessing
# tokenized_datasets = dataset.map(preprocess_function, batched=True)
# train_dataset = tokenized_datasets["train"]
# val_dataset = tokenized_datasets["validation"]
#
# # 🚀 Step 6: Training arguments (Enable GPU & Mixed Precision)
# training_args = TrainingArguments(
#     output_dir="./bart-arxiv",
#     evaluation_strategy="epoch",
#     save_strategy="epoch",
#     per_device_train_batch_size=4,  # Adjust for GPU memory
#     per_device_eval_batch_size=4,
#     num_train_epochs=3,
#     fp16=True,  # Enable Mixed Precision for Speed 🚀
#     logging_dir="./logs",
#     logging_steps=500,
#     save_total_limit=2,
#     save_safetensors=True,
#     push_to_hub=False
# )
#
# # 🚀 Step 7: Initialize Trainer
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=train_dataset,
#     eval_dataset=val_dataset,
#     tokenizer=tokenizer
# )
#
# # 🚀 Step 8: Start GPU-Accelerated Training
# trainer.train()
#
# # 🚀 Step 9: Save the Fine-Tuned Model
# model.save_pretrained("./fine_tuned_bart")
# tokenizer.save_pretrained("./fine_tuned_bart")

import torch
from datasets import load_dataset
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import Trainer, TrainingArguments

# 🚀 Step 1: Enable GPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# 🚀 Step 2: Load a subset of the ArXiv dataset
dataset = load_dataset("ccdv/arxiv-summarization")
train_data = dataset["train"].select(range(5000))       # ✅ Use subset for fast iteration
val_data = dataset["validation"].select(range(1000))

# 🚀 Step 3: Initialize tokenizer & model
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name).to(device)

# 🚀 Step 4: Preprocessing function
def preprocess_function(examples):
    inputs = tokenizer(
        examples["article"], max_length=512, truncation=True, padding="max_length"  # ✅ Reduce input size
    )
    labels = tokenizer(
        examples["abstract"], max_length=64, truncation=True, padding="max_length"  # ✅ Reduce label size
    )
    inputs["labels"] = labels["input_ids"]
    return inputs

# 🚀 Step 5: Apply preprocessing
train_dataset = train_data.map(preprocess_function, batched=True, remove_columns=["article", "abstract"])
val_dataset = val_data.map(preprocess_function, batched=True, remove_columns=["article", "abstract"])


# 🚀 Step 6: Optimized TrainingArguments
training_args = TrainingArguments(
    output_dir="./bart-arxiv-3050ti",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=2,          # ✅ Reduce batch size
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=8,          # ✅ Simulate batch size of 16
    num_train_epochs=1,                     # ✅ Start with 1 epoch
    fp16=True,                              # ✅ Use mixed precision
    learning_rate=3e-5,
    lr_scheduler_type="cosine",             # ✅ Better learning decay
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=250,
    save_total_limit=1,
    save_safetensors=True,
    push_to_hub=False
)

# 🚀 Step 7: Trainer Setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

# 🚀 Step 8: Train
trainer.train()

# 🚀 Step 9: Save model
model.save_pretrained("./fine_tuned_bart_3050ti")
tokenizer.save_pretrained("./fine_tuned_bart_3050ti")


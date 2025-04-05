import torch
from datasets import load_dataset
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import Trainer, TrainingArguments
from torch.utils.data import DataLoader

# 🚀 Step 1: Enable GPU
device = "cuda" if torch.cuda.is_available() else "cpu"

# 🚀 Step 2: Load the ArXiv dataset
dataset = load_dataset("ccdv/arxiv-summarization")

# 🚀 Step 3: Initialize tokenizer & model
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name).to(device)  # Move to GPU

# 🚀 Step 4: Preprocessing function
def preprocess_function(examples):
    inputs = tokenizer(
        examples["article"], max_length=1024, truncation=True, padding="max_length"
    )
    labels = tokenizer(
        examples["abstract"], max_length=150, truncation=True, padding="max_length"
    )
    inputs["labels"] = labels["input_ids"]
    return inputs

# 🚀 Step 5: Apply preprocessing
tokenized_datasets = dataset.map(preprocess_function, batched=True)
train_dataset = tokenized_datasets["train"]
val_dataset = tokenized_datasets["validation"]

# 🚀 Step 6: Training arguments (Enable GPU & Mixed Precision)
training_args = TrainingArguments(
    output_dir="./bart-arxiv",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=4,  # Adjust for GPU memory
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    fp16=True,  # Enable Mixed Precision for Speed 🚀
    logging_dir="./logs",
    logging_steps=500,
    save_total_limit=2,
    save_safetensors=True,
    push_to_hub=False
)

# 🚀 Step 7: Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer
)

# 🚀 Step 8: Start GPU-Accelerated Training
trainer.train()

# 🚀 Step 9: Save the Fine-Tuned Model
model.save_pretrained("./fine_tuned_bart")
tokenizer.save_pretrained("./fine_tuned_bart")

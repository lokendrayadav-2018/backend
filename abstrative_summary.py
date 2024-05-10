
def generate_abstractive_summary(text,model,tokenizer):
    prefixed_text = "summarize: " + text
    input_ids = tokenizer.encode(prefixed_text, return_tensors="pt")
    summary_ids = model.generate(input_ids, 
        max_length=150, 
        min_length=40, 
        length_penalty=2.0, 
        num_beams=4, 
        early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

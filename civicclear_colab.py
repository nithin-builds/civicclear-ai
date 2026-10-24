"""Spark-X2.6-4B inference core for CivicClear (Google Colab GPU recommended)."""
import json
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "XHToken/Spark-X2.6-4B"
SCHEMA = {"meaning":"", "next_steps":[], "documents":[], "dates":[], "uncertainties":[], "human_verification":""}

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, device_map="auto", torch_dtype="auto", trust_remote_code=True)
    return tokenizer, model

def build_prompt(notice: str, language: str = "Plain English") -> str:
    return f"""You are CivicClear, a cautious public-information accessibility assistant.
Transform the notice into {language}. Return JSON only using exactly these keys:
{json.dumps(SCHEMA)}
Rules: use only the notice; never invent dates, rights, requirements, or contact details; identify missing information; separate facts from suggested actions; require verification for legal, medical, housing, benefits, or deadline-sensitive decisions; do not repeat personal identifiers.
NOTICE:
{notice}
JSON:"""

def analyze(notice: str, language: str = "Plain English") -> dict:
    tokenizer, model = load_model()
    inputs = tokenizer(build_prompt(notice, language), return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=700, do_sample=False)
    decoded = tokenizer.decode(output[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return json.loads(decoded[decoded.index("{"):decoded.rindex("}")+1])

if __name__ == "__main__":
    sample = "Your application must be renewed within 30 days. Provide proof of household income."
    print(json.dumps(analyze(sample), indent=2, ensure_ascii=False))

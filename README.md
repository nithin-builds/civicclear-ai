# Aegis-Her (芳盾·微光)

A privacy-first accessibility assistant that helps frontline workers and displaced women turn maternal-health and crisis notices into clear next actions. Built for **HER Hack-Astron #7** with **Spark-X2.6-4B**.

## What is implemented

- `aegis_her_app.py`: standard-library HTTP service and CLI with PII redaction, strict schema validation, human-review gates, and 10 tests.
- `dist/index.html`: bilingual interactive workbench with four scenarios.
- Spark-X2.6-4B performs notice-to-action transformation through a local OpenAI-compatible endpoint.
- Replay mode exists only for UI testing and is visibly labelled; it is never represented as model output.

## Run

```bash
python3 aegis_her_app.py --test
ollama run SparkLLM/Spark-X2.6-4B
python3 aegis_her_app.py
```

Open `dist/index.html`, select **Live Spark**, and analyze a redacted notice.

## Reproducibility record

- Model: `XHToken/Spark-X2.6-4B` or official Ollama distribution `SparkLLM/Spark-X2.6-4B`
- Model API: `http://127.0.0.1:11434/v1`
- Aegis-Her service: `http://127.0.0.1:8088/v1/analyze`
- Generation: temperature `0.1`, maximum output `900` tokens

The final evidence record must state the exact revision, quantization, hardware, runtime versions, and include unedited output.

## Safety boundaries

This prototype does not diagnose, determine eligibility, prioritize people, or replace emergency services or qualified professionals. PII redaction is best-effort and must be followed by human review.

## Evaluation integrity

`benchmark_protocol.json` defines the planned N=32 evaluation. No quantitative result is claimed until raw model outputs and reviewer labels are published.

## AI-assisted development disclosure

AI assisted with implementation and documentation. The human contributor verifies the model run, evidence, and final submission.

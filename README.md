# CivicClear AI

CivicClear turns complex public-service notices into safe, structured action plans. It is an entry for HER Hack-Astron #7 and is designed around accessibility, uncertainty disclosure, and human verification.

## Live demo

https://civicclear-ai.blondharp2.chatgpt.site

## Why it is different

Typical summarizers shorten text. CivicClear produces a stable five-part schema: meaning, next actions, documents, dates, and uncertainty/human-check guidance. It never invents missing dates or presents itself as an authority.

## Demo and model architecture

The hosted interface uses deterministic examples so reviewers can test it without credentials. The included inference script runs Spark-X2.6-4B and asks it to emit the identical structured schema. This separation makes the public demo reliable while preserving reproducible proof of real model usage.

## Safety boundaries

- Remove personal identifiers before use.
- Not legal, medical, benefits, or housing advice.
- Missing or ambiguous information is surfaced, not guessed.
- High-impact actions must be verified with the issuing authority or a qualified professional.

## Run locally

Open `index.html` in a browser. For model inference, install `requirements.txt` in Google Colab and run `civicclear_colab.py` on a GPU runtime.

## AI-assisted development disclosure

The interface, test plan, prompt schema, and documentation were developed with AI assistance and reviewed for truthful capability claims.

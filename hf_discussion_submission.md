# [HER Hack-Astron # 7] [Open Source AI for Good] Aegis-Her (芳盾·微光)

## Project name and track

**Project:** Aegis-Her (芳盾·微光)  
**Primary track:** Maternal-health and crisis-information accessibility  
**Supporting capabilities:** privacy protection, public-service accessibility, and gender-safe policy review

## Who this helps and what problem it solves

Frontline workers and displaced women may receive urgent information in dense, unfamiliar, or mixed-language text. Aegis-Her converts a redacted notice into a cautious action plan: plain-language meaning, urgent actions, ordinary next steps, documents, deadlines, uncertainties, and a mandatory human-review instruction.

The system redacts common phone, email, and government-ID patterns before inference. It never diagnoses, determines eligibility, ranks people, or replaces emergency services or qualified professionals.

## How Spark-X2.6-4B is used

- **Model:** `XHToken/Spark-X2.6-4B`
- **Exact revision:** `66e3ae7bee54e0a523d692cb8ef841f35409807b`
- **Role:** multilingual notice-to-structured-action transformation using a strict JSON schema
- **Runtime:** Transformers `4.57.1`, PyTorch `2.11.0+cu130`, Tesla T4, `torch.bfloat16`
- **Generation:** thinking disabled, deterministic decoding, maximum output 600 tokens

Replay mode is only a clearly labelled UI test. Every screenshot presented as model evidence will be captured from live Spark-X2.6-4B output.

## Demo

**Live interface:** https://civicclear-ai.blondharp2.chatgpt.site  
**Source:** https://github.com/nithin-builds/civicclear-ai

### Illustrated walkthrough

1. `[SCREENSHOT: selected maternal-health scenario and sanitized preview]`
2. `[SCREENSHOT: terminal showing model/runtime and Aegis-Her service]`
3. `[SCREENSHOT: complete live result with model label]`
4. `[SCREENSHOT: uncertainty and human-review cards]`

**Actual input:** `社区诊所通知：孕妇若出现严重头痛、视力模糊、上腹疼痛或面部突然肿胀，应立即联系急诊服务。预约咨询电话 [PHONE-REDACTED]，患者身份证 [ID-REDACTED]。`  
**Actual output:** The model returned valid JSON in 7.26 seconds, correctly identifying the four warning signs and the urgent instruction to contact emergency services. The complete unedited evidence is published in `aegis_her_evidence.json`.

## How to reproduce

```bash
python3 aegis_her_app.py --test
ollama run SparkLLM/Spark-X2.6-4B
python3 aegis_her_app.py
```

Open `dist/index.html`, select **Live Spark**, choose a scenario, and run the analysis. The service also exposes `POST http://127.0.0.1:8088/v1/analyze`.

**Hardware:** NVIDIA Tesla T4  
**Precision:** `torch.bfloat16`

## Results and limitations

Ten deterministic tests cover redaction, schema validation, replay labelling, prompt boundaries, and empty-input rejection. They do not claim model quality.

An N=32 evaluation protocol is included, but no numerical result is claimed until raw outputs and human labels are complete. Current limitations include incomplete PII-pattern coverage, text-only input, dependence on local runtime configuration, and the possibility of incorrect or incomplete model output. Consequential decisions always require human verification.

## Contributors and disclosure

**Individual contributor:** `nithin-builds`  
**Contribution:** product concept, acceptance decisions, testing and final evidence verification  
**AI-assisted development:** AI assisted with implementation, UI and documentation. The human contributor verifies the actual model run and submission evidence.  
**Data:** synthetic scenarios only; no personal data.

---

## GitHub Issue #16 reply (post only after the Discussion exists)

Submitted: **Aegis-Her (芳盾·微光)** — a privacy-first maternal-health and crisis-information accessibility assistant powered by Spark-X2.6-4B.

Hugging Face Discussion: `[DIRECT DISCUSSION URL]`  
Source: https://github.com/nithin-builds/civicclear-ai  
Demo: https://civicclear-ai.blondharp2.chatgpt.site

Individual contributor: https://github.com/nithin-builds

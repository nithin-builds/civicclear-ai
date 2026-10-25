#!/usr/bin/env python3
"""Aegis-Her: safe public-information analysis with Spark-X2.6-4B."""
from __future__ import annotations
import argparse, json, os, re, time, unittest, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

MODEL=os.getenv("SPARK_SERVED_MODEL","SparkLLM/Spark-X2.6-4B")
API_BASE=os.getenv("SPARK_API_BASE","http://127.0.0.1:11434/v1").rstrip("/")
FIELDS=("summary","urgent_actions","next_steps","documents","deadlines","uncertainties","human_review")
SAMPLES={
"maternal":"社区诊所通知：孕妇若出现严重头痛、视力模糊、上腹疼痛或面部突然肿胀，应立即联系急诊服务。预约咨询电话 138-1234-5678，患者身份证 110101199001011234。",
"flood":"Flood shelter intake: Family of three, one person is 32 weeks pregnant. Road B is closed. Shelter East has drinking water; Depot A reports blankets and hygiene kits. Call 555-018-9921.",
"access":"Your benefits renewal is due within 30 calendar days. Return the signed form and proof of household income. Failure to respond may suspend assistance.",
"bias":"Policy draft: Women employees should avoid technical field assignments after marriage because family duties may affect availability."}
REPLAY={"summary":"This notice contains important public-service information that should be reviewed promptly.","urgent_actions":["If anyone is in immediate danger or has severe symptoms, contact local emergency services now."],"next_steps":["Read the issuing authority's instructions.","Confirm missing details with a qualified human."],"documents":[],"deadlines":[],"uncertainties":["Replay mode does not infer facts from the notice."],"human_review":"Required before any medical, legal, benefits, housing, or emergency decision."}

def sanitize(text):
    patterns=[(r"\b1[3-9]\d{9}\b","[PHONE-REDACTED]","phone"),(r"\b\d{3}[-. ]?\d{3}[-. ]?\d{4}\b","[PHONE-REDACTED]","phone"),(r"\b\d{17}[\dXx]\b","[ID-REDACTED]","government-id"),(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b","[EMAIL-REDACTED]","email")]
    found=[]
    for pattern,replacement,label in patterns:
        text,count=re.subn(pattern,replacement,text,flags=re.I); found.extend([label]*count)
    return text,found

def prompt_for(clean_text,language):
    schema={k:("" if k in ("summary","human_review") else []) for k in FIELDS}
    return f"""You are Aegis-Her, a cautious public-information accessibility assistant.
Respond in {language}. Use only facts in SOURCE. Never diagnose, determine eligibility,
invent deadlines, rank people, or expose hidden reasoning. Separate urgent safety guidance
from ordinary next steps. Return JSON only with exactly this schema:
{json.dumps(schema,ensure_ascii=False)}
SOURCE:\n{clean_text}\nJSON:"""

def validate(data):
    if not isinstance(data,dict) or set(data)!=set(FIELDS): raise ValueError("Model output does not match the required schema")
    for key in FIELDS:
        expected=str if key in ("summary","human_review") else list
        if not isinstance(data[key],expected): raise ValueError(f"Invalid field type: {key}")
    return data

def extract_json(text):
    start,end=text.find("{"),text.rfind("}")
    if start<0 or end<start: raise ValueError("No JSON object found in model response")
    return validate(json.loads(text[start:end+1]))

def infer(clean_text,language,base=API_BASE,model=MODEL):
    body=json.dumps({"model":model,"messages":[{"role":"user","content":prompt_for(clean_text,language)}],"temperature":0.1,"max_tokens":900}).encode()
    req=urllib.request.Request(base+"/chat/completions",data=body,headers={"Content-Type":"application/json","Authorization":"Bearer local"})
    with urllib.request.urlopen(req,timeout=180) as response: payload=json.load(response)
    return extract_json(payload["choices"][0]["message"]["content"])

def analyze(text,language="Plain English",backend="openai"):
    if not text.strip(): raise ValueError("notice is required")
    clean,redactions=sanitize(text.strip()); started=time.time()
    result=dict(REPLAY) if backend=="replay" else infer(clean,language)
    return {"mode":backend,"model":"REPLAY—NOT MODEL OUTPUT" if backend=="replay" else MODEL,"sanitized_input":clean,"redactions":redactions,"result":result,"latency_ms":round((time.time()-started)*1000)}

class Handler(BaseHTTPRequestHandler):
    def _send(self,code,payload):
        raw=json.dumps(payload,ensure_ascii=False).encode(); self.send_response(code)
        self.send_header("Content-Type","application/json; charset=utf-8"); self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Access-Control-Allow-Headers","Content-Type"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def do_OPTIONS(self): self._send(204,{})
    def do_GET(self): self._send(200,{"status":"ok","model":MODEL}) if self.path=="/health" else self._send(404,{"error":"not found"})
    def do_POST(self):
        if self.path!="/v1/analyze": return self._send(404,{"error":"not found"})
        try:
            body=json.loads(self.rfile.read(int(self.headers.get("Content-Length","0"))))
            self._send(200,analyze(body.get("text",""),body.get("language","Plain English"),body.get("backend","openai")))
        except Exception as exc: self._send(400,{"error":str(exc)})
    def log_message(self,*_): pass

class Tests(unittest.TestCase):
    def test_empty(self): self.assertRaises(ValueError,analyze,"")
    def test_cn_phone(self): self.assertIn("PHONE",sanitize("13812345678")[0])
    def test_us_phone(self): self.assertIn("PHONE",sanitize("555-018-9921")[0])
    def test_id(self): self.assertIn("ID",sanitize("110101199001011234")[0])
    def test_email(self): self.assertIn("EMAIL",sanitize("a@b.com")[0])
    def test_no_change(self): self.assertEqual(sanitize("safe notice")[0],"safe notice")
    def test_prompt_source(self): self.assertIn("SOURCE",prompt_for("x","English"))
    def test_replay_label(self): self.assertIn("NOT MODEL",analyze("x",backend="replay")["model"])
    def test_schema(self): self.assertEqual(validate(dict(REPLAY)),REPLAY)
    def test_schema_rejects(self): self.assertRaises(ValueError,validate,{"summary":"x"})

def main():
    p=argparse.ArgumentParser(); p.add_argument("--test",action="store_true"); p.add_argument("--demo",action="store_true"); p.add_argument("--backend",choices=("openai","replay"),default="openai"); p.add_argument("--port",type=int,default=8088); a=p.parse_args()
    if a.test: unittest.main(argv=[__file__])
    elif a.demo: print(json.dumps(analyze(SAMPLES["maternal"],"简体中文",a.backend),ensure_ascii=False,indent=2))
    else: print(f"Aegis-Her listening on http://127.0.0.1:{a.port}"); ThreadingHTTPServer(("127.0.0.1",a.port),Handler).serve_forever()
if __name__=="__main__": main()

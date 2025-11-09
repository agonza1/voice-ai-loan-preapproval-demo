# AI Context Guide (Condensed)

**Essential context for AI-assisted development tools. For detailed docs, see other files in `/docs`.**

## Critical Flow
1. Twilio call → `POST /` → TwiML with WebSocket URL
2. WebSocket `/ws` → Pipecat pipeline (STT → LLM → TTS)
3. Agent collects: **name → phone → zip_code** (in order)
4. Generate secure link → Send Email (MailerSend)
5. User completes form → `POST /loan-application`
6. Credit check → DecisionRules evaluation → Result/escale

## Key Files
- **`main.py`**: FastAPI endpoints (webhook, WebSocket, form)
- **`bot.py`**: Pipecat voice pipeline, LLM conversation
- **`templates/loan_application.html`**: Form (pre-fills from URL params)
- **`static/js/loan_application.js`**: Form pre-fill logic

## Tech Stack
FastAPI, Pipecat (https://reference-server.pipecat.ai/en/latest/), Twilio (webhooks), MailerSend (email), DecisionRules (https://docs.decisionrules.io/doc)

## DecisionRules Integration
```python
from decisionrules import DecisionRules
solver = DecisionRules(solver_key=os.getenv("DECISIONRULES_SOLVER_KEY"), host="https://api.decisionrules.io")
result = await solver.solve("loan-approval", data={...}, version="latest")
```

## Environment Variables
`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `DEEPGRAM_API_KEY`, `OPENAI_API_KEY`, `MAILERSEND_API_KEY`, `DECISIONRULES_SOLVER_KEY`, `WEBSOCKET_URL` (optional)

## Implementation Status
✅ Voice call, WebSocket, STT/LLM/TTS pipeline, form  
⏳ DecisionRules, MailerSend email, escalation

## Important Constraints
- Soft credit inquiry (explain to user)
- Explicit consent required
- Secure links expire (24h)
- HTTPS/WSS in production
- **In-memory storage only** - No database, data lost on restart

## Form Pre-fill
URL params: `?legal_name=X&phone=Y&zip_code=Z` → JavaScript reads on page load

## LLM System Prompt
Defines structured workflow: greeting → consent → collect (name, phone, zip) → send link

---
**Note**: Detailed documentation available in other `/docs` files. This is a condensed reference for AI tools.

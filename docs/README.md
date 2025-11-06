# Voice AI Loan Pre-Approval Demo - Documentation

This documentation provides comprehensive architecture and API reference for the Voice AI Loan Pre-Approval Demo application. This documentation is designed to serve as context for AI-assisted development tools like Cursor.

## Documentation Structure

- **[Architecture Overview](./architecture.md)** - High-level system architecture, components, and data flow
- **[API Reference](./api-reference.md)** - Complete API endpoint documentation
- **[High-Level Flow](./high-level-flow.md)** - Detailed workflow and process flows
- **[Components](./components.md)** - Detailed component descriptions and responsibilities
- **[Integrations](./integrations.md)** - Third-party service integrations and configuration

## Quick Start

For developers new to the project, start with:
1. [Architecture Overview](./architecture.md) - Understand the system design
2. [High-Level Flow](./high-level-flow.md) - Learn the application workflow
3. [API Reference](./api-reference.md) - Explore available endpoints

## Project Context

This is a voice-enabled loan pre-approval system that:
- Captures applicant information via voice calls (Twilio)
- Uses AI-powered conversation (OpenAI GPT-4o) with STT (Deepgram) and TTS (ElevenLabs)
- Evaluates loan eligibility using DecisionRules
- Sends secure links via Email (MailerSend) for application completion
- Handles edge cases with human escalation

## Key Technologies

- **FastAPI**: Web framework and WebSocket server
- **Pipecat**: Real-time audio processing pipeline ([API Reference](https://reference-server.pipecat.ai/en/latest/))
- **Twilio**: Call webhooks and audio streaming
- **MailerSend**: Email delivery service ([npm package](https://www.npmjs.com/package/mailersend))
- **DecisionRules**: Business rules engine for loan evaluation ([Documentation](https://docs.decisionrules.io/doc))


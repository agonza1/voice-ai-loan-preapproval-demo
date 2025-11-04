# Voice AI Agent Example

A multilingual voice AI conversation partner built with FastAPI and Pipecat that helps English speakers learn other languages through real-time voice conversations.

## Features

- Real-time voice conversations via WebSocket
- Speech-to-Text using Deepgram
- AI-powered responses with OpenAI GPT-4
- Text-to-Speech using ElevenLabs
- Twilio integration for phone calls
- Multilingual support
- Dynamic WebSocket URL generation for different deployment environments

## Architecture

- **FastAPI**: Web framework with WebSocket support
- **Pipecat**: Audio processing pipeline
- **Twilio**: Phone call integration
- **Deepgram**: Speech recognition
- **OpenAI**: Language model for conversations
- **ElevenLabs**: Text-to-speech synthesis

## Prerequisites

- Python 3.12+
- API keys for:
  - OpenAI
  - Deepgram
  - ElevenLabs
  - Twilio Account SID and Auth Token
- **For local development with Twilio**: ngrok or similar tunneling service (to expose your local server to receive webhook requests)

## Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run the application**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. **Set up tunneling for Twilio webhooks** (required for testing with phone calls):
   
   Twilio needs a publicly accessible URL to send webhook requests to your local server. Use a tunneling service like ngrok:
   
   ```bash
   # Install ngrok (if not already installed)
   # Visit https://ngrok.com/download or use: brew install ngrok / snap install ngrok
   
   # Start ngrok tunnel to your local server
   ngrok http 8000
   ```
   
   Copy the HTTPS URL from ngrok (e.g., `https://abc123.ngrok.io`) and configure it in your Twilio console:
   - Go to your Twilio Phone Number settings
   - Set the webhook URL for incoming calls to: `https://your-ngrok-url.ngrok.io/`
   
   **Note**: For WebSocket support, ensure ngrok is configured for WebSocket connections (ngrok's free tier supports this by default when using `http` protocol).

## Deployment

### Cerebrium Deployment

1. **Install Cerebrium CLI**:
   ```bash
   pip install cerebrium
   ```

2. **Configure secrets in Cerebrium dashboard**:
   - `OPENAI_API_KEY`
   - `DEEPGRAM_API_KEY`
   - `ELEVENLABS_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`

3. **Deploy**:
   ```bash
   cerebrium deploy
   ```

### Amazon ECS Deployment

1. **Configure AWS credentials**:
   ```bash
   aws configure
   ```

2. **Deploy infrastructure**:
   ```bash
   cd infrastructure
   cp terraform.tfvars.example terraform.tfvars
   # Edit terraform.tfvars with your API keys
   ./deploy-infra.sh
   ```

3. **Deploy application**:
   ```bash
   cd ..
   ./deploy.sh
   ```

4. **Application URL**:
   The application URL will be displayed at the end of the deployment process.
   Use the ALB DNS name for accessing the application.

## API Endpoints

- `POST /` - Returns TwiML with WebSocket URL for Twilio
- `WebSocket /ws` - Real-time audio streaming endpoint

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 |
| `DEEPGRAM_API_KEY` | Deepgram API key for speech recognition |
| `ELEVENLABS_API_KEY` | ElevenLabs API key for text-to-speech |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token |

## How It Works

1. External service (Twilio) makes POST request to `/`
2. Application returns TwiML with dynamically generated WebSocket URL
3. WebSocket connection established at `/ws`
4. Audio pipeline processes:
   - Incoming audio → Speech-to-Text
   - Text → AI processing
   - AI response → Text-to-Speech
   - Audio response sent back

## Cleanup

### Cerebrium
```bash
cerebrium delete cerebrium-demo
```

### Amazon ECS
```bash
cd infrastructure
tofu destroy
```
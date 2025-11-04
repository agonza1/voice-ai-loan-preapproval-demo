import os
import sys

from loguru import logger
from pipecat.frames.frames import LLMMessagesFrame, EndFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask

from pipecat.services.openai.llm import OpenAILLMService
from pipecat.processors.aggregators.openai_llm_context import (
    OpenAILLMContext,
)
from pipecat.services.deepgram.stt import DeepgramSTTService, LiveOptions
from pipecat.audio.vad.silero import SileroVADAnalyzer
from twilio.rest import Client
from pipecat.transports.network.fastapi_websocket import (
    FastAPIWebsocketTransport,
    FastAPIWebsocketParams,
)
from pipecat.serializers.twilio import TwilioFrameSerializer

from pipecat.services.elevenlabs.tts import ElevenLabsTTSService

logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

twilio = Client(
    os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN")
)

async def main(websocket_client, stream_sid):
    transport = FastAPIWebsocketTransport(
        websocket=websocket_client,
        params=FastAPIWebsocketParams(
            audio_out_enabled=True,
            add_wav_header=False,
            vad_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
            vad_audio_passthrough=True,
            serializer=TwilioFrameSerializer(stream_sid),
        ),
    )
    
    deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

    stt = DeepgramSTTService(
        api_key=deepgram_api_key,
        live_options=LiveOptions(
            model="nova-2-general",
            language="multi"
        )
    )

    llm = OpenAILLMService(
        name="LLM",
        api_key=openai_api_key,
        model="gpt-4o",
    )

    tts = ElevenLabsTTSService(
        api_key=elevenlabs_api_key,
        model="eleven_multilingual_v2",
        voice_id="Xb7hH8MSUJpSbSDYk0k2"
    )

    messages = [
        {
            "role": "system",
            "content": """
You are a professional and friendly loan pre-approval assistant for a fintech company. Your role is to help customers get a quick loan pre-approval estimate.

Your workflow:
1. Opening: Greet the caller warmly and introduce the quick pre-approval service. Ask if you can proceed to help them get an estimate.
2. Consent checkpoint: Explain that you'll use a soft credit inquiry that does not impact their credit score. Get their explicit consent before proceeding.
3. Collect basics: Gather the following information IN THIS ORDER:
   - Full name (legal name)
   - Mobile number (where you will send the secure link)
   - Zip code
4. Link handoff: AFTER collecting all three pieces of information (full name, mobile number, and zip code), confirm you've sent the secure link to their mobile number and offer to stay on the line if they need help.

IMPORTANT: Only mention sending the link AFTER you have collected the full name, mobile number, and zip code. Do not mention the link during the opening or consent phases.

Guidelines:
- Be professional, warm, and helpful
- Speak clearly and at a moderate pace
- Confirm information as you collect it
- If the caller seems hesitant, address their concerns
- Keep the conversation focused on the pre-approval process
- Be concise but thorough
- Use natural, conversational language
- Wait until you have all three pieces of information before sending the link""",
        },
    ]
    print('here', flush=True)
    context = OpenAILLMContext(messages=messages)
    context_aggregator = llm.create_context_aggregator(context)

    pipeline = Pipeline(
        [
            transport.input(),  # Websocket input from client
            stt,  # Speech-To-Text
            context_aggregator.user(),
            llm,  # LLM
            tts,  # Text-To-Speech
            transport.output(),  # Websocket output to client
            context_aggregator.assistant(),
        ]
    )

    task = PipelineTask(pipeline, params=PipelineParams(allow_interruptions=True))

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        # Kick off the conversation with the opening message
        opening_message = {
            "role": "system", 
            "content": "Say: 'Hi, you have reached the quick pre-approval line. We can estimate your eligible amount in a under 3 minutes. May I proceed?'"
        }
        messages.append(opening_message)
        await task.queue_frames([LLMMessagesFrame(messages)])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        await task.queue_frames([EndFrame()])

    runner = PipelineRunner(handle_sigint=False)

    await runner.run(task)
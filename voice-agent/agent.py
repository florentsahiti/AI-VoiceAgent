import logging
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, WorkerOptions
from livekit.plugins import groq, deepgram, silero

load_dotenv(override=True)

logger = logging.getLogger("voice-agent")
logger.setLevel(logging.INFO)


class Assistant(Agent):
    def __init__(self) -> None:
        # LLM: Groq running Llama 3.3 70B (free, fast)
        llm = groq.LLM(model="llama-3.3-70b-versatile")
        
        # STT: Deepgram Nova-2 (free credits, very fast)
        stt = deepgram.STT(model="nova-2")
        
        # TTS: Deepgram Aura (same DEEPGRAM_API_KEY as STT; avoids invalid Cartesia keys)
        tts = deepgram.TTS(model="aura-asteria-en")
        
        silero_vad = silero.VAD.load()

        super().__init__(
            instructions="""
                You are a helpful assistant communicating via voice.
                Keep your responses short and conversational, ideally 1-2 sentences.
            """,
            stt=stt,
            llm=llm,
            tts=tts,
            vad=silero_vad,
        )


async def entrypoint(ctx: JobContext):
    await ctx.connect()
    session = AgentSession()
    await session.start(
        room=ctx.room,
        agent=Assistant(),
    )


if __name__ == "__main__":
    agents.cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
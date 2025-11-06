"""Service layer for interacting with the OpenAI agent."""
import sys
import time
from pathlib import Path

from django.conf import settings

# Add the src directory to the path so we can import the OpenAI agent
src_path = Path(__file__).resolve().parent.parent.parent / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from openai_agent import OpenAIAgent
from .models import PromptResponse, AgentSession


class PromptAgentService:
    """Service for processing prompts using the OpenAI agent."""

    def __init__(self):
        """Initialize the agent service."""
        self.agent = OpenAIAgent(api_key=settings.OPENAI_API_KEY)

    def process_prompt(self, prompt_text: str, session: AgentSession = None) -> PromptResponse:
        """
        Process a user prompt and store the result.

        Args:
            prompt_text: The user's input prompt
            session: Optional agent session to use for configuration

        Returns:
            PromptResponse object with the result
        """
        # Determine which model to use
        model = session.model if session else settings.OPENAI_MODEL

        # Create the prompt response record
        prompt_response = PromptResponse.objects.create(
            prompt=prompt_text,
            session=session,
            model_used=model,
            status='processing'
        )

        start_time = time.time()

        try:
            # Generate the response using the OpenAI agent
            response_text = self.agent.generate_response(prompt_text, model=model)

            # Calculate processing time
            processing_time = time.time() - start_time

            # Update the record with success
            prompt_response.response = response_text
            prompt_response.status = 'completed'
            prompt_response.processing_time = processing_time
            prompt_response.save()

        except Exception as exc:
            # Calculate processing time even on error
            processing_time = time.time() - start_time

            # Update the record with error
            prompt_response.status = 'failed'
            prompt_response.error_message = str(exc)
            prompt_response.processing_time = processing_time
            prompt_response.save()

            raise

        return prompt_response

    def get_recent_prompts(self, limit: int = 10):
        """
        Get recent prompts and responses.

        Args:
            limit: Maximum number of records to return

        Returns:
            QuerySet of PromptResponse objects
        """
        return PromptResponse.objects.all()[:limit]

    def create_session(self, name: str, model: str = None, system_prompt: str = '') -> AgentSession:
        """
        Create a new agent session.

        Args:
            name: Name for the session
            model: Model to use (defaults to settings)
            system_prompt: Optional system prompt

        Returns:
            Created AgentSession object
        """
        if model is None:
            model = settings.OPENAI_MODEL

        return AgentSession.objects.create(
            name=name,
            model=model,
            system_prompt=system_prompt
        )

    def get_active_sessions(self):
        """Get all active agent sessions."""
        return AgentSession.objects.filter(is_active=True)

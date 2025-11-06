"""App configuration for the prompt agent."""
from django.apps import AppConfig


class PromptAgentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prompt_agent'
    verbose_name = 'Prompt Agent'

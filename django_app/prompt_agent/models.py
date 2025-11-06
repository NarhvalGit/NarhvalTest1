"""Database models for the prompt agent application."""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AgentSession(models.Model):
    """Represents an agent session with configuration."""

    name = models.CharField(max_length=200, help_text="Name of the agent session")
    model = models.CharField(
        max_length=100,
        default='gpt-4o-mini',
        help_text="OpenAI model to use for this session"
    )
    system_prompt = models.TextField(
        blank=True,
        help_text="System prompt to configure agent behavior"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Agent Session'
        verbose_name_plural = 'Agent Sessions'

    def __str__(self):
        return f"{self.name} ({self.model})"


class PromptResponse(models.Model):
    """Stores user prompts and AI responses."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    session = models.ForeignKey(
        AgentSession,
        on_delete=models.CASCADE,
        related_name='prompts',
        null=True,
        blank=True,
        help_text="Associated agent session"
    )
    prompt = models.TextField(help_text="User's input prompt")
    response = models.TextField(blank=True, help_text="AI generated response")
    model_used = models.CharField(
        max_length=100,
        default='gpt-4o-mini',
        help_text="Model used for this response"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    error_message = models.TextField(
        blank=True,
        help_text="Error message if processing failed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processing_time = models.FloatField(
        null=True,
        blank=True,
        help_text="Time taken to process in seconds"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prompt Response'
        verbose_name_plural = 'Prompt Responses'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Prompt at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

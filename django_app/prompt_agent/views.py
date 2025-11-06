"""Views for the prompt agent application."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import PromptForm, AgentSessionForm
from .services import PromptAgentService
from .models import PromptResponse, AgentSession


def index(request):
    """Main page with prompt interface."""
    service = PromptAgentService()

    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt_text = form.cleaned_data['prompt']
            session = form.cleaned_data.get('session')

            try:
                # Process the prompt
                prompt_response = service.process_prompt(prompt_text, session=session)

                messages.success(
                    request,
                    f'Prompt verwerkt in {prompt_response.processing_time:.2f} seconden!'
                )

                # Redirect to avoid form resubmission
                return redirect('index')

            except Exception as exc:
                messages.error(
                    request,
                    f'Fout bij het verwerken van de prompt: {str(exc)}'
                )
    else:
        form = PromptForm()

    # Get recent prompts
    recent_prompts = service.get_recent_prompts(limit=20)

    context = {
        'form': form,
        'recent_prompts': recent_prompts,
        'active_sessions': service.get_active_sessions(),
    }

    return render(request, 'prompt_agent/index.html', context)


@require_http_methods(["POST"])
def submit_prompt_ajax(request):
    """AJAX endpoint for submitting prompts."""
    try:
        data = json.loads(request.body)
        prompt_text = data.get('prompt', '').strip()

        if not prompt_text:
            return JsonResponse({
                'success': False,
                'error': 'Prompt mag niet leeg zijn'
            }, status=400)

        session_id = data.get('session_id')
        session = None
        if session_id:
            try:
                session = AgentSession.objects.get(id=session_id, is_active=True)
            except AgentSession.DoesNotExist:
                pass

        service = PromptAgentService()
        prompt_response = service.process_prompt(prompt_text, session=session)

        return JsonResponse({
            'success': True,
            'response': {
                'id': prompt_response.id,
                'prompt': prompt_response.prompt,
                'response': prompt_response.response,
                'model_used': prompt_response.model_used,
                'processing_time': prompt_response.processing_time,
                'created_at': prompt_response.created_at.isoformat(),
            }
        })

    except Exception as exc:
        return JsonResponse({
            'success': False,
            'error': str(exc)
        }, status=500)


def session_list(request):
    """List all agent sessions."""
    sessions = AgentSession.objects.all()
    return render(request, 'prompt_agent/session_list.html', {
        'sessions': sessions
    })


def session_create(request):
    """Create a new agent session."""
    if request.method == 'POST':
        form = AgentSessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            messages.success(request, f'Sessie "{session.name}" succesvol aangemaakt!')
            return redirect('session_list')
    else:
        form = AgentSessionForm()

    return render(request, 'prompt_agent/session_form.html', {
        'form': form,
        'title': 'Nieuwe Sessie Aanmaken'
    })


def session_edit(request, pk):
    """Edit an existing agent session."""
    session = get_object_or_404(AgentSession, pk=pk)

    if request.method == 'POST':
        form = AgentSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, f'Sessie "{session.name}" succesvol bijgewerkt!')
            return redirect('session_list')
    else:
        form = AgentSessionForm(instance=session)

    return render(request, 'prompt_agent/session_form.html', {
        'form': form,
        'title': f'Sessie Bewerken: {session.name}',
        'session': session
    })


def history(request):
    """View prompt history."""
    prompts = PromptResponse.objects.all()[:50]
    return render(request, 'prompt_agent/history.html', {
        'prompts': prompts
    })


def prompt_detail(request, pk):
    """View details of a specific prompt/response."""
    prompt = get_object_or_404(PromptResponse, pk=pk)
    return render(request, 'prompt_agent/prompt_detail.html', {
        'prompt': prompt
    })

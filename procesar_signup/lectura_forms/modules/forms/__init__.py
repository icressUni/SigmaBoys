"""
Google Forms integration module.
"""
from .handlers import (
    get_existing_watches, setup_watch, get_form_responses,
    delete_watch_by_id, list_all_watches
)

__all__ = [
    'get_existing_watches', 'setup_watch', 'get_form_responses',
    'delete_watch_by_id', 'list_all_watches'
]

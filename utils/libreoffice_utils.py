"""
LibreOffice utilities for dynamic command detection and usage.
"""
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)

_cached_libreoffice_cmd = None


def get_libreoffice_command() -> Optional[str]:
    """
    Get the working LibreOffice command dynamically.
    Uses caching to avoid repeated checks.
    
    Returns:
        str: The LibreOffice command that works, or None if none found
    """
    global _cached_libreoffice_cmd
    
    # Return cached result if available
    if _cached_libreoffice_cmd is not None:
        return _cached_libreoffice_cmd if _cached_libreoffice_cmd != "NONE" else None
    
    # List of commands to try, in order of preference
    commands_to_try = [
        # Generic symlink (preferred if available)
        'libreoffice-generic',
        # Common versioned commands (try newer versions first)
        'libreoffice25.2',
        'libreoffice24.8', 
        'libreoffice24.2',
        'libreoffice7.6',
        'libreoffice7.5',
        'libreoffice7.4',
        'libreoffice7.3',
        'libreoffice7.2',
        'libreoffice7.1',
        'libreoffice7.0',
        'libreoffice6.4',
        'libreoffice6.3',
        'libreoffice6.2',
        'libreoffice6.1',
        'libreoffice6.0',
        # Generic commands (less preferred)
        'libreoffice',
        'soffice'
    ]
    
    # Try to use the Python script for better detection
    try:
        result = subprocess.run(
            ['python3', '/app/scripts/get_libreoffice_cmd.py'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            cmd = result.stdout.strip()
            _cached_libreoffice_cmd = cmd
            logger.info(f"Found LibreOffice command via detection script: {cmd}")
            return cmd
    except Exception as e:
        logger.warning(f"Could not use LibreOffice detection script: {e}")
    
    # Fallback to manual testing
    for cmd in commands_to_try:
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and 'LibreOffice' in result.stdout:
                _cached_libreoffice_cmd = cmd
                logger.info(f"Found working LibreOffice command: {cmd}")
                return cmd
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    # No working command found
    _cached_libreoffice_cmd = "NONE"
    logger.error("No working LibreOffice command found")
    return None


def reset_libreoffice_command_cache():
    """Reset the cached LibreOffice command to force re-detection."""
    global _cached_libreoffice_cmd
    _cached_libreoffice_cmd = None
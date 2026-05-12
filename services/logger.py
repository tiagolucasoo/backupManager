def format_log(text: str, level: str = "info") -> str:
    prefix = {
        "success": "✔",
        "error": "✖",
        "warning": "⚠",
        "info": "●"
    }.get(level, "●")
    
    return f"{prefix} {text}\n"
def assume_content_type(file_path: str) -> str:
    # sourcery skip: assign-if-exp, reintroduce-else
    if file_path.endswith("html"):
        return "text/html"
    if file_path.endswith("json"):
        return "application/json"
    return ""

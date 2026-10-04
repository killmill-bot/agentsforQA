import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP


BASE_DIR = Path(os.getenv("FILE_READER_DIRECTORY", "./documents"))

mcp = FastMCP("file-system-reader")


def is_allowed_path(path: Path) -> bool:
    """Check that the path stays inside the configured base directory."""
    try:
        path.resolve().relative_to(BASE_DIR.resolve())
        return True
    except ValueError:
        return False


@mcp.tool()
def read_file(file_path: str) -> str:
    """Read a file from the configured directory."""
    try:
        resolved_path = (BASE_DIR / file_path).resolve()

        if not is_allowed_path(resolved_path):
            return "Access denied - invalid path"

        if not resolved_path.is_file():
            return "Error reading the given file: file not found"

        content = resolved_path.read_text(encoding="utf-8")
        return f"FILE: {resolved_path.name}\n\n{content}"

    except Exception as e:
        return f"Error reading the given file: {e}"


@mcp.tool()
def list_files() -> str:
    """List all files in the configured directory."""
    try:
        if not BASE_DIR.exists():
            BASE_DIR.mkdir(parents=True, exist_ok=True)

        files = [f for f in BASE_DIR.iterdir() if f.is_file()]

        return "\n".join(f.name for f in files)

    except Exception as e:
        return f"Error listing files: {e}"


if __name__ == "__main__":
    print(
        f"File System Reader MCP Server is running. "
        f"Base directory: {BASE_DIR.resolve()}"
    )
    mcp.run()
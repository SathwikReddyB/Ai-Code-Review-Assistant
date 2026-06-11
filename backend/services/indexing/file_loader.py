import os

SUPPORTED_EXTENSIONS = {
    ".py",
    ".java",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".cpp",
    ".c",
    ".go",
    ".md"
}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    ".next",
    "coverage",
    "__pycache__",
    "venv"
}


def load_repository_files(repo_path):

    documents = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
        ]

        files.sort(
            key=lambda x: (
                "readme" not in x.lower(),
                x.lower()
            )
        )

        for file in files:

            ext = os.path.splitext(file)[1].lower()

            is_readme = "readme" in file.lower()

            if ext not in SUPPORTED_EXTENSIONS and not is_readme:
                continue

            file_path = os.path.join(root, file)

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    content = f.read()

                documents.append({
                    "path": os.path.relpath(
                        file_path,
                        repo_path
                    ),
                    "content": content
                })

            except Exception:
                continue

    return documents
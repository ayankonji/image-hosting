---
{
  "name": "mimo_image",
  "description": "Upload a local image (from camera or IM) to a personal GitHub repository for remote LLM inspection. Use when the user wants to 'see' a local photo or when a skill needs to host an image for vision analysis.",
  "metadata": {
    "cap_groups": [
      "cap_lua"
    ],
    "manage_mode": "readonly"
  }
}
---

# GitHub Image Hosting

Use this skill when the user wants to upload a local image to GitHub so it can be inspected via URL, or when a workflow needs to host an image for vision models.

## Prerequisites

- The image must already exist on the local filesystem (e.g., captured by `take_picture` or saved from an IM channel).
- **A local configuration file is required:** Create `/fatfs/config/github_token.txt` and paste your GitHub Personal Access Token (with `repo` scope) inside. The script reads the token from this file to ensure security.

## Script Args Schema

```json
{
  "type": "object",
  "properties": {
    "image_path": {
      "type": "string",
      "description": "Absolute path to the local image file (e.g., /fatfs/inbox/photo.jpg)"
    },
    "filename": {
      "type": "string",
      "description": "Filename to use in the GitHub repository. If omitted, the original filename is used."
    }
  },
  "required": ["image_path"]
}
```

## Recommended Flow

1. Confirm the image exists at `image_path`.
2. Ensure `/fatfs/config/github_token.txt` contains a valid GitHub PAT.
3. Run the bundled script to upload the image.
4. Report the resulting GitHub URL to the user.

## Tool Call Inputs

Upload an image:
```json
{
  "path": "/fatfs/skills/mimo_image/scripts/upload_to_github.lua",
  "args": {
    "image_path": "/fatfs/inbox/webim/photo.jpg"
  }
}
```

## Script Behavior

- Reads the GitHub PAT from `/fatfs/config/github_token.txt`.
- Reads the local file and Base64-encodes it.
- Calls the GitHub Contents API to create/update the file in the `images/` directory.
- Prints the download URL on success.
- Prints an error message on failure.

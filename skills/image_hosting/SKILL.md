---
{
  "name": "image_hosting",
  "description": "Upload a local image to the GitHub image-hosting repository and get a public URL. Use when the user wants to host, share, or remotely inspect a local image.",
  "metadata": {
    "cap_groups": [
      "cap_lua"
    ],
    "manage_mode": "readonly"
  }
}
---

# Image Hosting

Use this skill when the user wants to upload a local image to GitHub for remote hosting, sharing, or vision model inspection.

## Prerequisites

- A GitHub Personal Access Token with `repo` scope is required.
- The image file must exist on the local device.

## Script Args Schema

```json
{
  "type": "object",
  "properties": {
    "image_path": {
      "type": "string",
      "description": "Absolute path to the local image file"
    },
    "github_token": {
      "type": "string",
      "description": "GitHub Personal Access Token with repo scope"
    },
    "filename": {
      "type": "string",
      "description": "Filename to use in the repo. Omit to use the original filename."
    }
  },
  "required": ["image_path", "github_token"]
}
```

## Recommended Flow

1. Ask the user for their GitHub token if not already provided.
2. Confirm the local image path.
3. Run the upload script with the image path and token.
4. Report the public URL on success.

## Tool Call Inputs

Upload an image:
```json
{
  "path": "/system/skills/image_hosting/scripts/upload_image.lua",
  "args": {
    "image_path": "/fatfs/inbox/photo.jpg",
    "github_token": "ghp_xxxxxxxxxxxx"
  }
}
```

## Script Behavior

- Reads the local image file and Base64-encodes it.
- Uses the GitHub Contents API to create/update the file under `images/` in the repository.
- Prints the raw download URL on success.
- Prints an error message on failure.

## Notes

- The token is never stored in the repository or skill files.
- Repo owner/name are configured in the script; fork and modify if needed.

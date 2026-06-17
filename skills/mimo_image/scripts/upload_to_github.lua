local storage = require("storage")
local json = require("json")
local capability = require("capability")

-- Configuration
local REPO_OWNER = "ayankonji"
local REPO_NAME = "image-hosting"
local TARGET_DIR = "images"
local TOKEN_FILE_PATH = "/fatfs/config/github_token.txt"

-- Read token from local file
local function get_github_token()
    if not storage.exists(TOKEN_FILE_PATH) then
        return nil, "GitHub Token file not found. Please create " .. TOKEN_FILE_PATH .. " containing your Personal Access Token."
    end
    local token = storage.read_file(TOKEN_FILE_PATH)
    if not token or token == "" then
        return nil, "GitHub Token file is empty."
    end
    return token, nil
end

local image_path = args and args.image_path
local filename = (args and args.filename) or nil

if not image_path then
    print("[mimo_image] ERROR: image_path is required")
    error("image_path is required")
end

-- Simple Base64 Encoder
local b64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
local function base64_encode(data)
    local result = {}
    for i = 1, #data, 3 do
        local a = data:byte(i) or 0
        local b = (i + 1 <= #data) and data:byte(i + 1) or 0
        local c = (i + 2 <= #data) and data:byte(i + 2) or 0
        local n = a * 65536 + b * 256 + c
        local idx1 = math.floor(n / 262144) + 1
        local idx2 = math.floor(n / 4096) % 64 + 1
        local idx3 = math.floor(n / 64) % 64 + 1
        local idx4 = n % 64 + 1
        table.insert(result, b64chars:sub(idx1, idx1))
        table.insert(result, b64chars:sub(idx2, idx2))
        table.insert(result, b64chars:sub(idx3, idx3))
        table.insert(result, b64chars:sub(idx4, idx4))
    end
    local pad = (3 - (#data % 3)) % 3
    for i = 1, pad do
        result[#result - i + 1] = '='
    end
    return table.concat(result)
end

local function safe_print(msg)
    print(string.format("[mimo_image] %s", tostring(msg)))
end

local function run()
    local GITHUB_TOKEN, err = get_github_token()
    if not GITHUB_TOKEN then
        safe_print("ERROR: " .. err)
        error(err)
    end

    if not storage.exists(image_path) then
        safe_print("ERROR: File not found: " .. image_path)
        error("File not found")
    end

    local content = storage.read_file(image_path)
    if not content then
        safe_print("ERROR: Failed to read file")
        error("Failed to read file")
    end

    local b64_content = base64_encode(content)
    if not filename then
        filename = image_path:match("([^/]+)$")
    end

    local path_in_repo = TARGET_DIR .. "/" .. filename
    local api_url = "https://api.github.com/repos/" .. REPO_OWNER .. "/" .. REPO_NAME .. "/contents/" .. path_in_repo

    -- Check if file exists to get SHA for update
    local ok_get, get_out = capability.call("http_request", {
        url = api_url,
        method = "GET",
        headers = {
            ["Authorization"] = "token " .. GITHUB_TOKEN,
            ["Accept"] = "application/vnd.github.v3+json"
        },
        timeout_ms = 15000,
    })

    local existing_sha = nil
    if ok_get and get_out then
        local ok_d, resp = pcall(json.decode, get_out)
        if ok_d and resp and resp.sha then
            existing_sha = resp.sha
        end
    end

    local payload = {
        message = "Upload image via ESP-Claw",
        content = b64_content,
    }
    if existing_sha then
        payload.sha = existing_sha
    end

    local headers = {
        ["Authorization"] = "token " .. GITHUB_TOKEN,
        ["Content-Type"] = "application/json",
        ["Accept"] = "application/vnd.github.v3+json"
    }

    local body_str = json.encode(payload)
    local ok, out, err = capability.call("http_request", {
        url = api_url,
        method = "PUT",
        headers = headers,
        body = body_str,
        timeout_ms = 60000,
    })

    if ok and out then
        -- Try to extract download_url using string pattern
        local url = out:match('"download_url"%s*:%s*"([^"]+)"')
        if url then
            safe_print("SUCCESS: " .. url)
        else
            safe_print("DONE_NO_URL: upload completed")
        end
    else
        safe_print("FAIL: " .. tostring(err))
        error("Upload failed")
    end
end

local ok, err = xpcall(run, debug.traceback)
if not ok then
    safe_print("FAILED: " .. tostring(err))
    error(err)
end

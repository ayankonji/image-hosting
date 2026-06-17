local arg_schema = require("arg_schema")
local storage = require("storage")
local json = require("json")
local capability = require("capability")

local ARG_SCHEMA = {
    image_path = arg_schema.string({}),
    github_token = arg_schema.string({}),
    filename = arg_schema.string({ default = nil }),
}

local ctx = arg_schema.parse(args, ARG_SCHEMA)

-- ===== 仓库配置 =====
local REPO_OWNER = "ayankonji"
local REPO_NAME = "image-hosting"
local TARGET_DIR = "images"
-- ====================

-- Base64 Encoder
local b64chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

local function base64_encode(data)
    return ((data:gsub('.', function(x)
        local r, b = '', x:byte()
        for i = 8, 1, -1 do
            r = r .. (b % 2 ^ i - b % 2 ^ (i - 1) > 0 and '1' or '0')
        end
        return r
    end) .. '0000'):gsub('%d%d%d?%d?%d?%d?', function(x)
        if #x ~= 6 then return '' end
        local c = 0
        for i = 1, 6 do
            c = c + (x:sub(i, i) == '1' and 2 ^ (6 - i) or 0)
        end
        return b64chars:sub(c + 1, c + 1)
    end) .. ({ '', '==', '=' })[#data % 3 + 1]
end

local function run()
    if not storage.exists(ctx.image_path) then
        print("[image_hosting] ERROR: File not found: " .. ctx.image_path)
        error("File not found")
    end

    local content = storage.read_file(ctx.image_path)
    if not content then
        print("[image_hosting] ERROR: Failed to read file")
        error("Failed to read file")
    end

    local b64_content = base64_encode(content)

    local filename = ctx.filename
    if not filename then
        filename = ctx.image_path:match("([^/]+)$")
    end

    local path_in_repo = TARGET_DIR .. "/" .. filename
    local api_url = "https://api.github.com/repos/" .. REPO_OWNER .. "/" .. REPO_NAME .. "/contents/" .. path_in_repo

    -- Check if file exists (to get SHA for update)
    local _, get_resp = pcall(function()
        local ok, out = capability.call("http_request", {
            url = api_url,
            method = "GET",
            headers = {
                ["Authorization"] = "token " .. ctx.github_token,
                ["Accept"] = "application/vnd.github.v3+json",
            },
            timeout_ms = 10000,
        })
        if ok and out then
            return json.decode(out)
        end
        return nil
    end)

    local payload = {
        message = "Upload image via ESP-Claw",
        content = b64_content,
    }

    -- Include SHA if file already exists (for update)
    if get_resp and get_resp.sha then
        payload.sha = get_resp.sha
    end

    local headers = {
        ["Authorization"] = "token " .. ctx.github_token,
        ["Content-Type"] = "application/json",
        ["Accept"] = "application/vnd.github.v3+json",
    }

    local ok, out, err = capability.call("http_request", {
        url = api_url,
        method = "PUT",
        headers = headers,
        body = json.encode(payload),
        timeout_ms = 30000,
    })

    if ok then
        local resp = json.decode(out)
        if resp and resp.content and resp.content.download_url then
            print("[image_hosting] SUCCESS: " .. resp.content.download_url)
        else
            print("[image_hosting] WARNING: Upload OK but URL parse failed. Response: " .. out)
        end
    else
        print("[image_hosting] ERROR: " .. tostring(err) .. " | " .. tostring(out))
        error("Upload failed")
    end
end

local ok, err = xpcall(run, debug.traceback)
if not ok then
    print("[image_hosting] FAILED: " .. tostring(err))
    error(err)
end

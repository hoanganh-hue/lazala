#!/usr/bin/env bash
set -euo pipefail

# BASE_URL: http://localhost:5000 or https://your-ngrok-domain
BASE_URL="${BASE_URL:-http://localhost:5000}"
# NGROK_BASIC_AUTH: optional user:pass when ngrok basic-auth is enabled
BASIC_AUTH="${NGROK_BASIC_AUTH:-}"
# USERNAME/PASSWORD for login tests (optional)
USERNAME="${USERNAME:-}"
PASSWORD="${PASSWORD:-}"

bearer=""

curl_json() { # path method [data]
  local path="$1"; shift || true
  local method="${1:-GET}"; shift || true
  local data="${1:-}"; shift || true
  local authHeader=()
  if [[ -n "$bearer" ]]; then authHeader+=(-H "Authorization: Bearer $bearer"); fi
  if [[ -n "$BASIC_AUTH" ]]; then authHeader+=(-u "$BASIC_AUTH"); fi
  local res
  if [[ -n "$data" ]]; then
    res=$(curl -s -w "\n%{http_code}" -X "$method" "${BASE_URL}${path}" -H "Content-Type: application/json" "${authHeader[@]}" --data "$data")
  else
    res=$(curl -s -w "\n%{http_code}" -X "$method" "${BASE_URL}${path}" "${authHeader[@]}")
  fi
  local body code
  body=$(echo "$res" | sed '$d')
  code=$(echo "$res" | tail -n1)
  echo "$code"
  echo "$body"
}

section() { echo; echo "==== $1 ===="; }

section "Health ${BASE_URL}/api/health"
code_body=$(curl_json "/api/health")
code=$(echo "$code_body" | head -n1)
body=$(echo "$code_body" | tail -n +2)
echo "HTTP $code"
echo "$body"

if [[ -n "$USERNAME" && -n "$PASSWORD" ]]; then
  section "Login /api/auth/login"
  loginBody="{\"username\":\"${USERNAME}\",\"password\":\"${PASSWORD}\"}"
  code_body=$(curl_json "/api/auth/login" "POST" "$loginBody" || true)
  code=$(echo "$code_body" | head -n1)
  body=$(echo "$code_body" | tail -n +2)
  echo "HTTP $code"
  echo "$body"
  token=$(echo "$body" | sed -n 's/.*"token":"\([^"]\+\)".*/\1/p' | head -n1 || true)
  if [[ -n "${token:-}" ]]; then
    bearer="$token"
    section "Me /api/auth/me"
    code_body=$(curl_json "/api/auth/me")
    echo "HTTP $(echo "$code_body" | head -n1)"
    echo "$(echo "$code_body" | tail -n +2)"

    section "Admin: List Users /api/users"
    code_body=$(curl_json "/api/users")
    echo "HTTP $(echo "$code_body" | head -n1)"
    echo "$(echo "$code_body" | tail -n +2)"
  else
    echo "Login failed or token missing."
  fi
fi

section "Devices /api/devices"
code_body=$(curl_json "/api/devices")
echo "HTTP $(echo "$code_body" | head -n1)"
echo "$(echo "$code_body" | tail -n +2)"

section "Audit /api/audit"
code_body=$(curl_json "/api/audit")
echo "HTTP $(echo "$code_body" | head -n1)"
echo "$(echo "$code_body" | tail -n +2)"

echo; echo "Done."


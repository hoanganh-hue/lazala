Windows Desktop app placeholder

This repository currently does not include a concrete desktop application implementation (Electron/Tauri). To align with the deployment plan (backend over Docker + ngrok, desktop client for Windows), use the guide in `HUONG_DAN_DESKTOP_APP.md` and the config template below.

Configuration
- Copy `desktop/config.example.json` to `desktop/config.json` and set `serverUrl` to your fixed ngrok domain.
- The desktop app should read this file at startup to know where the backend API is exposed.

Build & Packaging (to implement)
- Electron: follow steps in `HUONG_DAN_DESKTOP_APP.md` to scaffold `electron/` (main.js, preload.js) and wire the Angular or native UI.
- Configure electron-builder to create an NSIS installer for Windows.
- Ensure the app uses `serverUrl` from `desktop/config.json` for API calls.


// Electron main process (CommonJS)
const { app, BrowserWindow, Menu, ipcMain, shell } = require('electron');
const { autoUpdater } = require('electron-updater');
const path = require('path');
const fs = require('fs');

function loadConfig() {
  // Prefer desktop/config.json; fallback to desktop/config.example.json
  const root = process.cwd();
  const userConfigPath = path.resolve(root, 'desktop', 'config.json');
  const exampleConfigPath = path.resolve(root, 'desktop', 'config.example.json');
  let cfg = { serverUrl: 'http://localhost:5000', timeoutMs: 15000 };
  try {
    if (fs.existsSync(userConfigPath)) {
      cfg = JSON.parse(fs.readFileSync(userConfigPath, 'utf8'));
    } else if (fs.existsSync(exampleConfigPath)) {
      cfg = JSON.parse(fs.readFileSync(exampleConfigPath, 'utf8'));
    }
  } catch {}
  return cfg;
}

let mainWindow;

function createWindow() {
  const cfg = loadConfig();

  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.resolve(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      additionalArguments: [JSON.stringify({ serverUrl: cfg.serverUrl, timeoutMs: cfg.timeoutMs })],
    },
    show: false,
  });

  mainWindow.once('ready-to-show', () => mainWindow.show());
  mainWindow.loadFile(path.resolve(__dirname, 'index.html'));

  const template = [
    {
      label: 'DogeRat',
      submenu: [
        {
          label: 'Open API Docs',
          click: async () => {
            const { serverUrl } = loadConfig();
            shell.openExternal(`${serverUrl}/api-docs`);
          },
        },
        { type: 'separator' },
        { role: 'reload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'quit' },
      ],
    },
  ];
  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);

  // Auto-update (GitHub Releases)
  try {
    autoUpdater.autoDownload = true;
    autoUpdater.checkForUpdatesAndNotify();
  } catch {}
}

ipcMain.handle('get-server-url', async () => loadConfig().serverUrl);
ipcMain.handle('get-app-version', async () => app.getVersion());
ipcMain.handle('get-basic-auth', async () => loadConfig().basicAuth || '');

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

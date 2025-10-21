// Global teardown to close DB pools and sockets after ALL test suites
export default async function globalTeardown() {
  try {
    const { sequelize } = await import('./server/models');
    if (sequelize) {
      await sequelize.close();
    }
  } catch {}

  try {
    const mod: any = await import('./server/index');
    const io = mod.io;
    const server = mod.server;

    if (io) {
      try { io.removeAllListeners(); } catch {}
      try { io.disconnectSockets(true); } catch {}
      try { io.close(); } catch {}
    }

    if (server && typeof server.listening !== 'undefined' && server.listening) {
      await new Promise<void>((resolve) => {
        try { server.close(() => resolve()); } catch { resolve(); }
      });
    }
  } catch {}
}


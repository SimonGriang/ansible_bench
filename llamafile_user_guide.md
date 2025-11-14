# `llamafile` Cheat Sheet & User Guide

`llamafile` is a Python-based worker/service framework (or a CLI tool) that may spawn child processes to handle tasks. This guide covers common usage, CLI commands, process management, and troubleshooting.

---

## 1. Installing `llamafile`

```bash
# Using pip
pip install llamafile

# Verify installation
llamafile --version
```

---

## 2. Basic CLI Usage

```bash
# Start a worker/service
llamafile run

# Specify a configuration file
llamafile run --config config.yaml

# Run in daemon mode (background)
llamafile run --daemon
```

---

## 3. Common Options

| Option | Description |
|--------|-------------|
| `--config <file>` | Path to configuration file |
| `--daemon` | Run as a background process |
| `--workers <n>` | Number of worker processes to spawn |
| `--port <port>` | Specify the port for HTTP/REST API |
| `--log-level <level>` | Set log verbosity (`info`, `debug`, `warn`) |

---

## 4. Health Checks

```bash
# Check health of the service
curl -v http://localhost:8097/health

# Get only HTTP status code
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8097/health
```

---

## 5. Process Management

`llamafile` may leave orphaned or zombie processes if not properly terminated.

### List `llamafile` processes:
```bash
ps aux | grep llamafile
```

### Kill all `llamafile` processes:
```bash
pkill -9 -f llamafile
```

### Kill selectively:
```bash
kill -9 <PID>
```

### Avoid killing SSH / login shells
```bash
sudo ps -u <username> -o pid,comm | \
awk '$2!="sshd" && $2!="bash" && $2!="zsh"' | \
xargs -r sudo kill -9
```

---

## 6. Logging

```bash
# Set log level
llamafile run --log-level debug

# Check log file (if configured)
tail -f /var/log/llamafile.log
```

---

## 7. Configuration Tips

- Worker count: Set according to CPU cores and workload:
```yaml
workers: 4
```

- Timeout: Ensure proper timeouts to prevent zombie processes.
```yaml
timeout: 300
```

- Port: Default may be 8097; adjust if conflicts occur:
```yaml
port: 8098
```

---

## 8. Troubleshooting

| Problem | Solution |
|---------|---------|
| Orphaned processes after Ctrl+C | Use `pkill -9 -f llamafile` |
| Service not responding | Check logs with `tail -f` and restart |
| Port conflict | Change port in config or with `--port` |
| High CPU usage | Reduce number of workers or increase timeout |

---

## 9. Example Workflow

```bash
# Start service in daemon mode with 4 workers
llamafile run --workers 4 --daemon --config config.yaml

# Verify it's running
ps aux | grep llamafile

# Health check
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8097/health

# Stop all workers safely
pkill -9 -f llamafile
```

---

## Notes

- Always use `--config` to ensure consistent settings.
- Monitor your system to avoid zombie/orphaned workers.
- Use `htop` or `ps` to verify active processes.
- Combine with systemd or `tmux` for more stable long-running services.

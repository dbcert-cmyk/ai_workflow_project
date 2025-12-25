# AI Workspace - M4 Mac Mini

## Location
`/Volumes/ai/dev/ai-workspace`

## What's Running
- **MLX-LM Server**: OpenAI-compatible API on port 8080
- **Model**: Qwen 2.5 Coder 14B (4-bit quantized)
- **Process Manager**: PM2

## Quick Commands

### Start Everything
```bash
cd /Volumes/ai/dev/ai-workspace
./scripts/start.sh
```

### Stop Everything (Reclaim ~10-12GB RAM)
```bash
./scripts/stop.sh
```

### Check Status
```bash
pm2 status
```

### View Logs
```bash
pm2 logs mlx-llm-server
```

### Restart Service
```bash
pm2 restart mlx-llm-server
```

## API Usage

### Test the API
```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mlx-community/Qwen2.5-Coder-14B-Instruct-4bit",
    "messages": [{"role": "user", "content": "Your prompt here"}],
    "max_tokens": 200
  }'
```

### List Available Models
```bash
curl http://localhost:8080/v1/models
```

## Resources

### Memory Usage
- Model loaded: ~8-10GB RAM
- Total with server: ~10-12GB RAM
- When stopped: 0GB

### File Structure
```
/Volumes/ai/dev/ai-workspace/
├── venv/                    # Python virtual environment
├── models/
│   └── mlx-models/         # Downloaded models
├── servers/
│   └── mlx_server.py       # FastAPI server
├── scripts/
│   ├── start.sh            # Start services
│   └── stop.sh             # Stop services
├── mcp-servers/
│   └── config.json         # MCP configuration (future)
├── projects/               # Your future projects
└── ecosystem.config.js     # PM2 configuration
```

## Adding Future Projects

### FastAPI App
```bash
mkdir projects/my-app
cd projects/my-app
source ../../venv/bin/activate
# Build your app, it can call http://localhost:8080 for LLM
```

### Use in Python
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="mlx-community/Qwen2.5-Coder-14B-Instruct-4bit",
    messages=[{"role": "user", "content": "Help me code"}]
)
print(response.choices[0].message.content)
```

## Troubleshooting

### Port Already in Use
```bash
lsof -ti:8080 | xargs kill -9
pm2 restart mlx-llm-server
```

### Model Not Loading
Check logs: `pm2 logs mlx-llm-server`

### Out of Memory
Stop other applications or reduce model size (use smaller quantization)

## Next Steps

1. ✅ MLX-LM server working
2. ⏳ Add MCP servers (file editing, web search)
3. ⏳ Add Stable Diffusion (image generation)
4. ⏳ Build your FastAPI apps and agents

## Backup
- Bootable clone: [Your backup drive location]
- Models cache: `~/.cache/huggingface/`
- Workspace: `/Volumes/ai/dev/ai-workspace/`

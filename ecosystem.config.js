module.exports = {
  apps: [
    {
      name: 'mlx-llm-server',
      script: 'servers/mlx_server.py',
      interpreter: '/Volumes/ai/dev/ai-workspace/venv/bin/python',
      cwd: '/Volumes/ai/dev/ai-workspace',
      env: {
        MLX_WIRED_LIMIT: '1'
      }
    }
  ]
};

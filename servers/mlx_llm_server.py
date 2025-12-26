#!/usr/bin/env python3
"""
MLX-LM Server - OpenAI-compatible API
"""

import os

os.environ["MLX_WIRED_LIMIT"] = "1"

if __name__ == "__main__":
    import sys

    from mlx_lm import server

    # Run with default settings: host=127.0.0.1, port=8080
    sys.exit(
        server.run(
            host="127.0.0.1",
            port=8080,
            model_provider=None,  # type: ignore # Models loaded on-demand from requests
        )
    )

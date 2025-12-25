#!/bin/bash
cd /Volumes/ai/dev/ai-workspace
pm2 start ecosystem.config.js
echo "✅ AI Workspace Started"
pm2 status

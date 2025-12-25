#!/bin/bash
pm2 stop all
echo "✅ AI Workspace Stopped - Memory Reclaimed"
pm2 status

#!/bin/bash
set -e

echo "📦 Packaging ADK Agent for Terraform Deployment..."

# 1. Clean build directory
BUILD_DIR="build_tmp"
rm -rf ${BUILD_DIR}
mkdir -p ${BUILD_DIR}/agents

# 2. Copy agent source code and requirements
cp -r agents/* ${BUILD_DIR}/agents/
cp requirements.txt ${BUILD_DIR}/

# 3. Create the ADK App Wrapper (Agent Engine FastAPI Entrypoint)
# This mimics the internal behavior of the `adk deploy` CLI.
cat << 'EOF' > ${BUILD_DIR}/agents/agent_engine_app.py
import os
import vertexai
from vertexai.agent_engines import AdkApp
from .agent import root_agent

vertexai.init(
    project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
    location=os.environ.get("GOOGLE_CLOUD_LOCATION"),
)

# Expose the ADK standard API (stream_query, create_session, etc.)
adk_app = AdkApp(
    agent=root_agent,
    enable_tracing=None,
)
EOF

# 4. Create the source archive for Terraform inline_source
cd ${BUILD_DIR}
tar -czvf ../infra/source.tar.gz agents/ requirements.txt
cd ..

# 5. Cleanup
rm -rf ${BUILD_DIR}

echo "✅ Successfully created infra/source.tar.gz!"
echo "You can now run 'terraform apply' in the infra/ directory."

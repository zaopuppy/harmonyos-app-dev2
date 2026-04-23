# HarmonyOS Dev Environment Setup
# Source this script before using hdc, hvigorw, or ohpm
# Usage: source setup_env.sh

# Derive DEVECO_SDK_HOME from hdc if not set
if [ -z "$DEVECO_SDK_HOME" ]; then
    HDC_PATH=$(which hdc 2>/dev/null)
    if [ -n "$HDC_PATH" ]; then
        # hdc is at $DEVECO_SDK_HOME/default/openharmony/toolchains/hdc
        DEVECO_SDK_HOME=$(dirname $(dirname $(dirname $(dirname $(dirname $HDC_PATH)))))
        export DEVECO_SDK_HOME
        echo "DEVECO_SDK_HOME derived from hdc: $DEVECO_SDK_HOME"
    else
        echo "DEVECO_SDK_HOME not set and hdc not found in PATH"
        return 1 2>/dev/null || exit 1
    fi
fi

# Set DEVECO_HOME (parent of SDK root)
DEVECO_HOME=$(dirname "$DEVECO_SDK_HOME")
export DEVECO_HOME

# Add tools to PATH
export PATH="$DEVECO_SDK_HOME/default/openharmony/toolchains:$DEVECO_HOME/tools/node:$DEVECO_HOME/tools/ohpm/bin:$DEVECO_HOME/tools/hvigor/bin:$PATH"

echo "Environment configured:"
echo "  DEVECO_SDK_HOME=$DEVECO_SDK_HOME"
echo "  DEVECO_HOME=$DEVECO_HOME"
echo "  PATH updated"

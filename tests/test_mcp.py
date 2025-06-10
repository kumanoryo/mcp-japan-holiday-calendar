import subprocess
import json
import sys

def test_mcp_server():
    # Start the Docker container
    process = subprocess.Popen(
        ['docker', 'run', '-i', '--rm', 'mcp-japan-holiday'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Initialize MCP connection
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }
    
    # Send initialize message
    process.stdin.write(json.dumps(init_message) + '\n')
    process.stdin.flush()
    
    # Read response
    response = process.stdout.readline()
    print("Initialize response:", response.strip())
    
    # Send initialized notification
    initialized_message = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    process.stdin.write(json.dumps(initialized_message) + '\n')
    process.stdin.flush()
    
    # Call get_next_holiday tool
    tool_call = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_next_holiday",
            "arguments": {}
        }
    }
    
    process.stdin.write(json.dumps(tool_call) + '\n')
    process.stdin.flush()
    
    # Read tool response
    tool_response = process.stdout.readline()
    print("Tool response:", tool_response.strip())
    
    # Parse and extract the result
    try:
        response_data = json.loads(tool_response)
        if 'result' in response_data and 'content' in response_data['result']:
            for content in response_data['result']['content']:
                if content['type'] == 'text':
                    print("次の休日:", content['text'])
    except:
        print("Failed to parse response")
    
    process.terminate()

if __name__ == "__main__":
    test_mcp_server()

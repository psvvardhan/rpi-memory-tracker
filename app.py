from flask import Flask, render_template, jsonify
import subprocess
import re
from datetime import datetime

app = Flask(__name__)

def get_host_storage_info():
    """Get SD card storage information from the host system."""
    try:
        # Execute df command on the host filesystem
        # We need to mount the host's /proc to access this information
        result = subprocess.run(
            ["df", "-h", "/host-root"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the output (example: /dev/root 29G 11G 17G 40% /)
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            raise ValueError("Unexpected df output format")
        
        # Get the line for the root filesystem
        fs_line = lines[1].split()
        if len(fs_line) < 6:
            raise ValueError("Unexpected df output format")
        
        # Extract values - format varies but usually columns are:
        # Filesystem, Size, Used, Avail, Use%, Mounted on
        total_str = fs_line[1]
        used_str = fs_line[2]
        free_str = fs_line[3]
        percent_str = fs_line[4]
        
        # Convert to numeric values (removing G suffix)
        total_gb = float(re.sub(r'[^0-9.]', '', total_str))
        used_gb = float(re.sub(r'[^0-9.]', '', used_str))
        free_gb = float(re.sub(r'[^0-9.]', '', free_str))
        percent_used = float(re.sub(r'[^0-9.]', '', percent_str))
        
        return {
            'total': total_gb,
            'used': used_gb,
            'free': free_gb,
            'percent': percent_used,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
    except Exception as e:
        print(f"Error getting host storage info: {e}")
        # Return default values in case of error
        return {
            'total': 0,
            'used': 0,
            'free': 0,
            'percent': 0,
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'error': str(e)
        }

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html', storage=get_host_storage_info())

@app.route('/storage')
def storage():
    """API endpoint to get the current storage usage."""
    return jsonify(get_host_storage_info())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

#!/usr/bin/env python3
"""
Auto-fix script for network topology animation issues
Automatically integrates the topology animation fix into the HTML file
"""

import os
import re

def fix_topology_animations():
    """Fix the mesh topology animation issues"""
    
    html_file = 'templates/index.html'
    js_file = 'static/js/topology_animations.js'
    
    # Check if files exist
    if not os.path.exists(html_file):
        print(f"❌ Error: {html_file} not found!")
        return False
        
    if not os.path.exists(js_file):
        print(f"❌ Error: {js_file} not found!")
        return False
    
    # Read the HTML file
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"❌ Error reading HTML file: {e}")
        return False
    
    # Check if the script is already included
    if '/static/js/topology_animations.js' in html_content:
        print("✅ Topology animations script is already included!")
        return True
    
    # Find the closing body tag and add the script before it
    script_tag = '    <script src="/static/js/topology_animations.js"></script>\n'
    
    if '</body>' in html_content:
        # Insert before closing body tag
        html_content = html_content.replace('</body>', f'{script_tag}</body>')
        
        # Write back to file
        try:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("✅ Successfully integrated topology animation fix!")
            print("📁 Added script reference to HTML file")
            return True
        except Exception as e:
            print(f"❌ Error writing HTML file: {e}")
            return False
    else:
        print("❌ Could not find </body> tag in HTML file!")
        return False

def verify_fix():
    """Verify that the fix is working"""
    print("\n🔍 Verifying the fix...")
    
    js_file = 'static/js/topology_animations.js'
    html_file = 'templates/index.html'
    
    # Check JavaScript file
    if os.path.exists(js_file):
        print("✅ Enhanced animation JavaScript file exists")
        
        with open(js_file, 'r') as f:
            js_content = f.read()
            if 'animateMeshDataFlow' in js_content:
                print("✅ Mesh topology animation function found")
            else:
                print("❌ Mesh animation function not found in JS file")
                return False
    else:
        print("❌ Animation JavaScript file missing")
        return False
    
    # Check HTML integration
    if os.path.exists(html_file):
        with open(html_file, 'r') as f:
            html_content = f.read()
            if '/static/js/topology_animations.js' in html_content:
                print("✅ Script correctly referenced in HTML")
            else:
                print("❌ Script not referenced in HTML file")
                return False
    
    return True

def main():
    print("🔧 Network Topology Animation Fix Tool")
    print("=" * 50)
    
    # Change to the correct directory
    if os.path.basename(os.getcwd()) != '5G_6G_ORAN_repo':
        # Try to find the repo directory
        if os.path.exists('5G_6G_ORAN_repo'):
            os.chdir('5G_6G_ORAN_repo')
        elif os.path.exists('../5G_6G_ORAN_repo'):
            os.chdir('../5G_6G_ORAN_repo')
        else:
            print("❌ Could not find 5G_6G_ORAN_repo directory!")
            print("Please run this script from within the repository directory.")
            return
    
    print(f"📂 Working in: {os.getcwd()}")
    
    # Apply the fix
    if fix_topology_animations():
        if verify_fix():
            print("\n🎉 Topology animation fix applied successfully!")
            print("\n📋 Next Steps:")
            print("1. Start your Flask server: python flask_telecom_server.py")
            print("2. Open http://localhost:5000 in your browser")
            print("3. Go to the Network Topology section")
            print("4. Click 'Mesh Topology' then 'Simulate Data Flow'")
            print("5. Enjoy the enhanced mesh topology animation! 🌟")
        else:
            print("\n❌ Fix verification failed. Please check the files manually.")
    else:
        print("\n❌ Failed to apply the fix. Please check the error messages above.")

if __name__ == "__main__":
    main()

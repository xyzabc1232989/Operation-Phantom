import os
import stat
from collections import defaultdict

def scan_usb_files(mount_point):
    if not mount_point or not os.path.exists(mount_point):
        return {'error': 'Mount point not accessible'}
    
    file_counts = defaultdict(int)
    file_extensions = defaultdict(int)
    total_files = 0
    
    # Define file type categories
    categories = {
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.ico', '.svg', '.raw', '.heic'],
        'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg'],
        'executables': ['.exe', '.msi', '.app', '.bin', '.sh', '.bat', '.cmd', '.com', '.scr', '.dll'],
        'scripts': ['.py', '.js', '.vbs', '.ps1', '.pl', '.rb', '.php', '.asp', '.jsp', '.lua'],
        'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.iso', '.dmg']
    }
    
    try:
        for root, dirs, files in os.walk(mount_point):
            # Skip system directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['System Volume Information', '$RECYCLE.BIN']]
            
            for file in files:
                total_files += 1
                ext = os.path.splitext(file)[1].lower()
                file_extensions[ext] += 1
                
                # Categorize
                for category, extensions in categories.items():
                    if ext in extensions:
                        file_counts[category] += 1
                        break
                else:
                    file_counts['other'] += 1
                
                # Break if too many files to avoid performance issues
                if total_files > 5000:
                    break
            if total_files > 5000:
                break
    except Exception as e:
        return {'error': str(e)}
    
    return {
        'total_files': total_files,
        'documents': file_counts.get('documents', 0),
        'images': file_counts.get('images', 0),
        'videos': file_counts.get('videos', 0),
        'executables': file_counts.get('executables', 0),
        'scripts': file_counts.get('scripts', 0),
        'archives': file_counts.get('archives', 0),
        'other': file_counts.get('other', 0),
        'top_extensions': dict(sorted(file_extensions.items(), key=lambda x: x[1], reverse=True)[:5])
    }

def scan_hidden_files(mount_point):
    if not mount_point or not os.path.exists(mount_point):
        return {'error': 'Mount point not accessible', 'hidden_files': 0}
    
    hidden_files = []
    total_scanned = 0
    
    try:
        for root, dirs, files in os.walk(mount_point):
            dirs[:] = [d for d in dirs if d not in ['System Volume Information', '$RECYCLE.BIN']]
            
            for file in files:
                total_scanned += 1
                filepath = os.path.join(root, file)
                try:
                    # Check if hidden (Unix: starts with ., Windows: hidden attribute)
                    if os.name == 'posix':
                        is_hidden = file.startswith('.')
                    else:
                        # On Windows, check for hidden attribute
                        st = os.stat(filepath)
                        is_hidden = bool(st.st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN) if hasattr(stat, 'FILE_ATTRIBUTE_HIDDEN') else file.startswith('.')
                    
                    if is_hidden:
                        hidden_files.append({
                            'name': file,
                            'path': filepath,
                            'size': os.path.getsize(filepath)
                        })
                except Exception:
                    pass
                
                if total_scanned > 2000:
                    break
            if total_scanned > 2000:
                break
    except Exception as e:
        return {'error': str(e), 'hidden_files': len(hidden_files)}
    
    return {
        'hidden_files': len(hidden_files),
        'total_scanned': total_scanned,
        'sample': hidden_files[:5]
    }
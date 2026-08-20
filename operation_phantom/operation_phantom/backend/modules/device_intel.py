import os
import glob

def get_profile(mount_point):
    if not mount_point or not os.path.exists(mount_point):
        return {'error': 'Device not accessible'}
    
    file_count = 0
    folder_count = 0
    largest_file = {'name': '', 'size': 0}
    total_size = 0
    
    try:
        for root, dirs, files in os.walk(mount_point):
            # Skip system directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['System Volume Information', '$RECYCLE.BIN']]
            
            folder_count += len(dirs)
            
            for file in files:
                file_count += 1
                filepath = os.path.join(root, file)
                try:
                    size = os.path.getsize(filepath)
                    total_size += size
                    if size > largest_file['size']:
                        largest_file = {'name': file, 'size': size}
                except Exception:
                    pass
                
                # Limit scan for performance
                if file_count > 3000:
                    break
            if file_count > 3000:
                break
    except Exception as e:
        return {'error': str(e)}
    
    # Convert sizes to human readable
    def format_size(size_bytes):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    return {
        'files': file_count,
        'folders': folder_count,
        'largest_file': largest_file['name'],
        'largest_file_size': format_size(largest_file['size']),
        'total_data': format_size(total_size),
        'device_name': os.path.basename(mount_point)
    }
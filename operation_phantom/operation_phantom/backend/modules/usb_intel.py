import psutil
import os

def scan():
    usb_devices = []
    
    try:
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            # Check if it's likely a USB drive
            if 'removable' in partition.opts or 'usb' in partition.device.lower():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    size_gb = usage.total / (1024**3)
                    
                    # Get volume name
                    volume_name = os.path.basename(partition.mountpoint)
                    if partition.device:
                        volume_name = partition.device.split('/')[-1]
                    
                    usb_devices.append({
                        'name': volume_name,
                        'mount_point': partition.mountpoint,
                        'size_gb': round(size_gb, 1),
                        'used_gb': round(usage.used / (1024**3), 1),
                        'free_gb': round(usage.free / (1024**3), 1),
                        'filesystem': partition.fstype
                    })
                except Exception:
                    pass
    except Exception as e:
        print(f"USB scan error: {e}")
    
    return {
        'devices': usb_devices,
        'detected': len(usb_devices) > 0
    }
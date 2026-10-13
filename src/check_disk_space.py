
import shutil

drive = "C:\\"
usage = shutil.disk_usage(drive)

print(f"Total disk space: {usage.total / (1024**3):.2f} GB")
print(f"Used disk space: {usage.used / (1024**3):.2f} GB")
print(f"Free disk space: {usage.free / (1024**3):.2f} GB")

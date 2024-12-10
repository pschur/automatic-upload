import os
from ftplib import FTP

def upload_folder(ftp_conn, local_dir, remote_dir):
    """
    Recursively upload a folder and its contents to an FTP server.
    
    :param ftp_conn: FTP connection object
    :param local_dir: Local directory to upload
    :param remote_dir: Remote directory path
    """
    # Ensure the remote directory exists
    try:
        ftp_conn.cwd(remote_dir)
    except Exception:
        ftp_conn.mkd(remote_dir)
        ftp_conn.cwd(remote_dir)

    # Walk through local directory
    for item in os.listdir(local_dir):
        local_path = os.path.join(local_dir, item)
        remote_path = f"{remote_dir}/{item}"

        if os.path.isdir(local_path):
            # Recursively upload subfolders
            upload_folder(ftp_conn, local_path, remote_path)
        else:
            # Upload file
            with open(local_path, "rb") as file:
                ftp_conn.storbinary(f"STOR {remote_path}", file)
                print(f"Uploaded: {local_path} to {remote_path}")

def main():
    # FTP server details
    ftp_host = "ftp.example.com"  # Replace with your FTP host
    ftp_user = "your-ftp-username"  # Replace with your FTP username
    ftp_pass = "your-ftp-password"  # Replace with your FTP password

    # Paths
    local_directory = "/path/to/local/folder"  # Replace with the local folder
    remote_directory = "/path/to/remote/folder"  # Replace with the remote folder

    # Connect to FTP server
    ftp = FTP(ftp_host)
    ftp.login(user=ftp_user, passwd=ftp_pass)

    print(f"Connected to {ftp_host}")

    # Start uploading
    upload_folder(ftp, local_directory, remote_directory)

    # Close connection
    ftp.quit()
    print("Upload complete.")

if __name__ == "__main__":
    main()

import paramiko
from tkinter import messagebox


class SFTPClient:
    def __init__(self):
        self.host = '172.30.1.33'
        self.port = 22
        self.username = 'bc'
        self.password = 'love1357!!'
        self.open_connection()

    def open_connection(self):
        # SSH 객체 생성 및 연결
        transport = paramiko.Transport((self.host, self.port))
        # SSH 인증
        transport.connect(username=self.username, password=self.password)
        # 연결 객체 저장
        self._connection = transport

    def close_connection(self):
        if hasattr(self, '_connection'):
            self._connection.close()

    # local 파일을 원격 서버로 업로드
    def upload_file(self, local_path, remote_path):
        sftp = paramiko.SFTPClient.from_transport(self._connection)
        sftp.put(local_path, remote_path)
        sftp.close()
        if self._connection.is_active():
            sftp = paramiko.SFTPClient.from_transport(self._connection)
            sftp.put(local_path, remote_path)
            sftp.close()
            messagebox.showinfo("알림", "파일 업로드 성공")
        else:
            messagebox.showwarning("경고", "연결되지 않음")

    # 원격 파일을 local로 다운로드
    def download_file(self, remote_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self._connection)
        sftp.get(remote_path, local_path)
        sftp.close()

    # 원격 경로에서 파일 목록 가져오기
    def get_files_in_remote_path(self, remote_path):
        sftp = paramiko.SFTPClient.from_transport(self._connection)
        files = sftp.listdir(remote_path)
        sftp.close()
        return files

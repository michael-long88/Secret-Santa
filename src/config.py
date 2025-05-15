import ssl
from dataclasses import dataclass


@dataclass
class Config:
    port: int
    username: str
    password: str
    sender_email: str
    smtp_server: str
    ssl_context: ssl.SSLContext

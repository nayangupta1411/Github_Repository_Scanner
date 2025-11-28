SENSITIVE_FILES = [
    ".env", "id_rsa", "id_rsa.pub", "config.json", "secrets.yml",
    "credentials.json", "private.key", "key.pem"
]

SECRET_PATTERNS = {
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "Generic Token": r"[A-Za-z0-9_]{20,}",
    "JWT": r"eyJ[A-Za-z0-9-_]+?\.[A-Za-z0-9-_]+?\.[A-Za-z0-9-_]+"
}
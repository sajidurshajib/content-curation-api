import bcrypt


class PasswordHasher:
	@staticmethod
	def hash_password(password: str) -> str:
		"""
		Hashes a password using bcrypt.
		"""
		password_bytes = password.encode('utf-8')
		hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
		return hashed.decode('utf-8')

	@staticmethod
	def verify_password(password: str, hashed_password: str) -> bool:
		"""
		Verifies a password against a hashed password.
		"""
		password_bytes = password.encode('utf-8')
		hashed_password_bytes = hashed_password.encode('utf-8')
		return bcrypt.checkpw(password_bytes, hashed_password_bytes)

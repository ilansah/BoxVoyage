import hashlib

class Users : 
    """Represents a user account with username and hashed password."""
    
    def __init__ (self, username  , password) :
        self.username = username
        # Hash the password with SHA256 to avoid storing it in plain text
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()


    def to_dict(self) : 
        """Converts the user to a dictionary for saving to JSON."""
        return { 'username' : self.username,'password_hash' : self.password_hash }

    @classmethod
    def from_dict(cls, data: dict):
        """Reconstructs a User from a JSON dictionary (without re-hashing the password)."""
        # Create the object without calling __init__ to avoid re-hashing the hash
        user = cls.__new__(cls)
        user.username = data["username"]
        user.password_hash = data["password_hash"]
        return user
    

class AuthManager:
    """Manages user registration, login, and session."""
    
    def __init__(self, storage):
        self.storage = storage
        self._current_user = None
        self._users = self.storage.load()
    
    def register(self, username: str, password: str):
        if username in self._users:
            raise ValueError("Username already taken")
        user = Users(username, password)
        self._users[username] = user.to_dict()
        self.storage.save(self._users)

        return user
    
    def login(self, username: str, password: str):
        if username not in self._users:
            raise ValueError("User not found")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != self._users[username]["password_hash"]:
            raise ValueError("Incorrect password")
        user = Users.from_dict(self._users[username])
        self._current_user = user
        return user
    
    def get_current_user(self):
        return self._current_user
    
    def logout(self):
        self._current_user = None

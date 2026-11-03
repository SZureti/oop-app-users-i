class User:
    # Class variable: every post from every user, kept in sync with each user's own `posts` list
    all_posts = []
    _next_post_id = 1

    def __init__(self, username, email, age, phone, license, location):
        self.username = username
        self.email = email  # validated by the email property
        self.age = age  # will possibly be used for age-related validations and features
        self.phone = phone  # validated by the phone property
        self.license = license  # validated by the license property
        self.location = location  # later will configure time zone by location
        self.posts = []  # Instance property: this user's posts

    # ---------- Display ----------

    # License is stored privately (_license); only the last 4 characters are shown
    def __str__(self):
        return f"User(username={self.username}, email={self.email}, age={self.age}, phone={self.phone}, license={self._license[-4:] if self._license else None}, location={self.location})"

    def __repr__(self):
        return f"User(username={self.username!r}, email={self.email!r}, age={self.age!r}, phone={self.phone!r}, license={self._license[-4:] if self._license else None!r}, location={self.location!r})"

    def __eq__(self, other):
        if isinstance(other, User):
            return (self.username == other.username and self.email == other.email and self.age == other.age
                    and self.phone == other.phone and self.license == other.license and self.location == other.location)
        return False

    def __hash__(self):
        return hash((self.username, self.email, self.age, self.phone, self.license, self.location))

    def to_dict(self):
        return {"username": self.username, "email": self.email, "age": self.age, "phone": self.phone, "license": self.license, "location": self.location}

    @classmethod
    def from_dict(cls, data):
        return cls(username=data["username"], email=data["email"], age=data["age"], phone=data["phone"], license=data["license"], location=data["location"])

    # ---------- Validated properties ----------

    @property
    def license(self):
        return self._license if self._license else None

    @license.setter
    def license(self, value):
        if not value or len(value) < 4:
            raise ValueError("Invalid license number")
        self._license = value

    @property
    def email(self):
        return self._email if self._email else None

    @email.setter
    def email(self, value):
        if not value or "@" not in value:
            raise ValueError("Invalid email address")
        self._email = value

    @property
    def phone(self):
        return self._phone if self._phone else None

    @phone.setter
    def phone(self, value):
        if not value or len(value) < 10:
            raise ValueError("Invalid phone number")
        self._phone = value

    # ---------- Updates ----------

    def update_email(self, new_email):
        self.email = new_email
        return self

    def update_username(self, new_username):
        self.username = new_username
        return self

    def update(self, new_username=None, new_email=None):
        if new_username is not None:
            self.username = new_username
        if new_email is not None:
            self.email = new_email
        return self

    # Format phone number to (XXX) XXX-XXXX
    def format_phone(self, phone):
        if phone:
            phone = phone.replace("-", "").replace(" ", "")
            if len(phone) == 10:
                return f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"
        return phone

    def update_phone(self, new_phone):
        self.phone = self.format_phone(new_phone)
        return self

    def copy(self):
        return User(username=self.username, email=self.email, age=self.age, phone=self.phone, license=self.license, location=self.location)

    def merge(self, other):
        if isinstance(other, User):
            if other.username is not None:
                self.username = other.username
            if other.email is not None:
                self.email = other.email
            if other.age is not None:
                self.age = other.age
            if other.phone is not None:
                self.phone = other.phone
            if other.license is not None:
                self.license = other.license
            if other.location is not None:
                self.location = other.location
        return self

    # ---------- Posts ----------

    def create_post(self, content):
        """Create a post for this user. Stored on the user AND in the class-wide list."""
        post = {"id": User._next_post_id, "author": self.username, "content": content}
        User._next_post_id += 1
        self.posts.append(post)
        User.all_posts.append(post)
        return post

    def delete_post(self, post):
        """Delete a post (the post dict or its id) from this user and from the class-wide list."""
        post_id = post["id"] if isinstance(post, dict) else post
        for p in self.posts:
            if p["id"] == post_id:
                self.posts.remove(p)
                User.all_posts.remove(p)
                return True
        return False  # not one of this user's posts

    # ---------- State checks ----------

    def is_valid(self):
        return self.username is not None and self.email is not None and self.age is not None and self.phone is not None and self.license is not None and self.location is not None

    def is_empty(self):
        return self.username is None and self.email is None and self.age is None and self.phone is None and self.license is None and self.location is None

    # clear/reset set the private fields directly so the validating setters are bypassed
    def clear(self):
        self.username = None
        self._email = None
        self.age = None
        self._phone = None
        self._license = None
        self.location = None
        return self

    def is_cleared(self):
        return self.is_empty()

    def reset(self):
        self.username = ""
        self._email = ""
        self.age = ""
        self._phone = ""
        self._license = ""
        self.location = ""
        return self

    def is_reset(self):
        return self.username == "" and self.email is None and self.age == "" and self.phone is None and self.license is None and self.location == ""

    def is_modified(self):
        return bool(self.username or self.email or self.age or self.phone or self.license or self.location)

    def is_pristine(self):
        return not self.is_modified()

    def is_dirty(self):
        return not self.is_pristine()

    def is_clean(self):
        return not self.is_dirty()

    def is_not_clean(self):
        return not self.is_clean()

    def is_not_dirty(self):
        return not self.is_dirty()

    def is_not_pristine(self):
        return not self.is_pristine()

    def is_not_modified(self):
        return not self.is_modified()

    def is_not_reset(self):
        return not self.is_reset()

    def is_not_cleared(self):
        return not self.is_cleared()

    def is_not_empty(self):
        return not self.is_empty()

    def is_not_valid(self):
        return not self.is_valid()


# Print every user in the given list
def print_all_users(users):
    for user in users:
        print(user)
        print(user.is_valid())


if __name__ == "__main__":
    alice = User("Alice", "alice@example.com", 30, "1234567890", "C123456", "New York")
    jose = User("Jose", "jose@example.com", 25, "0987654321", "Z789012", "Los Angeles")
    tony = User("Tony", "tony@example.com", 40, "1122334455", "N456789", "Chicago")
    donna = User("Donna", "donna@example.com", 35, "5566778899", "F321654", "San Francisco")
    kali = User("Kali", "kali@example.com", 28, "9988776655", "I654321", "Miami")
    kuti = User("Kuti", "kuti@example.com", 32, "4455667788", "L987654", "Seattle")

    users = [alice, jose, tony, donna, kali, kuti]
    print_all_users(users)

    # Formatted phone number (format_phone is an instance method)
    print(alice.format_phone(alice.phone))

    # Posts demo
    alice.create_post("Hello world!")
    alice.create_post("My second post")
    jose.create_post("Hi from Jose")

    print("\nAlice's posts:", alice.posts)
    print("Jose's posts:", jose.posts)
    print("All posts:", User.all_posts)

    # Bonus: delete a post, both lists stay in sync
    alice.delete_post(alice.posts[0])
    print("\nAfter deleting Alice's first post:")
    print("Alice's posts:", alice.posts)
    print("All posts:", User.all_posts)
    print("Jose can't delete Alice's post:", jose.delete_post(alice.posts[0]))

class Account:
  def __init__(self, username, easy, medium, hard) -> None:
    self.username = username
    self.easy = easy
    self.medium = medium
    self.hard = hard
    self.total = easy + medium + hard

  def to_dict(self):
    return {
      "username": self.username,
      "easy": self.easy,
      "medium": self.medium,
      "hard": self.hard,
      "total": self.total
    }

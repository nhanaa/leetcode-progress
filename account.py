class Account:
  def __init__(self, username, easy, medium, hard) -> None:
    self.username = username
    self.easy = easy
    self.medium = medium
    self.hard = hard
    self.total = easy + medium + hard

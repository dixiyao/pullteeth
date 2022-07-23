class ErrorClass():
  pass

class PlaneErorr(ErrorClass):
  def __init__(self):
    super().__init__()
  def __str__(self):
    return '具有颌骨模型时不需要从平面确定基准'
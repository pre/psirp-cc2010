from publishment import *

class BufferedPublishment(Publishment):
  
  MAX_BUFFER_LENGTH = 5000

  def __init__(self, content):
  	self.content = create(self.MAX_BUFFER_LENGTH)
  	self.content.buffer[:len(content)] = content
	
  def replace_content(self, new_content, offset=0):
    left_boundary = offset
    right_boundary = len(new_content)+offset
    self.content.buffer[left_boundary:right_boundary] = new_content
  
	
  


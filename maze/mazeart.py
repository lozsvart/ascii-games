from art import create, translate

def _split_text(text, max_width = 11):
    def split_paragraph(paragraph, max_width):
      words = paragraph.split()
      line_length = 0
      result = ""
      for word in words:
          if line_length > 0:
              line_length += 1 + len(word)
              if line_length > max_width:
                  line_length = len(word)
                  result += "\n" + word
              else:
                  result += " " + word
            
          else:
              result += word
              line_length += len(word)
      return result

    paragraphs = text.split("\n")
    return "\n".join(map(lambda paragraph: split_paragraph(paragraph, max_width), paragraphs))

def _get_writing_art(writing):
    lines = len(writing.split('\n'))
    return translate(create(writing), (6 - lines // 2, 1))

def writing(message):
  return _get_writing_art(_split_text(message))

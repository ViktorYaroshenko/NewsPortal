from django import template

register = template.Library()

bad_words = ['Хорватии', 'и']
znaki = ['.', ',', ';', ':', '!', '?', '(', ')', '"', "'"]

@register.filter()
def change(text):
   text = text.split()
   for i, word in enumerate(text):
      if word[-1] in znaki:
         _word = word[:-1]
         if _word in bad_words:
            text[i] = '***'
      else:
         if word in bad_words:
            text[i] = '***'
   return ' '.join(text)



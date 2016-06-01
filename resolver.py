# Lifted from https://github.com/sporto/rails_go_to_spec
import re

class Resolver:

  def run(self, file):
    if self.is_test(file):
      return self.get_source(file)
    else:
      return self.get_test(file)

  def is_test(self, file):
    return file.find('_test.rb') != -1

  def get_source(self, file):
    # find erb, haml
    match = re.search(r'(.erb|.haml|.slim)_test.rb$', file)
    related = []

    if match:
      ext = match.group(0)
      regex = re.escape(ext)
      ext = re.sub(r'_test.rb', '', ext)
      file = re.sub(regex, ext, file)
    else:
      # simply sub .rb to _spec.rb
      # e.g. foo.rb -> foo_spec.rb
      file = re.sub(r'\_test.rb$', '.rb', file)

    if file.find('/test/lib/') > -1:
      # file in lib
      related.append(re.sub(r'/test/lib/', '/lib/', file))
    else:
      related.append(re.sub(r'/test/', '/app/', file, 1))
      related.append(re.sub(r'/test/', '/', file, 1))

    return related


  def get_test(self, file):
    # find erb, haml
    match = re.search(r'erb$|haml$|slim$', file)
    related = []

    if match:
      ext = match.group(0)
      regex = re.escape(ext) + "$"
      file = re.sub(regex, ext + '_test.rb', file)
    else:
      file = re.sub(r'\.rb$', '_test.rb', file)

    if file.find('/lib/') > -1:
      related.append(re.sub(r'/lib/', '/test/lib/', file))
    elif file.find('/app/') > -1:
      related.append(re.sub(r'/app/', '/test/', file, 1))
    else:
      related.append('/test' + file)

    return related

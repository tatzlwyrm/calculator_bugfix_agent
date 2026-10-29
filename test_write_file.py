from functions.write_file import write_file
from functions.quoz import quoz

print(write_file("calculator", "quoz.txt", "What a day! What a lovely day!"))
print(write_file("calculator", "lorem.md", "wait, this isn't lorem ipsum"))
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
#print(write_file("/", "jaws.md", "PAGE 1: Sunset over the ocean"))

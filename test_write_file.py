from functions.write_file import write_file

work_dir = 'calculator'
fileContent = {
  "lorem.txt": "wait, this isn't lorem ipsum",
  "pkg/morelorem.txt": "lorem ipsum dolor sit amet",
  "/tmp/temp.txt": "this should not be allowed"
}

for file in fileContent.keys():
  print(f'{write_file(work_dir, file, fileContent[file])}')
  

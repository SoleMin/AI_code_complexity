import javalang


source_file='data/CodeDataset/1.java'
f = open(source_file)
source = f.read()
f.close()

tree = javalang.parse.parse(source)
# tree.parse_type_declaration()
for path,node in tree:
    print()
    # print(path)
    print(node)
import javalang

def state_counter(typelist):
    num_state = 0
    num_state+=typelist.count(javalang.tree.IfStatement)
    num_state+=typelist.count(javalang.tree.WhileStatement)
    num_state+=typelist.count(javalang.tree.DoStatement)
    num_state+=typelist.count(javalang.tree.ForStatement)
    num_state+=typelist.count(javalang.tree.AssertStatement)
    num_state+=typelist.count(javalang.tree.BreakStatement)
    num_state+=typelist.count(javalang.tree.ContinueStatement)
    num_state+=typelist.count(javalang.tree.ReturnStatement)
    num_state+=typelist.count(javalang.tree.ThrowStatement)
    num_state+=typelist.count(javalang.tree.SynchronizedStatement)
    num_state+=typelist.count(javalang.tree.TryStatement)
    num_state+=typelist.count(javalang.tree.SwitchStatement)
    num_state += typelist.count(javalang.tree.BlockStatement)

    return num_state
def feature_Extractor(source_file):
    PATH='data/CodeDataset/'
    f = open(PATH+source_file)
    source = f.read()
    f.close()
    typelist=[]
    # print(source_file)
    tree = javalang.parse.parse(source)
    num_sort=0
    num_hash_map=0
    num_hash_set=0
    num_Priority=0
    num_nasted_loop=0
    num_recursive=0
    for path,node in tree:
        # print(node)
        if type(node)==javalang.tree.MethodDeclaration:
            temp_name=node.name
            if node.name in str(node).replace('name='+temp_name,''):
                num_recursive+=1
            # print(node.name)
        typelist.append(type(node))
        if type(node)==javalang.tree.ForStatement:
            if str(node).count('ForStatement') != 1 and str(node).count('ForStatement')>num_nasted_loop:
                num_nasted_loop=str(node).count('ForStatement')
        if type(node)==javalang.tree.LocalVariableDeclaration:
            try:
                if node.declarators[0].initializer.type.name == 'HashMap':
                    num_hash_map += 1
                elif node.declarators[0].initializer.type.name == 'HashSet':
                    num_hash_set += 1
                elif node.declarators[0].initializer.type.name == 'PriorityQueue':
                    num_Priority += 1
            except:
                pass

        if type(node) ==javalang.tree.MethodInvocation:
            if node.member =='sort':
                num_sort+=1

    num_if = typelist.count(javalang.tree.IfStatement)
    num_loof = typelist.count(javalang.tree.ForStatement) +typelist.count(javalang.tree.WhileStatement)
    num_vari = typelist.count(javalang.tree.VariableDeclaration)+typelist.count(javalang.tree.LocalVariableDeclaration)
    num_state = state_counter(typelist)
    num_break = typelist.count(javalang.tree.BreakStatement)
    num_method =typelist.count(javalang.tree.MethodDeclaration)
    num_switch =typelist.count(javalang.tree.SwitchStatement)


    return [num_if,num_switch,num_loof,num_break,num_Priority,num_sort,num_hash_map,num_hash_set,num_recursive,num_nasted_loop,num_vari,num_method,num_state]

feature_Extractor('140.java')
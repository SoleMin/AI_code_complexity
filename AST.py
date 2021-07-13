import javalang
import pandas as pd
import numpy as np
import inspect

def state_counter(typelist):
    num_state = 0
    num_state += typelist.count(javalang.tree.IfStatement)
    num_state += typelist.count(javalang.tree.WhileStatement)
    num_state += typelist.count(javalang.tree.DoStatement)
    num_state += typelist.count(javalang.tree.ForStatement)
    num_state += typelist.count(javalang.tree.AssertStatement)
    num_state += typelist.count(javalang.tree.BreakStatement)
    num_state += typelist.count(javalang.tree.ContinueStatement)
    num_state += typelist.count(javalang.tree.ReturnStatement)
    num_state += typelist.count(javalang.tree.ThrowStatement)
    num_state += typelist.count(javalang.tree.SynchronizedStatement)
    num_state += typelist.count(javalang.tree.TryStatement)
    num_state += typelist.count(javalang.tree.SwitchStatement)
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
        print(node)
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

def get_graph(source_file):

    f = open(source_file)
    source = f.read()
    f.close()

    print(source_file)

    tree = javalang.parse.parse(source)
    graph_list=[]

    features=_dict={}
    node_dict={}
    value_dict={}
    root=tree.__iter__().__next__()[1]
    # print(root)
    # print(tree.__iter__().__next__()[1])
    for i,(path,node) in enumerate(tree):
        node_dict[node]=i
    s_num = i
    temp_index = 0
    features_dict = {}
    for name, obj in inspect.getmembers(javalang.tree):
        if inspect.isclass(obj):
            features_dict[obj] = temp_index
            temp_index += 1

    features_dict['normal'] = str(temp_index + 1)

    inv_map = {v: k for k, v in node_dict.items()}
    for i in range(len(inv_map)):
        value_dict[str(i)]=str(features_dict[type(inv_map[i])])


    # for path, node in tree:
    #
    #     if type(node)==javalang.tree.SwitchStatement:
    #         print(node.control)
    #         print(type(node),node.attrs)

    # graph_list.append()
    # print(node_dict)
    # print()
    graph_list,value_dict,_=visit(root,graph_list,node_dict,s_num,value_dict,features_dict)
    # print(graph_list)
    # print(value_dict)
    return {'edges':graph_list,'features':value_dict}
    # print(graph_list)
def visit(node,graph_list,node_dict,s_num,value_dict,features_dict):

    if node != None and type(node) != str and type(node) != bool and type(node) != set :
        attr_list = node.attrs

        for i in attr_list:
            # print(type(getattr(node, i)))
            # print(getattr(node, i),i)

            if type(getattr(node, i)) == list:
                graph_list,value_dict, s_num = visit_list(node, graph_list, node_dict, s_num, getattr(node, i),value_dict,features_dict)

            else:
                # print(node)
                if (getattr(node, i) != None) and type(getattr(node, i)) != set:
                    if node_dict.get(getattr(node, i)) == None:
                        graph_list.append((node_dict.get(node), s_num))
                        value_dict[str(s_num)]=features_dict['normal']
                        s_num += 1
                    else:
                        graph_list.append((node_dict.get(node),node_dict.get(getattr(node, i))))
                        graph_list,value_dict , s_num = visit(getattr(node, i),graph_list,node_dict,s_num,value_dict,features_dict)

    return graph_list,value_dict,s_num

def visit_list(node,graph_list,node_dict,s_num,item_list,value_dict,features_dict):

    for item in item_list:
        if type(item) == list:
            graph_list,value_dict,s_num=visit_list(node,graph_list,node_dict,s_num,item,value_dict,features_dict)

        elif (item != None):
            if node_dict.get(item) == None:
                graph_list.append((node_dict.get(node), s_num))
                value_dict[str(s_num)] = features_dict['normal']
                s_num += 1

            else:
                graph_list.append((node_dict.get(node), node_dict.get(item)))
                graph_list,value_dict,s_num=visit(item, graph_list, node_dict, s_num,value_dict,features_dict)

    return graph_list,value_dict,s_num

def analysis(source_file):
    PATH = 'data/CodeDataset/'
    f = open(PATH + source_file)
    source = f.read()
    f.close()
    tree = javalang.parse.parse(source)

    for path, node in tree:
        if type(node)==javalang.tree.SwitchStatement:
            # print(node)
            # print(len(node.statements))
            for i in node.attrs:
                print(i)
            for i in node.attrs:
                print(i,": ",getattr(node,i))
            print()
            # print(node.type)
            # print(len(node.declarators)
            # print(node.modifiers)
            # print(node.annotations)

get_graph('data/CodeDataset/'+'54.java')
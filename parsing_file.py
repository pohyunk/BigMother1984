def_list = {}
valid = []  # 0:invalid, 1:valid, 2:ignored(invalid after valid)

def is_defined(name, val):
    print(f"(is_defined) name:{name} val:{val} {def_list}")
    #print("!!!!!", name in def_list.keys())
    if (name in def_list):
        if (str(def_list[name]) == val):
            print("!!!",def_list[name], val)
            return True
        else:
            print("???",def_list[name], val)            
            return False
    else:
        return False

def print_def_list():
    # check all define...
    for key in def_list:
        print(key, def_list[key])

def process_define():
    if("#define" in line):
        token = line.split()
        if (len(token) == 2):
            #print("(process_define)"+token[1])
            def_list[token[1]] = 1
        if (len(token) > 2):
            if (token[2] != '0'):
                #print("(process_define)"+token[1], token[2])
                if (token[2].isnumeric()):
                    def_list[token[1]] = int(token[2])
                else:
                    def_list[token[1]] = token[2]

def process_line():
    global depth
    global valid

    if('#ifdef ' in line):    #ifdef XXX
        token = line.split()
        print("[ifdef] " + token[1])
        if(is_defined(str(token[1]), '1')):
            valid.append(1)
        else:
            valid.append(0)
        
        print(len(valid), valid)
  
    elif('#ifndef ' in line):    #ifdef XXX
        token = line.split()
        print("[ifndef] " + token[1])
        if(is_defined(str(token[1]), '0')):
            valid.append(1)
        else:
            valid.append(0)
        
        print(len(valid), valid)

    elif("#if defined" in line):    #if defined
        token = line.split('(')
        define = token[1].split(')')
        print("[if defined] " + define[0])
        if(is_defined(str(token[1]), '1')):
            valid.append(1)
        else:
            valid.append(0)
        
        print(len(valid), valid)


    elif('#if ' in line):    #if (XXX == VAL)
        token = line.split('(')
        print("++++++", line)
        print(f">>>>{token[0]}>>>{token[1]}")
        define = str(token[1]).split('==')
        value = str(define[1]).split(')')
        print(f">>>>{define[0]}>>>{value[0]}")
        if is_defined(str(define[0]).strip(), str(value[0]).strip()):
            valid.append(1)
        else:
            valid.append(0)
        
        print(len(valid), valid)

        print("[if] " + define[0] + ":" + value[0])

    elif('#else if (' in line) or ('#elif (' in line):
        token = line.split('(')
        define = str(token[1]).split('==')
        value = str(define[1]).split(')')
        print(f">>>>{define[0]}>>>{value[0]}")
        if (valid[len(valid)-1] == 0):
            if is_defined(str(define[0]).strip(), str(value[0]).strip()):
                valid[len(valid)-1] = 1
            else:
                valid[len(valid)-1] = 0
        else:   # valid:1 or 2
            valid[len(valid)-1] = 2
        
        print(len(valid), valid)

        print("[if] " + define[0] + ":" + value[0])

    elif('#else' in line):    #else
        print("[else]")
        if (valid[len(valid)-1] == 1):
            valid[len(valid)-1] = 0
        elif (valid[len(valid)-1] == 2):
            valid[len(valid)-1] = 0
        else:
            valid[len(valid)-1] = 1
        print(len(valid), valid)

    elif('#endif' in line):    #endif
        del valid[len(valid)-1]
        print("[endif]")
        print(len(valid), valid)

    if len(valid) > 0:
        if valid[len(valid)-1] != 1:
            #print("zzz")
            return

    process_define()





r = open('prj_conf.h', mode='rt', encoding='utf-8')
#r.readline()

for line in r:
    #print(line)
    process_line()

print_def_list()
#print(def_list)

r.close()

objects={}

def get_object(key):
  return objects[key]
  
def set_object(key,value):
  global objects
  objects[key]=value
  
def read_objects(file_name):
    f=open(file_name,'r')
    lines=f.readlines()
    f.close()
    dic={}
    for line in lines:
        if line.startswith('==='):
            continue
        temp=line[:-1].split('::')
        key=temp[1]
        value_type=temp[0]
        values=temp[2].split(' ')
        if len(values)==0:
            dic[key]=None
        elif len(values)==1:
            if value_type=='str':
                dic[key]=values[0]
            elif value_type=='int':
                dic[key]=int(values[0])
            elif value_type=='float':
                dic[key]=float(values[0])
            else:
                dic[key]=None
        else:
            if value_type=='str':
                dic[key]=values
            elif value_type=='int':
                for value in values:
                    dic[key].append(int(value))
            elif value_type=='float':
                for value in values:
                    dic[key].append(float(value))
            else:
                dic[key]=None
    global objects
    objects=dic
    
 read_objects('data/objects.nomi')

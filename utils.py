import os,emoji,random
from discord import opus

variables={}

def init_opus_lib():
    if opus.is_loaded():
        return
    opus_libs=['libopus-0.x86.dll','libopus-0.x64.dll','libopus-0.dll','libopus.so.0','libopus.0.dylib']
    for lib in opus_libs:
        if opus.is_loaded():
            print(lib)
            return
        try:
            opus.load_opus(lib)
            continue
        except Exception as e:
			print(e)
            pass

def read_variables(file_name):
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
    global variables
    variables=dic

def get_variables(key):
    global variables
    return variables[key]

def set_variables(key,value):
    global variables
    variables[key]=value
    
def to_emoji(text):
    return emoji.emojize(text,use_aliases=True)

def to_raw_text(emoji_text):
    return emoji.demojize(emoji_text)
    
def random_bright_color():
    global variables
    return int(random.choice(variables['bright_colors']),16)

def to_time_format(seconds):
    m,s=divmod(seconds,60)
    h,m=divmod(m, 60)
    res='{:d}:{:02d}:{:02d}'.format(h,m,s)
    if h==0:
        res='{:02d}:{:02d}'.format(m,s)
    return res

init_opus_lib()
read_variables('data/variables.nomi')
variables['token']=os.getenv('token')

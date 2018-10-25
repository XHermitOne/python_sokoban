import os, os.path

for i in range(51, 86):
    file_name='%04u.map'%(i)
    if os.path.isfile('tmp.map'):
        os.remove('tmp.map')
    os.rename(file_name, 'tmp.map')
    src=open('tmp.map', 'rt')
    lines=src.readlines()
    dst=open(file_name, 'w')
    new_lines=[]
    for line in lines:
        new_line=line.rstrip()
        if new_line:
            new_line=new_line.replace(',', '')
            new_line=new_line.replace('"', '')
            new_line=new_line.replace('$', 'O')
            new_line=new_line.replace('.', '*')
            new_line=new_line.replace('"', '')
            new_line=new_line[:new_line.find('#')]+\
                new_line[new_line.find('#'):].replace(' ', '.')
            print(new_line)
            new_lines.append(new_line+'\n')
    dst.writelines(new_lines)
    print() 
    dst.close
    src.close()
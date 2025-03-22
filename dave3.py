import ollama
import random
import time


def generate_function(object_repr, action,output):
    python_code_string = f"Create a Python class named 'tomfun' that takes Python object(s) represented as {object_repr} as __init__ data and has functions to perform the actions: {action}. The class must have functions to return the Python object(s) represented as {output} as a return. write all code in one chunk."
    results =  ollama.generate(model = 'tomchat-coder4', prompt=python_code_string,stream = False)
    tmp_code = results['response']
    tmp_code = str(tmp_code)
    #print(tmp_code)
    if tmp_code.find('```python'):
        tmp_code = tmp_code[tmp_code.find('```python')+9:]
    #print('strip top   ',tmp_code)
    if tmp_code.find('```python'):
        tmp_code = tmp_code[:tmp_code.find('```python')]
    #print('strip senond top   ',tmp_code)
    if tmp_code.find('````'):
        tmp_code = tmp_code[:tmp_code.find('````')]
    #print('strip four   ',tmp_code)
    if tmp_code.find('```'):
        tmp_code = tmp_code[:tmp_code.find('```')]
    #print('strip three   ',tmp_code)
    return tmp_code



def fix_function(object_repr, action,function):
    python_code_string = f"Check for errors and fix if nessisary the Python class tomfun {function} that takes a Python objects represented as {object_repr} and performs the actions: {action}. The new class must have returns for these Python objects represented as {output} as a return.check that all parentheses, brackets and braces are closed"
    results =  ollama.generate(model = 'tomchat-coder4', prompt=python_code_string,stream = False)
    tmp_code = results['response']
    tmp_code = str(tmp_code)
    if tmp_code.find('```python'):
        tmp_code = tmp_code[tmp_code.find('```python')+9:]
    #print('strip top   ',tmp_code)
    if tmp_code.find('```python'):
        tmp_code = tmp_code[:tmp_code.find('```python')]
    #print('strip senond top   ',tmp_code)
    if tmp_code.find('````'):
        tmp_code = tmp_code[:tmp_code.find('````')]
    #print('strip four   ',tmp_code)
    if tmp_code.find('```'):
        tmp_code = tmp_code[:tmp_code.find('```')]
    #print('strip three   ',tmp_code)
    return tmp_code
    
def fix_prompt_action(object_repr, action,function):
    python_code_string = f"White a new action prompt to produce aa Python class tomfun {function} that takes a Python objects represented as {object_repr} and performs the old actions: {action}. The new class must have returns for these Python objects represented as {output} as a return."
    results =  ollama.generate(model = 'tomchat-relax', prompt=python_code_string,stream = False)
    prompt = results['response']
    prompt = str(prompt)
    return prompt

    
def remove_comments(code_string):
    try:
        lines = code_string.splitlines()
        cleaned_lines = []
        in_multiline_string = False
        multiline_quote_type = None
        for line in lines:
            original_line = line  # Store the original line for indentation
            line = line.lstrip()  # Remove leading whitespace *only for comment detection*
            if not in_multiline_string:
                if line.startswith('"""') or line.startswith("'''"):
                    in_multiline_string = True
                    multiline_quote_type = line[:3]
                     #Check if the multiline string is closed on the same line
                    if line.count(multiline_quote_type) >=2 and line.find(multiline_quote_type,3) != -1: #Find the second instance of the quote type
                        in_multiline_string = False
                        multiline_quote_type = None
                        cleaned_lines.append("") #Add empty line for the docstring
                    continue #Skip the rest of the current line.
                elif '#' in line:
                    line = line[:line.find('#')]  # Remove comment part
            else:
                if line.endswith(multiline_quote_type) or line.count(multiline_quote_type) >=2 and line.find(multiline_quote_type,3) != -1:
                    in_multiline_string = False
                    multiline_quote_type = None
                    continue #Skip the line containing the closing quotes
            if not in_multiline_string: #Only append if not in multiline string
                cleaned_lines.append(original_line[:original_line.find(line)] + line) #Preserve indentation by adding back the original indentation
        return "\n".join(cleaned_lines)
    except Exception as e:
        print(f"An error occurred: {e}")
        return code_string

def remove_empty_lines(code):
    lines = code.split('\n')
    return '\n'.join([line for line in lines if line.strip() != ''])


object_repr = "a list of integers or a list floating point numbers"
action = "calculate the sum,avarage,min and max of the list"
output = "an integer in integer input. a floating point if floating point input"
#test_function(object_repr, action,output,[1, 2, 3, 4, 5,5,4,3,2,1])

generated_function_code = generate_function(object_repr, action,output)
print(generated_function_code)
#generated_function_code = fix_function(object_repr, action,generated_function_code)
#print(generated_function_code)
generated_function_code = remove_comments(generated_function_code)
generated_function_code = remove_empty_lines(generated_function_code)
try:
    exec(generated_function_code)
except:
    gfc = generate_function(object_repr, action,output)
    gfc = remove_comments(gfc)
    gfc = remove_empty_lines(gfc)
    print('try number two : ',gfc)
    try:
        exec(gfc)
    except:
        gfc = fix_function(object_repr, action,generated_function_code)
        gfc = remove_comments(gfc)
        gfc = remove_empty_lines(gfc)
        print('repare number one : ',gfc)
        exec(gfc)
        

result = tomfun([1, 2, 3, 4, 5,5,4,3,2,1])
print('In:',[1, 2, 3, 4, 5,5,4,3,2,1]," Result:", result)
print()
    
object_repr = "integer number"
action = "check if a number its square and its cube is prime."
output = "bool,bool.bool"
#test_function(object_repr, action,output,17)
generated_function_code = generate_function(object_repr, action,output)
generated_function_code = remove_comments(generated_function_code)
generated_function_code = remove_empty_lines(generated_function_code)
print(generated_function_code)
try:
    exec(generated_function_code)
except:
    try:
        gfc = generate_function(object_repr, action,output)
        gfc = remove_comments(gfc)
        gfc = remove_empty_lines(gfc)
        print('try number 2',gfc)
        exec(gfc)
    except:
        tomfun = print

try:
    result = tomfun(17)  
    print('In:',17," Result:", result)
except:
    print('result fail')
print()

object_repr = "integer number"
action = "calculate the factorial of a number."
output = "integer number"
#test_function(object_repr, action,output,12)
generated_function_code = generate_function(object_repr, action,output)
generated_function_code = remove_comments(generated_function_code)
generated_function_code = remove_empty_lines(generated_function_code)
print(generated_function_code)
try:
    exec(generated_function_code)
except:
    gfc = generate_function(object_repr, action,output)
    gfc = remove_comments(gfc)
    gfc = remove_empty_lines(gfc)
    print('try number two : ',gfc)
    try:
        exec(gfc)
    except:
        gfc = fix_function(object_repr, action,gfc)
        gfc = remove_comments(gfc)
        gfc = remove_empty_lines(gfc)
        print('repare number one : ',gfc)
        try:
            exec(gfc)
        except:
            gfc = generate_function(object_repr, action,output)
            gfc = remove_comments(gfc)
            gfc = remove_empty_lines(gfc)
            print('try number three : ',gfc)
            try:
                exec(gfc)
            except:
                action =fix_prompt_action(object_repr, action,gfc) 
                gfc = generate_function(object_repr, action,output)
                gfc = remove_comments(gfc)
                gfc = remove_empty_lines(gfc)
                print('actin fix : ',gfc)
                try:
                    exec(gfc)
                except:
                    tomfun = Print

try:
    result = tomfun(7)  
    print('In:',7," Result:", result)
except:
    print('result fail')
print()   

object_repr = "password"
action = "generate random passwords and a parword entry dialog for inputed password"
output = "string"
#test_function(object_repr, action,output,'')
#test_function(object_repr, action,output,'')
generated_function_code = generate_function(object_repr, action,output)
#generated_function_code = fix_function(object_repr, action,generated_function_code)
generated_function_code = remove_comments(generated_function_code)
generated_function_code = remove_empty_lines(generated_function_code)
print(generated_function_code)
try:
    exec(generated_function_code)
except:
    gfc = generate_function(object_repr, action,output)
    gfc = remove_comments(gfc)
    gfc = remove_empty_lines(gfc)
    print('try number two : ',gfc)
    try:
        exec(gfc)
    except:
        gfc = fix_function(object_repr, action,generated_function_code)
        gfc = remove_comments(gfc)
        gfc = remove_empty_lines(gfc)
        print('repare number one : ',gfc)
        exec(gfc)
 
try:   
    result = tomfun('tyicjfd')  
    print('In:',''," Result:", result)
except:
    print('result fail')
print()

object_repr = "input,output node numbers"
action = "write a simple neural network imputed input and output node numbers. using only the python random and numpy modules."
output = "a class object with a .train method and a .test metod"
generated_function_code = generate_function(object_repr, action,output)
#generated_function_code = fix_function(object_repr, action,generated_function_code)
generated_function_code = remove_comments(generated_function_code)
generated_function_code = remove_empty_lines(generated_function_code)
print(generated_function_code)
try:
    exec(generated_function_code)
except:
    gfc = generate_function(object_repr, action,output)
    gfc = remove_comments(gfc)
    gfc = remove_empty_lines(gfc)
    print('try number two : ',gfc)
    try:
        exec(gfc)
    except:
        gfc = fix_function(object_repr, action,generated_function_code)
        gfc = remove_comments(gfc)
        gfc = remove_empty_lines(gfc)
        print('repare number one : ',gfc)
        exec(gfc) 
try:   
    result = tomfun(5,2)  
    print('In:',5,2," Result:", result)
except:
    gfc = generate_function(object_repr, action,output)
    gfc = remove_comments(gfc)
    gfc = remove_empty_lines(gfc)
    print('try number two : ',gfc)
    try:
        exec(gfc)
    except:
        gfc = fix_function(object_repr, action,generated_function_code)
        gfc = remove_comments(gfc)
        gfc = remove_empty_lines(gfc)
        print('repare number one : ',gfc)
        try:
            exec(gfc) 
        except:
            print('result fail')

print()

object_repr = "The location of an jpg"
action = "open and resize the image to (600,600) then save as {image_name_resize.jpg}, return True on sucess."
output = "bool"
#test_function(object_repr, action,output,'/home/ttombbab/Downloads/Download/3.jpg')
generated_function_code = generate_function(object_repr, action,output)
generated_function_code = remove_comments(generated_function_code)
generated_function_code = remove_empty_lines(generated_function_code)
print(generated_function_code)
#generated_function_code = fix_function(object_repr, action,generated_function_code)
#print('fix ::::::::::',generated_function_code)

try:
    exec(generated_function_code)
except:
    gfc = generate_function(object_repr, action,output)
    gfc = remove_comments(gfc)
    gfc = remove_empty_lines(gfc)
    print('try number two : ',gfc)
    try:
        exec(gfc)
    except:
        gfc = fix_function(object_repr, action,generated_function_code)
        gfc = remove_comments(gfc)
        gfc = remove_empty_lines(gfc)
        print('repare number one : ',gfc)
        exec(gfc)
try:
    result = tomfun('/home/ttombbab/Downloads/Download/3.jpg')  
    print("Result:", result)
except:
    print('result fail')

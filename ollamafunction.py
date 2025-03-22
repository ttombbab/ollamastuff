import ollama
import random
import time

url = 'http://localhost:11434/api/generate'
python_commands = [ "generate random musical output using the mmusic scale c,c#,d,d#,e,f,f#,g,g#,a,a#,b an S for silence and the minus sign to denote length of notes.",
    "find the common elements in two lists?","check if a number is prime.","find the maximum of two numbers?","convert Celsius to Fahrenheit.",
    "calculate the factorial of a number.","reverse a string.","calculate the average of a list of numbers.",
    "generate a random password?",'make a simple neural network',
    "get the integer from between '<|Z' and 'Z|' from a block of text"]
    
#python_command = random.choice(python_commands)
#python_commands = ["generate random musical output using the mmusic scale c,c#,d,d#,e,f,f#,g,g#,a,a#,b an S for silence and the minus sign to denote length of notes.",]
#python_command = "get the integer from between '<|Z' and 'Z|' from a block of text"
#seeds = [random.randint(32767,1048576) for i in range(5)]
#'make a simple neural network',
seed = random.randint(32767,1048576)

def extract_integer_from_tag(textt):
    textt = textt[textt.find('<|Z')+2:textt.rfind('Z|>')]
    try:
        return int(textt)
    except:
        return 0

def get_code(python_command,seed):
    false = "Write a Python function to " +  python_command + " The Python output should be entirly between the tags ```python and ```. The Python code must be able to be passed to the exec() funcion without error." 
    results =  ollama.generate(model = 'tomchat-coder4', prompt=false,stream = False)
    try:
        #print(results.keys())
        sample_text = results['response']
    except:
        sample_text = results
    example_text = sample_text
    return example_text
    
def fix_code(python_code):
    python_code_string='rewrite the code and fix any problems, ' +  python_code + ' for the prompt,'+ python_command+' The Python output should be entirly between the tags ```python and ```. The Python code must be able to be passed to the exec() funcion without error.'
    #print(python_code_string)
    results =  ollama.generate(model = 'tomchat-coder4', prompt=python_code_string,stream = False)
    #print(results)
    sample_text = results['response']
    example_text = sample_text
    return example_text   
    
def rate_code(python_scripts):
    data = '{"model":"tomchat-coder4","prompt":"from these five Python scripts' +  python_scripts + ' for the prompt,'+ python_command+' Which one is the best. Pick only one. Output must contain the winning number in the form ### winning_list_index_number","stream":false}'
    print('data: ',data)
    results =  ollama.generate(model = 'tomchat-coder4', prompt=data,stream = False)
    sample_text = results['response']
    example_text = sample_text
    return example_text   

#print(get_code(python_command,i))
codes = {}
code_store = {}
for python_command in python_commands:
	print('code seed start:',seed)
	t = time.time()
	tmp_code = get_code(python_command,seed)
	#print('code seed:',i,' tmp_code:',tmp_code)
	tmp_code = str(tmp_code)
	if tmp_code.find('```python'):
		tmp_code = tmp_code[tmp_code.find('```python')+9:]
		if tmp_code.find('```'):
			tmp_code = tmp_code[:tmp_code.find('```')]

	fix = fix_code(tmp_code)
	if fix.find('```python'):
		fix = fix[fix.find('```python')+9:]
		if fix.find('```'):
			fix = fix[:fix.find('```')]
	codes[seed] = fix
	print('code seed:',seed,", Time:",time.time()-t,' Fix code:',tmp_code)
	

    #key_list = []
    #val_list = []
    #print(codes)
    #for k in codes.keys():
	#    key_list.append(k)
	#    val_list.append(codes[k])
	    
    #newval = ''
    #for count,l in enumerate(val_list):
    #    newval= newval + str(count+1) + '.:' + l + '  '
    #example_text = rate_code(str(newval))
    #example_text = ''

    #print('best in show:',example_text)
    #print('code: ',val_list[extract_integer_from_tag(example_text)])
    #code_store[python_command] = key_list[extract_integer_from_tag(example_text)]
    
print(code_store)

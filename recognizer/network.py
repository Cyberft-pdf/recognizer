import subprocess
import platform


command = "'color 2 & ipconfig /all" 
command = f'color 2 & {command}'

subprocess.Popen(["start", "cmd", "/k", command], shell=True)



try:
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    output = result.stdout
    error = result.stderr
    
    print("Výstup z příkazu:")
    print(output)
    
    if error:
        print("Chyba:")
        print(error)
except subprocess.CalledProcessError as e:
    print(f"Chyba při spuštění příkazu: {e}")
import pymem
import keyboard


toggle_f1 = False
toggle_f2 = False
original_bytes_f1 = None
original_bytes_f2 = None


def find_pattern(process_name, pattern):
    pm = pymem.Pymem(process_name)
    module = pymem.process.module_from_name(pm.process_handle, "GameAssembly.dll") 
    module_base = module.lpBaseOfDll
    module_end = module_base + module.SizeOfImage
    buffer = pm.read_bytes(module_base, module.SizeOfImage)
    
    for i in range(len(buffer) - len(pattern)):
        if all(buffer[i+j] == pattern[j] for j in range(len(pattern))):
            return module_base + i
    return None


def replace_pattern(process_name, pattern_to_replace, new_pattern):
    try:
        address = find_pattern(process_name, pattern_to_replace)
        if address:
            pm = pymem.Pymem(process_name)
            original = pm.read_bytes(address, len(new_pattern))
            pm.write_bytes(address, new_pattern, len(new_pattern))
            print("Pattern replaced at address:", hex(address))
            return original 
        else:
            print("Pattern not found.")
            return None
    except pymem.exception.ProcessNotFound:
        print("Process not found.")
        return None


def toggle_replacement_f1():
    global toggle_f1
    global original_bytes_f1
    toggle_f1 = not toggle_f1  

    if toggle_f1:
        print("Replacement for F1 activated.")
        original_bytes_f1 = replace_pattern(process_name, pattern_to_replace_f1, new_pattern_f1)
    else:
        if original_bytes_f1:
            print("Returning F1 to original bytes.")
            pm = pymem.Pymem(process_name)
            address = find_pattern(process_name, new_pattern_f1)
            if address:
                pm.write_bytes(address, original_bytes_f1, len(original_bytes_f1))
            else:
                print("Pattern not found.")
        else:
            print("No original bytes stored for F1.")


def toggle_replacement_f2():
    global toggle_f2
    global original_bytes_f2
    toggle_f2 = not toggle_f2  # Toggle the state

    if toggle_f2:
        print("Replacement for F2 activated.")
        original_bytes_f2 = replace_pattern(process_name, pattern_to_replace_f2, new_pattern_f2)
    else:
        if original_bytes_f2:
            print("Returning F2 to original bytes.")
            pm = pymem.Pymem(process_name)
            address = find_pattern(process_name, new_pattern_f2)
            if address:
                pm.write_bytes(address, original_bytes_f2, len(original_bytes_f2))
            else:
                print("Pattern not found.")
        else:
            print("No original bytes stored for F2.")



process_name = "BleachBraveSouls.exe"


pattern_to_replace_f1 = b'\x2B\x50\x10\xE8\x1B\xE4\xF5\xFF'
new_pattern_f1 = b'\x90\x90\x90\xE8\x1B\xE4\xF5\xFF'

pattern_to_replace_f2 = b'\x0F\x8E\x46\x02\x00\x00\x84'
new_pattern_f2 =  b'\x0F\x8D\x46\x02\x00\x00'


keyboard.add_hotkey('f1', toggle_replacement_f1)
keyboard.add_hotkey('f2', toggle_replacement_f2)


print("Press F1 to toggle replacement for the first pattern.")
print("Press F2 to toggle replacement for the second pattern.")


keyboard.wait('esc')



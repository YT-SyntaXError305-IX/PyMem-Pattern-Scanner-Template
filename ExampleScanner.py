import pymem
import keyboard

# Global variables to keep track of toggle states and original bytes replaced
toggle_f1 = False
toggle_f2 = False
original_bytes_f1 = None
original_bytes_f2 = None

# Function to find a specific pattern in the target process's memory
def find_pattern(process_name, pattern):
    pm = pymem.Pymem(process_name)
    module = pymem.process.module_from_name(pm.process_handle, "Barony.exe")  # Target Module could be a DLL, such as GameAssembly.dll, to search for AOB bytes.
    module_base = module.lpBaseOfDll
    module_end = module_base + module.SizeOfImage
    buffer = pm.read_bytes(module_base, module.SizeOfImage)
    
    for i in range(len(buffer) - len(pattern)):
        if all(buffer[i+j] == pattern[j] for j in range(len(pattern))):
            return module_base + i
    return None

# Function to replace a specific pattern with a new pattern in the target process's memory
def replace_pattern(process_name, pattern_to_replace, new_pattern):
    try:
        address = find_pattern(process_name, pattern_to_replace)
        if address:
            pm = pymem.Pymem(process_name)
            original = pm.read_bytes(address, len(new_pattern))
            pm.write_bytes(address, new_pattern, len(new_pattern))  # Write the new pattern to memory
            print("Pattern replaced at address:", hex(address))
            return original  # Return the original bytes so they can be restored later if needed
        else:
            print("Pattern not found.")
            return None
    except pymem.exception.ProcessNotFound:
        print("Process not found.")
        return None

# Function to toggle replacement for the first pattern (bound to F1 key)
def toggle_replacement_f1():
    global toggle_f1
    global original_bytes_f1
    toggle_f1 = not toggle_f1  # Toggle the state

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

# Function to toggle replacement for the second pattern (bound to F2 key)
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


# Target process name
process_name = "Barony.exe" 

# Patterns and replacements for F1 and F2
pattern_to_replace_f1 = b'\xC7\x86\x70\x02\x00\x00\x08\x00\x00\x00'
new_pattern_f1 = b'\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'

pattern_to_replace_f2 = b'\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90'
new_pattern_f2 =  b'\xC7\x86\x70\x02\x00\x00\x08\x00\x00\x00'

# Registering hotkeys for F1 and F2 to toggle replacements
keyboard.add_hotkey('f1', toggle_replacement_f1)
keyboard.add_hotkey('f2', toggle_replacement_f2)

# Instructions for the user
print("Press F1 to toggle replacement for the first pattern.")
print("Press F2 to toggle replacement for the second pattern.")

# Waiting for user to press Esc to exit (optional)
keyboard.wait('esc')

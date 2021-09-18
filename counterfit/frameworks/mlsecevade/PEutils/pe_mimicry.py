import json
from pathlib import Path
import numpy as np
import gzip
import pickle
import itertools
import os
from collections import defaultdict
import random
import lief
import json
import heapq
from .pe_modify import PEFileModifier
from .strontic_allowed_kernel32_functions import ALLOWED_FUNCTIONS
from ember import PEFeatureExtractor

MiB = 1048576 

with gzip.open('counterfit/frameworks/mlsecevade/PEutils/file_data.pkl.gz', 'rb') as infile:
    FILE_DATA = pickle.load(infile)

with gzip.open('counterfit/frameworks/mlsecevade/PEutils/file_size.pkl.gz', 'rb') as infile:
    FILE_SIZE = pickle.load(infile)
    
SUCCESSFUL_BENIGNS = {#'/media/kevin/A536-D98F/ben_program_files/LHService.exe',
#'/media/kevin/A536-D98F/ben_program_files/DeleteMonitorDll.exe',
#'/media/kevin/A536-D98F/benign_files_win10/winbiodatamodeloobe.exe',
#'/media/kevin/A536-D98F/benign_files_win10/openwith.exe',
#'/media/kevin/A536-D98F/benign_files_win10/PresentationHost.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//wmpshare.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//unins000.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//zotero.exe',
#'/media/kevin/A536-D98F/ben_program_files/LHService.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//FullTrustNotifier.exe',
#'/media/kevin/A536-D98F/ben_program_files/miktex-mkocp.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//x64launcher.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//x86launcher.exe',
#'/media/kevin/A536-D98F/ben_program_files/LHService.exe',
'/media/kevin/A536-D98F/ben_program_files/WINWORD.EXE',
#'/media/kevin/A536-D98F/ben_program_files_x86//wmpshare.exe',
#'/media/kevin/A536-D98F/ben_program_files/ewpexapp.exe',
#'/media/kevin/A536-D98F/ben_program_files/devcon.exe',
#'/media/kevin/A536-D98F/ben_program_files/cygwin-console-helper.exe',
#'/media/kevin/A536-D98F/ben_program_files/bibsort.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//x64launcher.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//91.0.4472.164_91.0.4472.124_chrome_updater.exe',
#'/media/kevin/A536-D98F/ben_program_files/WINWORD.EXE',
#'/media/kevin/A536-D98F/ben_program_files/POWERPNT.EXE',
#'/media/kevin/A536-D98F/ben_program_files_x86//SecAnnotate.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//GoogleUpdate.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//JXR2PNG.exe', 
#'/media/kevin/A536-D98F/ben_program_files_x86//91.0.4472.164_91.0.4472.124_chrome_updater.exe',
#'/media/kevin/A536-D98F/benign_files_win10/displayswitch.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//x64launcher.exe',
#'/media/kevin/A536-D98F/ben_program_files/ErrorReport.exe',
#'/media/kevin/A536-D98F/ben_program_files_x86//ITest.exe',
#'/media/kevin/A536-D98F/benign_files_win10/FlashUtil64_32_0_0_465_pepper.exe',
}


VALID_SECTION_NAMES = ['.edata', '.cdata', '.adata', '.data2', '.data1', '/4', '/19', 'CPADinfo', 'GFIDS', '.phs', 'CONST', '.retplne', '.bootdat', '.didata', '.boxld01', 'local_da', 'text', '.giats', '.gehcont', '.pccode', '.pecode', '.orpc', '.c2r', '_RDATA', '.CRT', '.imrsiv', '.00cfg',   '.gfids', '.didat', '.tls', '.idata', '.bss', '.reloc', '.rsrc', '.xdata', '.pdata', '.rdata', '.data', '.text']

PACKED_SECTION_NAMES = open('counterfit/frameworks/mlsecevade/PEutils/packed_section_names.txt', 'r').read().strip().split('\n')

OPTIONAL_HEADER_ATTRS = [
        "major_linker_version",
        "minor_linker_version",
        "major_operating_system_version",
        "minor_operating_system_version",
        "major_image_version",
        "minor_image_version",
]

LIBRARIES_TO_ADD = {'ADVAPI32.dll' : ['RegQueryValueA',                   
'RegCloseKey',                      
'RegOpenKeyExA',                    
'RegGetValueW',                     
'RegSetValueExW',                   
'RegQueryValueExW',                 
'RegOpenKeyExW'],

'KERNEL32.dll' : [
'GetModuleHandleA',                 
'LoadLibraryA',                    
'VirtualProtect',                   
'lstrcatA',                         
'lstrcpyA',                         
'GetWindowsDirectoryA',             
'FreeLibrary',                      
'GetStartupInfoA',                  
'GlobalAlloc',                      
'GlobalUnlock',                     
'GlobalLock',                       
'GetThreadContext',                 
'VirtualQuery',                     
'GetSystemTimeAsFileTime',          
'InitializeSListHead',              
'CreateEventW',                     
'IsProcessorFeaturePresent',        
'WaitForSingleObject',              
'QueryPerformanceCounter',          
'TerminateProcess',                 
'CreateMutexW',                    
'GetSystemInfo',                   
'RtlCaptureContext',                
'UnhandledExceptionFilter',         
'LoadLibraryExW',                   
'IsDebuggerPresent',                
'SetUnhandledExceptionFilter',      
'GetModuleHandleExW',               
'LoadLibraryExA',                   
'GetCurrentProcessId',              
'OpenThread',                       
'GetLastError',                     
'GetFileAttributesW',               
'GetSystemDirectoryW',              
'SuspendThread',                    
'GetCurrentProcess',                
'GetCurrentThreadId',               
'GetStartupInfoW',                  
'GetModuleHandleW',                 
'ReleaseMutex',                     
'RaiseException',                   
'CloseHandle',                      
'GetProcAddress',                   
'CreateThread',                    
'ResumeThread'      
],
'ole32.dll': [          
'CoTaskMemRealloc',                 
'CoRevokeClassObject',              
'CoRegisterClassObject',            
'GetHGlobalFromStream',             
'IsAccelerator',                    
'OleLockRunning',                   
'OleUninitialize',                  
'OleInitialize',                    
'CoTaskMemFree',                    
'CoTaskMemAlloc',                   
'StringFromGUID2',                  
'CLSIDFromProgID',                 
'CLSIDFromString',                  
'CoGetClassObject',                 
'CreateStreamOnHGlobal',            
'CoInitialize',                     
'CoCreateInstance',
],

"USER32.dll": [
"RegisterWindowMessageW",
"EnableWindow",
"SendMessageW",
"DefWindowProcW",
"LoadMenuW",
"GetCursorPos",
"SetForegroundWindow",
"IsWindowEnabled",
"KillTimer",
"SetTimer",
"GetKeyState",
"GetDlgCtrlID",
"ReuseDDElParam",
"UnpackDDElParam",
"LoadBitmapW",
"SetActiveWindow",
"BringWindowToTop",
"MessageBoxW",
"GetMenuItemInfoW",
"InsertMenuItemW",
"DeleteMenu",
"GetMenuItemCount",
"GetMenuItemID",
"GetSubMenu",
"GetMenuState",
"MapDialogRect",
"IsRectEmpty",
"EnableScrollBar",
"UpdateWindow",
"CopyRect",
"FrameRect",
"IsWindowVisible",
"PostMessageW",
"OffsetRect",
"LoadCursorW",
"GetWindow",
"GetClassNameW",
"GetParent",
"GetDesktopWindow",
"SetWindowLongW",
"GetWindowLongW",
"SetRectEmpty",
"FillRect",
"GetSysColor",
"ScreenToClient",
"ClientToScreen",
"GetWindowRect",
"GetClientRect",
"GetWindowTextLengthW",
"GetWindowTextW",
"SetWindowTextW",
"RedrawWindow",
"InvalidateRgn",
"InvalidateRect",
"EndPaint",
"BeginPaint",
"ReleaseDC",
"GetDC",
"GetSystemMetrics",
"CopyAcceleratorTableW",
"DestroyAcceleratorTable",
"CreateAcceleratorTableW",
"LoadAcceleratorsW",
"ReleaseCapture",
"SetCapture",
"GetFocus",
"SetFocus",
"CharNextW",
"GetDlgItem",
"SetWindowPos",
"MoveWindow",
"DestroyWindow",
"IsChild",
"IsWindow",
"CreateWindowExW",
"GetClassInfoExW",
"RegisterClassExW",
"UnregisterClassW",
"CallWindowProcW"
]


}


    
def process_pe(pe):
    sections = []
    imports = defaultdict(set)
    timestamps = []
    overlays = []
            
    #s[0] name,  s[1] entropy,  s[2] characteristics,  s[3] characteristics lists,  s[4] bytes
    total_section_size = 0
    for s in pe.sections:
        sections.append((s.name, s.entropy, s.characteristics, s.characteristics_lists, bytes(s.content), s.size, s.virtual_size))
        total_section_size += len(bytes(s.content))
        
    #calculate halway section
    curr_size = 0
    curr_sect = 0
    halfway_section = 0
    for s in pe.sections:
        curr_size += len(bytes(s.content))
            
        if curr_size > total_section_size/2:
            halfway_section = curr_sect
            break
            
        curr_sect += 1

    for lib in pe.imports:
        for func in lib.entries:
            imports[lib.name].add(func.name)
                
    timestamps.append(pe.header.time_date_stamps)
        
    overlays.append(bytes(pe.overlay))
    poh = {oh: getattr(pe.optional_header, oh) for oh in OPTIONAL_HEADER_ATTRS}
    return (sections, imports, timestamps, overlays, poh, halfway_section)

class PEMimicryAttack:
    saved_overlay = None
    all_section_names = defaultdict(lambda:0)
    valid_filenames = set()
    section_mids = {}
    
    def __init__(self, huh, **kwargs):
        pass
    
    @staticmethod    
    def sections_similarity(a,b):
        #returns score for similarity between sections of two PE files, lower score = more similar 
        #a, b are section data of two PE files, a is attacker (malicious), b is benign
        #    a[0] name, a[1] entropy, a[2] characteristics, a[3] characteristics list, a[4] bytez
        #idealy b covers a, i.e., b has more sections than a, and the
        #only look at entropy, size, and characteristics, because sections names can be changed
        
        #penalize benign files shorter than target malware
        entropy_penalty = 0
        size_penalty = 0
        char_penalty = 0
        
        total_target_size = 0
        
        for s_a, s_b in itertools.zip_longest(a,b):
            if s_a == None: #incentivize longer benign
                entropy_penalty -= 1
                size_penalty -= min(len(s_b[4])/total_target_size, 1) 
                continue
                
            if s_b == None: #penalize shorter benign
                entropy_penalty += 1
                size_penalty += 1
                char_penalty += len(s_a[3])
                continue    
                
            total_target_size += len(s_a[4])
                
            if s_a[1] == 0:
                entropy_penalty += (s_a[1]-s_b[1])
            else:
                entropy_penalty += (s_a[1]-s_b[1])**2/s_a[1]**2

            if len(s_a[4]) == 0:
                #size_penalty += (len(s_a[4]) - len(s_b[4]))/total_target_size
                pass
            else:
                size_penalty += (len(s_a[4]) - len(s_b[4]))**2/len(s_a[4])**2
                
            if len(s_a[3]) == 0:    
                char_penalty += len(s_a[3].symmetric_difference(s_b[3]))
            else:
                char_penalty += len(s_a[3].symmetric_difference(s_b[3]))**2/len(s_a[3])**2
                
        alpha = 1
        beta = 1
        gamma = 1
        return alpha*entropy_penalty + beta*size_penalty + gamma*char_penalty
        
    @staticmethod    
    def imports_similarity(a,b):
        #returns similarity between imports of two PEs
        #a,b are imports, dicts, with key: library, value: set of functions
        #a is attacker (malicious), b is benign
        penalty = 0
        for lib in a.keys():
            if lib not in b:
                penalty += len(a[lib])
            
            else:
                penalty += len(a[lib].difference(b[lib]))
    
        return 0.1*penalty
        
    @staticmethod
    def similarity(a, b):        
        #a, b are two PE files, a is attacker (malicious), b is benign
        #a[0] sections, a[1] imports, a[2] timestamps, a[3] overlays

        #sections similarity seems to be the only similarity that matters
        similarity = PEMimicryAttack.sections_similarity(a[0], b[0])
        #similarity += PEMimicryAttack.imports_similarity(a[1], b[1])
        
        return similarity
        
    @staticmethod
    def select_benign(sample):
        #sample is processed pe
        
        h = []
        for fn in FILE_DATA.keys(): #can choose from all benign PEs or from known successful (evaded) PEs
        #for fn in SUCCESSFUL_BENIGNS:   
            overlay = FILE_DATA[fn][3][0]
            
            #choose only large files with overlays
            if len(overlay) == 0:
                continue
            if FILE_SIZE[fn] < 1.0*MiB:
                continue
                
                
            PEMimicryAttack.valid_filenames.add(fn)
        
            similarity = PEMimicryAttack.similarity(sample, FILE_DATA[fn])
            
            PEMimicryAttack.section_mids[fn] = FILE_DATA[fn][5]
            
            #heavily penalize when halway_criteria not met
            if len(sample[0]) > FILE_DATA[fn][5]:
                similarity += 1000000000
                
            heapq.heappush(h, (similarity, fn))
            
        #pop N most similar (1)
        lowest = []
        for i in range(1):
            lowest.append(heapq.heappop(h))
            
        return lowest

    @staticmethod    
    def mimic_file(target_pe, target_bytes, benign_pe):
        pe_mod = PEFileModifier(target_bytes)
        
        #unpack first
        pe_mod.upx_unpack()
        
        imports_dict = defaultdict(list)
        

        #add mimicry imports
        for lib in benign_pe[1].keys(): #can either mimic benign imports, or add predetermined imports
        #for lib in LIBRARIES_TO_ADD:

            if lib not in ['KERNEL32.dll', 'ADVAPI32.dll', 'USER32.dll', 'ole32.dll']:
                continue
        
            if lib not in target_pe[1]:
                functions = benign_pe[1][lib]
                #functions = LIBRARIES_TO_ADD[lib]
                for f in functions:
                    if f not in benign_pe[1][lib]:
                        continue
                        
                    if lib == 'KERNEL32.dll' and f not in ALLOWED_FUNCTIONS:
                        continue
                        
                    imports_dict[lib].append(f)
                
            else:
                diff = benign_pe[1][lib].difference(target_pe[1][lib])
                #diff = LIBRARIES_TO_ADD[lib]

                for f in diff:
                    if f not in benign_pe[1][lib]:
                        continue
                        
                    if f in target_pe[1][lib]:
                        continue

                    if lib == 'KERNEL32.dll' and f not in ALLOWED_FUNCTIONS:
                        continue
                        
                    imports_dict[lib].append(f)
                    
        
        #only add imports if not managed application
        #also do not add if target pe has no imports
        if len(target_pe[1]) != 0 and 'mscoree.dll' not in target_pe[1]:
            pe_mod.add_all_imports(imports_dict, False)
        
        names_used = set()

        #rename existing sections
        for ts, bs in zip(target_pe[0], benign_pe[0]): #pe[0] is section data
            name = bs[0]
            if name in PACKED_SECTION_NAMES:
                for vsn in reversed(VALID_SECTION_NAMES):
                    if vsn not in names_used:
                        name = vsn

            pe_mod.rename_section_(ts[0], name) #section[0] is current section name
            names_used.add(name)
        
        
        #add mimicry sections
        if len(target_pe[0]) <= benign_pe[5]:
            for ts, bs in itertools.zip_longest(target_pe[0], benign_pe[0]):
                if ts == None and len(pe_mod.content) < 2*MiB:
                    name = bs[0]

                    if name in names_used or name in PACKED_SECTION_NAMES:
                        changed = False
                        for vsn in reversed(VALID_SECTION_NAMES):
                            if vsn not in names_used:
                                name = vsn
                                changed = True
                                break
                                
                        if not changed:
                            print("name not changed!")
                            name += 's'

                    #leave 30000 buffer from 2MiB
                    free_space = int(2*MiB - len(pe_mod.content) - 30000)
                    free_space = int(free_space/512)*512
                    
                    if free_space > 0:
                        size = bs[5]
                        
                        if size > MiB:
                            free_space -= 2048
                        
                        if size > free_space:
                            size = int(free_space/512)*512

                            
                        if free_space > 0:
                            pe_mod.add_section_w_size(name, bs[2], bs[4][:free_space] + b'\x00'*(size-free_space), size)

                        names_used.add(name)
                    
        #just add the sections, if midway section is not far down enough 
        else:
            sc = 0
            for bs in benign_pe[0]:
                if sc < benign_pe[5]:
                    sc += 1
                    continue
                    
                if len(pe_mod.content) < 2*MiB:
                    name = bs[0]
                    
                    if name in names_used or name in PACKED_SECTION_NAMES:
                        changed = False
                        for vsn in reversed(VALID_SECTION_NAMES):
                            if vsn not in names_used:
                                name = vsn
                                changed = True
                                break
                                
                        if not changed:
                            print("name not changed!")
                            name += 's'

                    free_space = int(2*MiB - len(pe_mod.content) - 30000)
                    free_space = int(free_space/512)*512
                    
                    
                    if free_space > 0:
                        size = bs[5]
                        
                        if size > MiB:
                            free_space -= 2048
                        
                        if size > free_space:
                            size = int(free_space/512)*512
                        
                        if free_space > 0:
                            pe_mod.add_section_w_size(name, bs[2], bs[4][:free_space] + b'\x00'*(size-free_space), size)

                        names_used.add(name)

        #rename new import section
        pe_mod.rename_section_('.l1', '.idata')
        
        #set mimicry timestamps
        pe_mod.set_timestamp(benign_pe[2][0])
        
        #set optional header
        pe_mod.modify_optional_header(benign_pe[4])
        
        
        #add mimicry overlays     
        free_space = int(2*MiB - len(pe_mod.content))
        overlay_length = len(benign_pe[3][0])
        overlay = benign_pe[3][0]
        
        pe_mod.append_overlay(overlay[:free_space])
        
        return pe_mod.content
        
    def generate(self, x, y=None):
        new_files = []
        
        i = 1
        for bytez in x:
            pe = lief.parse(bytez)
            p_pe = process_pe(pe)
            lowest = PEMimicryAttack.select_benign(p_pe)
            
            #use best one
            best = FILE_DATA[lowest[0][1]] #lowest = [(similarity, filename), ...] aka a list of tuples
            new_files.append(PEMimicryAttack.mimic_file(p_pe, bytez, best))
            
            i += 1

        return np.array(new_files)

def get_valid_filenames(directory, filenames):
    for root, dirs, files in os.walk(directory):
        for fn in files:
            if fn.endswith('.exe') or fn.endswith('.EXE'): 
                filenames.append(os.path.join(root, fn))

if __name__ == '__main__':    
    filenames = []
    get_valid_filenames('/media/kevin/A536-D98F/benign_files_win10/', filenames)
    get_valid_filenames('/media/kevin/A536-D98F/ben_program_files/', filenames)
    get_valid_filenames('/media/kevin/A536-D98F/ben_program_files_x86//', filenames)
    
    file_data = {}
    file_size = {}
    
    random.shuffle(filenames)
    i = 0
    for fn in filenames:
        pe = lief.parse(fn)
        if not pe:
            continue
            
        filesize = Path(fn).stat().st_size
        if filesize > 2*MiB:
            continue
        
        
        file_data[fn] = process_pe(pe)
        file_size[fn] = filesize
        
        i += 1
        
        if i%20 == 0:
            print('stored', i, 'files')

            
    with gzip.open('counterfit/frameworks/mlsecevade/PEutils/file_data.pkl.gz', 'wb') as outfile:
        pickle.dump(file_data, outfile)
    
    with gzip.open('counterfit/frameworks/mlsecevade/PEutils/file_size.pkl.gz', 'wb') as outfile:
        pickle.dump(file_size, outfile)

        

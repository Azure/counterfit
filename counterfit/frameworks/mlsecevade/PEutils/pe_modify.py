import lief
import random
import tempfile
import os
import subprocess

class PEFileModifier(object):
    def __init__(self, file_content: bytes, verbose: bool = False):
        self.bytez = file_content
        self.packed_section_names = open('counterfit/frameworks/mlsecevade/PEutils/packed_section_names.txt', 'r').read().strip().split('\n')
        if verbose:
            lief.logging.enable()
        else:
            lief.logging.disable()           

    def _build(self, pe, imports=False):
        builder = lief.PE.Builder(pe)
        if imports:
            # patch the original import table in order to redirect functions to the new import table
            builder.build_imports(True).patch_imports(True)  
        builder.build()
        return builder.get_build()

    def _ispacked(self, pe):
        for s in pe.sections:
            if s.name in self.packed_section_names:
                return True
        return False

    def _section_rename_if_exists(self, pe, section_name, target_name):
        for s in pe.sections:
            if s.name == section_name:
                break
        if s.name == section_name:
            s.name = target_name

    def add_section(self, section_name: str, characteristics: int, section_content: bytes):
        pe = lief.PE.parse(raw=list(self.bytez))
        if self._ispacked(pe):
            return  # don't mess with sections if the file is packed
        replace_name = '.' + ''.join(list(map(chr, [random.randint(ord('a'), ord('z')) for _ in range(6)])))  # example: .nzomcu
        self._section_rename_if_exists(pe, section_name, replace_name)  # rename if exists
        section = lief.PE.Section(name=section_name, content=list(section_content), characteristics=characteristics)
        pe.add_section(section, lief.PE.SECTION_TYPES.UNKNOWN)
        self.bytez = self._build(pe)

    def rename_section_(self, section_name: str, target_name: str):
        pe = lief.PE.parse(raw=list(self.bytez))
        if self._ispacked(pe):
            return  # don't mess with sections if the file is packed
        self._section_rename_if_exists(pe, section_name, target_name)  # rename if exists
        self.bytez = self._build(pe)  # idempotent if the section doesn't exist

    def get_timestamp(self):
        pe = lief.PE.parse(raw=list(self.bytez))
        return pe.header.time_date_stamps
    
    def set_timestamp(self, timestamp: int):
        pe = lief.PE.parse(raw=list(self.bytez))
        pe.header.time_date_stamps = timestamp
        self.bytez = self._build(pe)

    def append_overlay(self, content: bytes):
        self.bytez += content

    def add_imports(self, library, functions):
        pe = lief.PE.parse(raw=list(self.bytez))
        lib = pe.add_library(library)
        for f in functions:
            lib.add_entry(f)
        self.bytez = self._build(pe)

    def upx_unpack(self):
        # dump to a temporary file
        tmpfilename = os.path.join(
            tempfile._get_default_tempdir(), next(tempfile._get_candidate_names()))

        with open(tmpfilename, 'wb') as outfile:
            outfile.write(self.bytez)

        # test with upx -t
        with open(os.devnull, 'w') as DEVNULL:
            retcode = subprocess.call(
                ['upx', tmpfilename, '-t'], stdout=DEVNULL, stderr=DEVNULL
            )

        if retcode == 0:
            with open(os.devnull, 'w') as DEVNULL:
                retcode = subprocess.call(
                    ['upx', tmpfilename, '-d', '-o', tmpfilename + '_unpacked'], stdout=DEVNULL, stderr=DEVNULL
                )
            if retcode == 0:
                with open(tmpfilename + '_unpacked', 'rb') as result:
                    self.bytez = result.read()

        os.unlink(tmpfilename)

        return
        
    def modify_optional_header(self, boh):
        pe = lief.PE.parse(raw=list(self.bytez))

        for key in boh.keys():
            pe.optional_header.__setattr__(key, boh[key])

        self.bytez = self._build(pe)

    def add_all_imports(self, imports_dict, disable = False):
        pe = lief.PE.parse(raw=list(self.bytez))
        
        for library in imports_dict.keys():
            lib = pe.add_library(library)
            for f in imports_dict[library]:
                existing_functions = {e.name for e in lib.entries}
                if f not in existing_functions:
                    lib.add_entry(f)
                    
        if disable:
            pe.optional_header.dll_characteristics &= ~lief.PE.DLL_CHARACTERISTICS.DYNAMIC_BASE
            pe.optional_header.dll_characteristics &= ~lief.PE.DLL_CHARACTERISTICS.NX_COMPAT
            
        self.bytez = self._build(pe, True)
        return

    def add_section_w_size(self, section_name: str, characteristics: int, section_content: bytes, size=None):
        pe = lief.PE.parse(raw=list(self.bytez))
        if self._ispacked(pe):
            return  # don't mess with sections if the file is packed
        replace_name = '.' + ''.join(list(map(chr, [random.randint(ord('a'), ord('z')) for _ in range(6)])))  # example: .nzomcu
        self._section_rename_if_exists(pe, section_name, replace_name)  # rename if exists
        section = lief.PE.Section(name=section_name, content=list(section_content), characteristics=characteristics)
        if size != None:
            section.size = size
        pe.add_section(section, lief.PE.SECTION_TYPES.UNKNOWN)
        self.bytez = self._build(pe)
        
    @property
    def content(self):
        return bytes(self.bytez)

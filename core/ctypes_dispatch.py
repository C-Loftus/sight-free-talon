"""
ctypes-only replacement for win32com.client.Dispatch, with SAPI.SpVoice support.
Windows only. No third-party packages.
"""
import ctypes
import enum
import os
import time
import traceback
from ctypes import (POINTER, Structure, Union, WinDLL, WINFUNCTYPE, byref,
                    c_double, c_float, c_int32, c_int64, c_long, c_short,
                    c_ubyte, c_uint, c_uint32, c_ushort, c_void_p, c_wchar_p,
                    wintypes)

ole32 = WinDLL("ole32")
oleaut32 = WinDLL("oleaut32")
user32 = WinDLL("user32")

class GUID(Structure):
    _fields_ = [("Data1", c_uint32), ("Data2", c_ushort),
                ("Data3", c_ushort), ("Data4", c_ubyte * 8)]

class _VU(Union):
    _fields_ = [("llVal", c_int64), ("lVal", c_int32), ("fltVal", c_float),
                ("dblVal", c_double), ("boolVal", c_short),
                ("bstrVal", c_void_p), ("pdispVal", c_void_p),
                ("_pad", c_void_p * 2)]  # forces correct size on x86 and x64

class VARIANT(Structure):
    _fields_ = [("vt", c_ushort), ("r1", c_ushort), ("r2", c_ushort),
                ("r3", c_ushort), ("u", _VU)]

class DISPPARAMS(Structure):
    _fields_ = [("rgvarg", POINTER(VARIANT)),
                ("rgdispidNamedArgs", POINTER(c_long)),
                ("cArgs", c_uint), ("cNamedArgs", c_uint)]

class EXCEPINFO(Structure):
    _fields_ = [("wCode", c_ushort), ("wReserved", c_ushort),
                ("bstrSource", c_void_p), ("bstrDescription", c_void_p),
                ("bstrHelpFile", c_void_p), ("dwHelpContext", c_uint32),
                ("pvReserved", c_void_p), ("pfnDeferredFillIn", c_void_p),
                ("scode", c_long)]

ole32.CoInitializeEx.argtypes = [c_void_p, c_uint32]
ole32.CoInitializeEx.restype = c_long
ole32.CLSIDFromProgID.argtypes = [c_wchar_p, POINTER(GUID)]
ole32.CLSIDFromProgID.restype = c_long
ole32.IIDFromString.argtypes = [c_wchar_p, POINTER(GUID)]
ole32.IIDFromString.restype = c_long
ole32.CoCreateInstance.argtypes = [POINTER(GUID), c_void_p, c_uint32,
                                   POINTER(GUID), POINTER(c_void_p)]
ole32.CoCreateInstance.restype = c_long
oleaut32.GetActiveObject.argtypes = [POINTER(GUID), c_void_p, POINTER(c_void_p)]
oleaut32.GetActiveObject.restype = c_long
oleaut32.SysAllocString.argtypes = [c_wchar_p]
oleaut32.SysAllocString.restype = c_void_p
oleaut32.SysFreeString.argtypes = [c_void_p]
oleaut32.VariantClear.argtypes = [POINTER(VARIANT)]
oleaut32.VariantClear.restype = c_long
oleaut32.VariantInit.argtypes = [POINTER(VARIANT)]
user32.PeekMessageW.argtypes = [POINTER(wintypes.MSG), wintypes.HWND,
                                wintypes.UINT, wintypes.UINT, wintypes.UINT]
user32.PeekMessageW.restype = wintypes.BOOL
user32.TranslateMessage.argtypes = [POINTER(wintypes.MSG)]
user32.DispatchMessageW.argtypes = [POINTER(wintypes.MSG)]
user32.DispatchMessageW.restype = ctypes.c_ssize_t

COINIT_APARTMENTTHREADED = 2
CLSCTX_ALL = 23
LOCALE_USER_DEFAULT = 0x0400
DISPATCH_METHOD, DISPATCH_PROPERTYGET = 1, 2
DISPATCH_PROPERTYPUT, DISPATCH_PROPERTYPUTREF = 4, 8
DISPID_PROPERTYPUT, DISPID_NEWENUM = -3, -4
DISP_E_EXCEPTION = -2147352567
DISP_E_MEMBERNOTFOUND = -2147352573
E_NOTIMPL = -2147467263
E_NOINTERFACE = -2147467262

VT_EMPTY, VT_NULL, VT_I2, VT_I4, VT_R4, VT_R8 = 0, 1, 2, 3, 4, 5
VT_DATE, VT_BSTR, VT_DISPATCH, VT_ERROR, VT_BOOL = 7, 8, 9, 10, 11
VT_CY, VT_VARIANT, VT_UNKNOWN, VT_DECIMAL = 6, 12, 13, 14
VT_I1, VT_UI1, VT_UI2, VT_UI4, VT_I8, VT_UI8 = 16, 17, 18, 19, 20, 21
VT_INT, VT_UINT = 22, 23
VT_BYREF = 0x4000

ole32.CoInitializeEx(None, COINIT_APARTMENTTHREADED)

def _check(hr, what=""):
    if hr < 0:
        raise OSError(f"COM error 0x{hr & 0xFFFFFFFF:08X} {what}".strip())

def _guid(s):
    g = GUID()
    _check(ole32.IIDFromString(s, byref(g)), f"(bad GUID {s})")
    return g

_IID_NULL = GUID()
_IID_IUnknown = _guid("{00000000-0000-0000-C000-000000000046}")
_IID_IDispatch = _guid("{00020400-0000-0000-C000-000000000046}")
_IID_IEnumVARIANT = _guid("{00020404-0000-0000-C000-000000000046}")
_IID_IConnectionPointContainer = _guid("{B196B284-BAB4-101A-B69C-00AA00341D07}")

def _slot(ptr, index):
    """Return the address of vtable slot `index` of COM interface `ptr`."""
    vtbl = ctypes.cast(ptr, POINTER(c_void_p))[0]
    return ctypes.cast(vtbl, POINTER(c_void_p))[index]

def _vcall(ptr, index, argtypes, *args):
    """Call vtable slot `index` of COM interface `ptr`; returns the HRESULT."""
    return WINFUNCTYPE(c_long, c_void_p, *argtypes)(_slot(ptr, index))(ptr, *args)

def _addref(ptr):
    WINFUNCTYPE(c_uint32, c_void_p)(_slot(ptr, 1))(ptr)

def _release(ptr):
    WINFUNCTYPE(c_uint32, c_void_p)(_slot(ptr, 2))(ptr)
 
def _to_variant(v, value):
    oleaut32.VariantInit(byref(v))
    if value is None:
        v.vt = VT_EMPTY
    elif isinstance(value, bool):
        v.vt, v.u.boolVal = VT_BOOL, (-1 if value else 0)
    elif isinstance(value, int):
        value = int(value)
        if -2**31 <= value < 2**31:
            v.vt, v.u.lVal = VT_I4, value
        else:
            v.vt, v.u.llVal = VT_I8, value
    elif isinstance(value, float):
        v.vt, v.u.dblVal = VT_R8, value
    elif isinstance(value, str):
        v.vt, v.u.bstrVal = VT_BSTR, oleaut32.SysAllocString(value)
    elif isinstance(value, Dispatch):
        _addref(value._ptr)  # VariantClear will Release it
        v.vt, v.u.pdispVal = VT_DISPATCH, value._ptr
    else:
        raise TypeError(f"Unsupported argument type: {type(value).__name__}")

def _wrap_iface(ptr, cls, unknown):
    """Wrap an interface pointer found in a VARIANT; the wrapper gets its own reference."""
    if not ptr:
        return None
    if unknown:
        out = c_void_p()
        _check(_vcall(ptr, 0, [POINTER(GUID), POINTER(c_void_p)],
                      byref(_IID_IDispatch), byref(out)), "(QueryInterface IDispatch)")
        return cls(_ptr=out.value)
    _addref(ptr)
    return cls(_ptr=ptr)

_BYREF_TYPES = {VT_I2: c_short, VT_I4: c_int32, VT_ERROR: c_int32, VT_R4: c_float,
                VT_R8: c_double, VT_DATE: c_double, VT_BOOL: c_short,
                VT_UI1: c_ubyte, VT_I8: c_int64, VT_I1: ctypes.c_byte,
                VT_UI2: c_ushort, VT_UI4: c_uint32, VT_UI8: ctypes.c_uint64,
                VT_INT: c_int32, VT_UINT: c_uint32, VT_CY: c_int64}

def _decimal(v):
    """Decode a DECIMAL (it overlays the whole 16-byte VARIANT):
    r1 = scale (low byte) + sign (high byte), r2/r3 = Hi32, u = Lo64."""
    scale = v.r1 & 0xFF
    negative = bool((v.r1 >> 8) & 0x80)
    hi32 = v.r2 | (v.r3 << 16)
    lo64 = v.u.llVal & 0xFFFFFFFFFFFFFFFF
    mantissa = (hi32 << 64) | lo64
    if negative:
        mantissa = -mantissa
    return mantissa if scale == 0 else mantissa / (10 ** scale)

def _deref(v, cls):
    base = v.vt & 0x0FFF
    addr = v.u.pdispVal
    if not addr:
        return None
    if base == VT_DECIMAL:
        return _decimal(VARIANT.from_address(addr))
    if base == VT_VARIANT:
        return _from_variant(VARIANT.from_address(addr), cls, clear=False)
    if base == VT_BSTR:
        p = c_void_p.from_address(addr).value
        return ctypes.wstring_at(p) if p else ""
    if base in (VT_DISPATCH, VT_UNKNOWN):
        return _wrap_iface(c_void_p.from_address(addr).value, cls, base == VT_UNKNOWN)
    ctype = _BYREF_TYPES.get(base)
    if ctype is None:
        raise NotImplementedError(f"VARIANT type {v.vt:#x} not supported")
    val = ctype.from_address(addr).value
    if base == VT_BOOL:
        return val != 0
    if base == VT_CY:
        return val / 10000
    return val

def _from_variant(v, cls=None, clear=True):
    cls = cls or Dispatch
    vt = v.vt
    try:
        if vt & VT_BYREF:
            return _deref(v, cls)
        if vt in (VT_EMPTY, VT_NULL):
            return None
        if vt == VT_BSTR:
            return ctypes.wstring_at(v.u.bstrVal) if v.u.bstrVal else ""
        if vt == VT_BOOL:
            return v.u.boolVal != 0
        if vt == VT_I2:
            return c_short(v.u.lVal & 0xFFFF).value
        if vt in (VT_I4, VT_ERROR):
            return v.u.lVal
        if vt == VT_I8:
            return v.u.llVal
        if vt == VT_R4:
            return v.u.fltVal
        if vt in (VT_R8, VT_DATE):  # DATE = OLE days since 1899-12-30
            return v.u.dblVal
        if vt == VT_UI1:
            return v.u.lVal & 0xFF
        if vt == VT_DECIMAL:
            return _decimal(v)
        if vt == VT_CY:
            return v.u.llVal / 10000
        if vt == VT_I1:
            return ctypes.c_byte(v.u.lVal & 0xFF).value
        if vt == VT_UI2:
            return v.u.lVal & 0xFFFF
        if vt in (VT_UI4, VT_UINT):
            return v.u.lVal & 0xFFFFFFFF
        if vt == VT_INT:
            return v.u.lVal
        if vt == VT_UI8:
            return v.u.llVal & 0xFFFFFFFFFFFFFFFF
        if vt in (VT_DISPATCH, VT_UNKNOWN):
            return _wrap_iface(v.u.pdispVal, cls, vt == VT_UNKNOWN)
        raise NotImplementedError(f"VARIANT type {vt} not supported")
    finally:
        if clear and not (vt & VT_BYREF):
            oleaut32.VariantClear(byref(v))

def pump_messages(timeout_ms=0):
    """Dispatch pending Windows messages for up to timeout_ms (0 = just drain the queue).
    COM events from a single-threaded apartment are only delivered while this runs."""
    msg = wintypes.MSG()
    end = time.monotonic() + timeout_ms / 1000.0
    while True:
        while user32.PeekMessageW(byref(msg), None, 0, 0, 1):
            user32.TranslateMessage(byref(msg))
            user32.DispatchMessageW(byref(msg))
        if time.monotonic() >= end:
            return
        time.sleep(0.005)

_QI_T = WINFUNCTYPE(c_long, c_void_p, POINTER(GUID), POINTER(c_void_p))
_REF_T = WINFUNCTYPE(c_uint32, c_void_p)
_GTIC_T = WINFUNCTYPE(c_long, c_void_p, POINTER(c_uint))
_GTI_T = WINFUNCTYPE(c_long, c_void_p, c_uint, c_uint32, POINTER(c_void_p))
_GIDS_T = WINFUNCTYPE(c_long, c_void_p, POINTER(GUID), POINTER(c_wchar_p),
                      c_uint, c_uint32, POINTER(c_long))
_INV_T = WINFUNCTYPE(c_long, c_void_p, c_long, POINTER(GUID), c_uint32, c_ushort,
                     POINTER(DISPPARAMS), POINTER(VARIANT), POINTER(EXCEPINFO),
                     POINTER(c_uint))

class _EventSink:
    """A COM IDispatch object implemented in Python, used as an outgoing-interface sink."""

    def __init__(self, iid, names, callback, cls):
        self._iid, self._names, self._cb, self._cls = iid, names, callback, cls
        self._refs = 1

        def qi(this, riid, ppv):
            req = bytes(riid[0])
            if req in (bytes(_IID_IUnknown), bytes(_IID_IDispatch), bytes(self._iid)):
                ppv[0] = this
                self._refs += 1
                return 0
            ppv[0] = None
            return E_NOINTERFACE

        def addref(this):
            self._refs += 1
            return self._refs

        def release(this):
            self._refs -= 1
            return self._refs

        def gtic(this, pct):
            pct[0] = 0
            return 0

        def gti(this, i, lcid, pp):
            return E_NOTIMPL

        def gids(this, riid, names, n, lcid, ids):
            return E_NOTIMPL

        def invoke(this, dispid, riid, lcid, flags, pparams, pres, pexc, perr):
            name = self._names.get(dispid)
            if name is None:
                return DISP_E_MEMBERNOTFOUND
            try:
                p = pparams[0]
                # rgvarg is in reverse order; restore declaration order
                args = []
                for i in range(p.cArgs - 1, -1, -1):
                    try:
                        args.append(_from_variant(p.rgvarg[i], self._cls, clear=False))
                    except NotImplementedError as e:
                        print(f"[ctypes_dispatch] {name}: {e}; passing None")
                        args.append(None)
                self._cb(name, *args)
            except Exception:
                traceback.print_exc()
            return 0

        # keep the callback objects alive for as long as the sink lives
        self._fns = (_QI_T(qi), _REF_T(addref), _REF_T(release), _GTIC_T(gtic),
                     _GTI_T(gti), _GIDS_T(gids), _INV_T(invoke))
        self._vtbl = (c_void_p * 7)(*[ctypes.cast(f, c_void_p).value for f in self._fns])
        self._obj = c_void_p(ctypes.addressof(self._vtbl))
        self.iface = ctypes.addressof(self._obj)  # the COM interface pointer

class _Connection:
    def __init__(self, cp, cookie, sink):
        self._cp, self._cookie, self._sink = cp, cookie, sink

    def close(self):
        if self._cp:
            _vcall(self._cp, 6, [c_uint32], self._cookie)  # IConnectionPoint::Unadvise
            _release(self._cp)
            self._cp = None

    __enter__ = lambda self: self
    __exit__ = lambda self, *a: self.close()


class _Member:
    def __init__(self, obj, name):
        self._obj, self._name = obj, name

    def __call__(self, *args):
        return self._obj._invoke(self._name, DISPATCH_METHOD | DISPATCH_PROPERTYGET, args)


class Dispatch:
    _PROPS = frozenset()   # names read directly as properties (no parentheses)
    _CHILD = None          # class used for returned objects; None -> Dispatch

    def __init__(self, progid=None, *, _ptr=None):
        object.__setattr__(self, "_ptr", None)
        object.__setattr__(self, "_ids", {})
        if _ptr is None:
            clsid = GUID()
            _check(ole32.CLSIDFromProgID(progid, byref(clsid)), f"(ProgID {progid!r})")
            p = c_void_p()
            _check(ole32.CoCreateInstance(byref(clsid), None, CLSCTX_ALL,
                                          byref(_IID_IDispatch), byref(p)),
                   f"(CoCreateInstance {progid!r})")
            _ptr = p.value
        object.__setattr__(self, "_ptr", _ptr)

    @classmethod
    def active(cls, progid):
        """Attach to a running instance (like GetActiveObject)."""
        clsid = GUID()
        _check(ole32.CLSIDFromProgID(progid, byref(clsid)))
        unk = c_void_p()
        _check(oleaut32.GetActiveObject(byref(clsid), None, byref(unk)), "(GetActiveObject)")
        disp = c_void_p()
        _check(_vcall(unk.value, 0, [POINTER(GUID), POINTER(c_void_p)],
                      byref(_IID_IDispatch), byref(disp)))
        _release(unk.value)
        return cls(_ptr=disp.value)

    # ---- low level
    def _qi(self, iid):
        out = c_void_p()
        _check(_vcall(self._ptr, 0, [POINTER(GUID), POINTER(c_void_p)],
                      byref(iid), byref(out)), "(QueryInterface)")
        return out.value

    def _dispid(self, name):
        ids = self._ids
        if name not in ids:
            names = (c_wchar_p * 1)(name)
            did = c_long()
            _check(_vcall(self._ptr, 5,
                          [POINTER(GUID), POINTER(c_wchar_p), c_uint, c_uint32, POINTER(c_long)],
                          byref(_IID_NULL), names, 1, LOCALE_USER_DEFAULT, byref(did)),
                   f"(unknown member {name!r})")
            ids[name] = did.value
        return ids[name]

    def _invoke(self, name, flags, args):
        return self._invoke_id(self._dispid(name), flags, args, name)

    def _invoke_id(self, dispid, flags, args, name="", raw=False):
        n = len(args)
        argv = (VARIANT * max(n, 1))()
        for i, a in enumerate(reversed(args)):  # IDispatch wants reverse order
            _to_variant(argv[i], a)

        params = DISPPARAMS(argv if n else None, None, n, 0)
        put_id = c_long(DISPID_PROPERTYPUT)
        if flags & (DISPATCH_PROPERTYPUT | DISPATCH_PROPERTYPUTREF):
            params.rgdispidNamedArgs = ctypes.pointer(put_id)
            params.cNamedArgs = 1

        result, exc, argerr = VARIANT(), EXCEPINFO(), c_uint(0)
        oleaut32.VariantInit(byref(result))
        try:
            hr = _vcall(self._ptr, 6,
                        [c_long, POINTER(GUID), c_uint32, c_ushort, POINTER(DISPPARAMS),
                         POINTER(VARIANT), POINTER(EXCEPINFO), POINTER(c_uint)],
                        dispid, byref(_IID_NULL), LOCALE_USER_DEFAULT, flags,
                        byref(params), byref(result), byref(exc), byref(argerr))
            if hr == DISP_E_EXCEPTION:
                desc = ctypes.wstring_at(exc.bstrDescription) if exc.bstrDescription else ""
                src = ctypes.wstring_at(exc.bstrSource) if exc.bstrSource else ""
                for b in (exc.bstrDescription, exc.bstrSource, exc.bstrHelpFile):
                    if b:
                        oleaut32.SysFreeString(b)
                raise OSError(f"{src}: {desc}" if src else desc)
            _check(hr, f"(Invoke {name!r}, bad arg index {argerr.value})")
        finally:
            for i in range(n):
                oleaut32.VariantClear(byref(argv[i]))
        if raw:
            return result
        return _from_variant(result, type(self)._CHILD or Dispatch)

    # ---- python-facing API
    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self._PROPS:
            return self._invoke(name, DISPATCH_PROPERTYGET, ())
        return _Member(self, name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            return object.__setattr__(self, name, value)
        flag = DISPATCH_PROPERTYPUTREF if isinstance(value, Dispatch) else DISPATCH_PROPERTYPUT
        self._invoke(name, flag, (value,))

    def put(self, name, *args):
        """Indexed property set: obj.put('Item', index, value). Last argument is the value."""
        flag = DISPATCH_PROPERTYPUTREF if isinstance(args[-1], Dispatch) else DISPATCH_PROPERTYPUT
        self._invoke(name, flag, args)

    # ---- collections: iteration via _NewEnum, plus Count / Item
    def __iter__(self):
        raw = self._invoke_id(DISPID_NEWENUM, DISPATCH_METHOD | DISPATCH_PROPERTYGET,
                              (), "_NewEnum", raw=True)
        enum_ptr = c_void_p()
        try:
            _check(_vcall(raw.u.pdispVal, 0, [POINTER(GUID), POINTER(c_void_p)],
                          byref(_IID_IEnumVARIANT), byref(enum_ptr)),
                   "(QueryInterface IEnumVARIANT)")
        finally:
            oleaut32.VariantClear(byref(raw))
        child = type(self)._CHILD or Dispatch
        try:
            while True:
                item, fetched = VARIANT(), c_uint32(0)
                oleaut32.VariantInit(byref(item))
                # IEnumVARIANT::Next is slot 3 (S_FALSE with fetched == 0 means done)
                _check(_vcall(enum_ptr.value, 3,
                              [c_uint32, POINTER(VARIANT), POINTER(c_uint32)],
                              1, byref(item), byref(fetched)), "(IEnumVARIANT::Next)")
                if fetched.value == 0:
                    break
                yield _from_variant(item, child)
        finally:
            _release(enum_ptr.value)

    def __len__(self):
        return int(self._invoke("Count", DISPATCH_PROPERTYGET, ()))

    def __getitem__(self, i):
        if isinstance(i, int):
            n = len(self)
            if i < 0:
                i += n
            if not 0 <= i < n:
                raise IndexError("collection index out of range")
        return self._invoke("Item", DISPATCH_METHOD | DISPATCH_PROPERTYGET, (i,))

    def __bool__(self):
        return True

    # ---- events (connection points)
    def connect_events(self, iid, names, callback, child=None):
        """Subscribe to an outgoing dispinterface.
        iid: GUID string; names: {dispid: event name}; callback(name, *args).
        Returns a connection; call .close() to unsubscribe."""
        guid = _guid(iid)
        cpc = self._qi(_IID_IConnectionPointContainer)
        cp = c_void_p()
        try:  # IConnectionPointContainer::FindConnectionPoint is slot 4
            _check(_vcall(cpc, 4, [POINTER(GUID), POINTER(c_void_p)],
                          byref(guid), byref(cp)), "(FindConnectionPoint)")
        finally:
            _release(cpc)
        sink = _EventSink(guid, names, callback, child or type(self)._CHILD or Dispatch)
        cookie = c_uint32()
        try:  # IConnectionPoint::Advise is slot 5
            _check(_vcall(cp.value, 5, [c_void_p, POINTER(c_uint32)],
                          sink.iface, byref(cookie)), "(Advise)")
        except Exception:
            _release(cp.value)
            raise
        return _Connection(cp.value, cookie.value, sink)

    def __del__(self):
        try:
            if self._ptr:
                _release(self._ptr)
        except Exception:
            pass

Dispatch._CHILD = Dispatch


class SpeakFlags(enum.IntFlag):          # SpeechVoiceSpeakFlags
    DEFAULT = 0
    ASYNC = 1
    PURGE_BEFORE_SPEAK = 2
    IS_FILENAME = 4
    IS_XML = 8
    IS_NOT_XML = 16
    PERSIST_XML = 32
    NLP_SPEAK_PUNC = 64


class VoiceEvents(enum.IntFlag):         # SpeechVoiceEvents (for EventInterests)
    START_INPUT_STREAM = 2
    END_INPUT_STREAM = 4
    VOICE_CHANGE = 8
    BOOKMARK = 16
    WORD_BOUNDARY = 32
    PHONEME = 64
    SENTENCE_BOUNDARY = 128
    VISEME = 256
    AUDIO_LEVEL = 512
    PRIVATE = 1024
    ALL = 33790


class RunningState(enum.IntEnum):        # SpeechRunState
    DONE = 1
    IS_SPEAKING = 2

SSFM_CREATE_FOR_WRITE = 3                # SpeechStreamFileMode

_SAPI_PROPS = frozenset("""
Status Voice AudioOutput AudioOutputStream Rate Volume EventInterests Priority
AlertBoundary SynchronousSpeakTimeout AllowAudioOutputFormatChangesOnNextSet
CurrentStreamNumber LastStreamNumberQueued LastResult RunningState InputWordPosition
InputWordLength InputSentencePosition InputSentenceLength LastBookmark LastBookmarkId
PhonemeId VisemeId Id DataKey Category Count Type Guid Format
""".split())

_SPVOICE_EVENT_IID = "{A372ACD1-3BEF-4BBD-8FFB-CB3E2B416AF8}"   # _ISpeechVoiceEvents
_SPVOICE_EVENTS = {1: "StartStream", 2: "EndStream", 3: "VoiceChange", 4: "Bookmark",
                   5: "Word", 6: "Phoneme", 7: "SentenceBoundary", 8: "Viseme",
                   9: "AudioLevel", 10: "EnginePrivate"}


class SapiObject(Dispatch):
    """Any SAPI automation object. Known SAPI properties are read without parentheses."""
    _PROPS = _SAPI_PROPS

    def __repr__(self):
        try:
            return f"<SapiObject {self.Id}>"
        except Exception:
            return f"<SapiObject 0x{self._ptr:x}>"

SapiObject._CHILD = SapiObject


class SpVoice(SapiObject):
    """SAPI.SpVoice. All COM members work under their original names (Speak, Pause,
    Resume, Skip, GetVoices, GetAudioOutputs, WaitUntilDone, Rate, Volume, ...)."""

    def __init__(self, *, _ptr=None):
        super().__init__("SAPI.SpVoice", _ptr=_ptr)
        object.__setattr__(self, "_conns", [])

    def __repr__(self):
        return f"<SpVoice 0x{self._ptr:x}>"

    def speak(self, text, flags=0):
        """Speak text (or XML/file depending on flags); returns the stream number."""
        return self.Speak(text, int(flags))

    def wait(self, timeout_ms=-1):
        """Wait for async speech to finish while pumping messages (so events fire).
        Returns True when finished, False on timeout."""
        end = None if timeout_ms < 0 else time.monotonic() + timeout_ms / 1000.0
        while True:
            pump_messages(0)
            if self.WaitUntilDone(0):
                return True
            if end is not None and time.monotonic() >= end:
                return False
            time.sleep(0.01)

    def find_voice(self, text, optional=""):
        """First installed voice whose description contains `text` (case-insensitive)."""
        for tok in self.GetVoices("", optional):
            if text.lower() in tok.GetDescription().lower():
                return tok
        return None

    def connect(self, handler, interests=VoiceEvents.ALL):
        """Subscribe to SpVoice events. `handler` is either an object with methods named
        On<Event> (OnWord, OnEndStream, OnBookmark, ...) or a callable(name, *args).
        Events arrive only while messages are pumped (wait(), pump_messages())."""
        self.EventInterests = int(interests)

        def dispatch(name, *args):
            fn = getattr(handler, "On" + name, None)
            if fn is not None:
                fn(*args)
            elif callable(handler):
                handler(name, *args)

        conn = self.connect_events(_SPVOICE_EVENT_IID, _SPVOICE_EVENTS, dispatch, SapiObject)
        self._conns.append(conn)
        return conn

    def disconnect(self):
        for c in self._conns:
            c.close()
        self._conns.clear()

    def save_wav(self, text, path, flags=0):
        """Render speech to a WAV file using this voice's Voice/Rate/Volume."""
        stream = SapiObject("SAPI.SpFileStream")
        stream.Open(os.fspath(path), SSFM_CREATE_FOR_WRITE, False)
        try:
            v = SpVoice()
            v.Voice = self.Voice
            v.Rate = self.Rate
            v.Volume = self.Volume
            v.AudioOutputStream = stream
            v.Speak(text, int(flags) & ~int(SpeakFlags.ASYNC))
        finally:
            stream.Close()

# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NV Access Limited, Łukasz Golonka, Leonard de Ruijter
# This file is covered by the GNU Lesser General Public License, version 2.1.
# See the file license.txt for more details.

import ctypes
import time

# Load the NVDA client library
# get dir of this file
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
dll_path = os.path.join(dir_path, "nvdaControllerClient64.dll")

clientLib = ctypes.windll.LoadLibrary(dll_path)

# Test if NVDA is running, and if its not show a message
res = clientLib.nvdaController_testIfRunning()
if res != 0:
	errorMessage = str(ctypes.WinError(res))
	ctypes.windll.user32.MessageBoxW(0, "Error: %s" % errorMessage, "Error communicating with NVDA", 0)

# Speak and braille some messages
for count in range(4):
	clientLib.nvdaController_speakText("This is a test client for NVDA")
	clientLib.nvdaController_brailleMessage("Time: %g seconds" % (0.75 * count))
	time.sleep(0.625)
	clientLib.nvdaController_cancelSpeech()
clientLib.nvdaController_speakText("This is a test client for NVDA!")
clientLib.nvdaController_brailleMessage("Test completed!")
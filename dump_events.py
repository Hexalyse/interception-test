import pyWinhook as pyHook
import pythoncom

def OnKeyboardEvent(event):
    # 0x10 is the flag for LLKHF_INJECTED indicating the event was injected.
    if event.Injected:
        print("Injected input detected")
    else:
        print("Real input detected")

    # Return True to pass the event to other handlers
    return True

# Create a hook manager
hm = pyHook.HookManager()
# Watch for all keyboard events
hm.KeyDown = OnKeyboardEvent
hm.MouseLeftDown = OnKeyboardEvent
# Set the hook
hm.HookKeyboard()
hm.HookMouse()
# Wait forever
pythoncom.PumpMessages()

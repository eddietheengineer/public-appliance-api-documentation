# Writable Binary Sensor Review

110 ERDs currently classified as `binary_sensor` but have `write` in operations.
They need to be reclassified as `switch` or `button`.

---

## Switch (76 ERDs)

Self-contained toggles, option states, mode controls. Each ERD is both read and write.

### 0x004f Enhanced Sabbath Mode Status

```json
{
  "name": "Enhanced Sabbath Mode Status",
  "id": "0x004f",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Specifies whether Enhanced Sabbath Mode is active.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Enhanced Sabbath Mode State",
      "type": "enum",
      "values": {
        "0": "Inactive",
        "1": "Active"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Enhanced Sabbath Mode Status: Sabbath mode toggle."
}
```

### 0x101e Nighttime Snack Mode Status

```json
{
  "name": "Nighttime Snack Mode Status",
  "id": "0x101e",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Nighttime Snack Mode feature is turned on or off.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Nighttime Snack Mode Status",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Nighttime Snack Mode Status: Boolean writable switch."
}
```

### 0x102c Lock out feature state

```json
{
  "name": "Lock out feature state",
  "id": "0x102c",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to update the lock out feature state.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Lock out feature state",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Lock out feature state: Boolean writable switch."
}
```

### 0x102d Display always on feature

```json
{
  "name": "Display always on feature",
  "id": "0x102d",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to force the display to be on all the time",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Display always on feature state",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Display always on feature: Boolean writable switch."
}
```

### 0x1032 Door Mute Status Upper Compartment

```json
{
  "name": "Door Mute Status Upper Compartment",
  "id": "0x1032",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Door mute functionality, upper compartment.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Door Mute Status Upper Compartment",
      "type": "enum",
      "values": {
        "0": "Off",
        "1": "On",
        "255": "Not Applicable"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "device_class": "door",
  "confidence": "high",
  "comment": "Door Mute Status Upper Compartment: Door open/closed binary sensor."
}
```

### 0x1033 Door Mute Status Lower Compartment

```json
{
  "name": "Door Mute Status Lower Compartment",
  "id": "0x1033",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Door mute functionality, lower compartment.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Door Mute Status Lower Compartment",
      "type": "enum",
      "values": {
        "0": "Off",
        "1": "On",
        "255": "Not Applicable"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "device_class": "door",
  "confidence": "high",
  "comment": "Door Mute Status Lower Compartment: Door open/closed binary sensor."
}
```

### 0x1034 Door Mute Status Middle Compartment

```json
{
  "name": "Door Mute Status Middle Compartment",
  "id": "0x1034",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Door mute functionality, middle compartment.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Door Mute Status Middle Compartment",
      "type": "enum",
      "values": {
        "0": "Off",
        "1": "On",
        "255": "Not Applicable"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "device_class": "door",
  "confidence": "high",
  "comment": "Door Mute Status Middle Compartment: Door open/closed binary sensor."
}
```

### 0x1053 Autofill pitcher feature request

```json
{
  "name": "Autofill pitcher feature request",
  "id": "0x1053",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request to enable or disable autofill pitcher feature",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Autofill pitcher feature request",
      "type": "enum",
      "values": {
        "0": "Disable",
        "1": "Enable"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Autofill pitcher feature request: Binary enum writable switch."
}
```

### 0x1168 Valve Manual Override Status

```json
{
  "name": "Valve Manual Override Status",
  "id": "0x1168",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Indicates valve is in manual override state.  Must be cleared before a valve position command accepted.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Manual Override",
      "type": "enum",
      "values": {
        "0": "Clear",
        "1": "Set"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Valve Manual Override Status: Enum writable select."
}
```

### 0x116f Unlock Request

```json
{
  "name": "Unlock Request",
  "id": "0x116f",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Triggers Unlock of Go Box. (resets to 0 after request serviced).",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Go Box Unlock Request",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Unlock Request: Boolean writable switch."
}
```

### 0x142c SBC Request To Power Off Barcode Scanner

```json
{
  "name": "SBC Request To Power Off Barcode Scanner",
  "id": "0x142c",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used by the SBC to request powering the barcode scanner off",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Barcode Scanner Power Disabled",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "SBC Request To Power Off Barcode Scanner: Boolean writable switch."
}
```

### 0x2054 Time Saver Option Request

```json
{
  "name": "Time Saver Option Request",
  "id": "0x2054",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This ERD is used to request a change of the Time Saver option, a feature that allows a user to select a shorter wash cycle.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Time Saver Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Time Saver Option Request: Binary enum writable switch."
}
```

### 0x2057 Steam Option Request

```json
{
  "name": "Steam Option Request",
  "id": "0x2057",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This ERD is used to request a change of the steam option.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Steam Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Steam Option Request: Binary enum writable switch."
}
```

### 0x2060 Tumble Care Option Request

```json
{
  "name": "Tumble Care Option Request",
  "id": "0x2060",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This ERD is used to request a change of the tumble care option.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Tumble Care Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Tumble Care Option Request: Binary enum writable switch."
}
```

### 0x2063 Wash And Dry Option Request

```json
{
  "name": "Wash And Dry Option Request",
  "id": "0x2063",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This ERD is used to request a change of the Wash and Dry option, where a wash cycle is followed by a cycle to dry small loads of laundry.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "WashAndDry Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Wash And Dry Option Request: Binary enum writable switch."
}
```

### 0x206a Load Recommended Washer Link Cycle Request

```json
{
  "name": "Load Recommended Washer Link Cycle Request",
  "id": "0x206a",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Write 255 to this 0x206A to load the cycle in 0x206B Recommended Washer Link Cycle.\nThe ERD will reset back to normal automatically after writing.\n\nDepends on\n- 0x206C Washer Link Option Selection must be Enabled\n\n0x2096 Load Recommended Washer Link Cycle Request is a member of both\n- V1 Washer Link and\n- V1 Washer Link 2",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Load Washer Link Cycle Request",
      "type": "enum",
      "values": {
        "0": "Request Processed",
        "255": "Load Cycle"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Load Recommended Washer Link Cycle Request: Enum writable select."
}
```

### 0x208a Air Fluff Cycle Option Request

```json
{
  "name": "Air Fluff Cycle Option Request",
  "id": "0x208a",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Use this ERD to request a change of ERD 0x2089 Air Fluff option selection. When a request has been processed, the unit will update this value to 0xFF.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Air Fluff Cycle Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Air Fluff Cycle Option Request: Binary enum writable switch."
}
```

### 0x2093 Smart Vent Cycle Option Request

```json
{
  "name": "Smart Vent Cycle Option Request",
  "id": "0x2093",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This ERD requests a change in the smart vent cycle option status. When a request has been processed, the unit will update this value to 0xFF.\n\nDepends on\n- 0x2094 Smart Vent Cycle Option Allowables",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Smart Vent Cycle Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Smart Vent Cycle Option Request: Binary enum writable switch."
}
```

### 0x20a0 Color Keeper Option Request

```json
{
  "name": "Color Keeper Option Request",
  "id": "0x20a0",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request a change of the Color Keeper option. This feature will modify wash cycle parameters to save color in garments.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Color Keeper Option",
      "type": "enum",
      "values": {
        "0": "Disable",
        "1": "Enable"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Color Keeper Option Request: Binary enum writable switch."
}
```

### 0x20a3 No Tangle Wash Option Request

```json
{
  "name": "No Tangle Wash Option Request",
  "id": "0x20a3",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request a change of no tangle wash option.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "No Tangle Wash Option",
      "type": "enum",
      "values": {
        "0": "Disable",
        "1": "Enable"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "No Tangle Wash Option Request: Binary enum writable switch."
}
```

### 0x20a9 True Rinse Option Request

```json
{
  "name": "True Rinse Option Request",
  "id": "0x20a9",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request a change of the True Rinse option, which is a feature that improves rinse performance.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "True Rinse Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "True Rinse Option Request: Binary enum writable switch."
}
```

### 0x20b2 Delay Wash Option Request

```json
{
  "name": "Delay Wash Option Request",
  "id": "0x20b2",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to request a change for delay wash option.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Delay Wash Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Delay Wash Option Request: Binary enum writable switch."
}
```

### 0x20b4 Extra Rinse Option Request

```json
{
  "name": "Extra Rinse Option Request",
  "id": "0x20b4",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to request a change for the extra rinse option.\n\nAfter this ERD is written by a client, it will be updated with an invalid value.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Extra Rinse Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Extra Rinse Option Request: Binary enum writable switch."
}
```

### 0x20b6 Fabric Softener Option Request

```json
{
  "name": "Fabric Softener Option Request",
  "id": "0x20b6",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to request a change for fabric softener option.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Fabric Softener Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Fabric Softener Option Request: Binary enum writable switch."
}
```

### 0x20bd Warm Rinse Option Request

```json
{
  "name": "Warm Rinse Option Request",
  "id": "0x20bd",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to request a change for the warm rinse option.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Warm Rinse Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Warm Rinse Option Request: Binary enum writable switch."
}
```

### 0x2125 Eco Option Request

```json
{
  "name": "Eco Option Request",
  "id": "0x2125",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This ERD requests a change in the Eco Option.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Eco Option Status",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Eco Option Request: Binary enum writable switch."
}
```

### 0x214c Soaking Rinse Option Request

```json
{
  "name": "Soaking Rinse Option Request",
  "id": "0x214c",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This ERD requests a change in the Soaking Rinse Option.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Soaking Rinse Option Status",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Soaking Rinse Option Request: Binary enum writable switch."
}
```

### 0x2156 Wash complete cycle notification option Request

```json
{
  "name": "Wash complete cycle notification option Request",
  "id": "0x2156",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Use this ERD to request a change of the 0x2155 Wash complete cycle notification option. After being written, this ERD is invalidated by changing it to an undefined value.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Wash Complete Notification Enabled",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Wash complete cycle notification option Request: Boolean writable switch."
}
```

### 0x2172 Smart Wash And Rinse Option Request

```json
{
  "name": "Smart Wash And Rinse Option Request",
  "id": "0x2172",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request a change of the smart wash and rinse option.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Smart Wash And Rinse Option",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Smart Wash And Rinse Option Request: Binary enum writable switch."
}
```

### 0x2f1b Short Cycle Option Request

```json
{
  "name": "Short Cycle Option Request",
  "id": "0x2f1b",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request a change of the Short Cycle option. This feature will modify wash cycle time.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Short Cycle Option",
      "type": "enum",
      "values": {
        "0": "Disable",
        "1": "Enable"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Short Cycle Option Request: Binary enum writable switch."
}
```

### 0x3101 Rinse Aid Option State

```json
{
  "name": "Rinse Aid Option State",
  "id": "0x3101",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current state of the Rinse Aid Option State",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Rinse Aid Option Enabled",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Rinse Aid Option State: Boolean writable switch."
}
```

### 0x3108 Door Pocket Light State

```json
{
  "name": "Door Pocket Light State",
  "id": "0x3108",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current state of the door pocket light state",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Door Pocket Light State",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "device_class": "door",
  "confidence": "high",
  "comment": "Door Pocket Light State: Door open/closed binary sensor."
}
```

### 0x3109 Demo Mode State

```json
{
  "name": "Demo Mode State",
  "id": "0x3109",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current state of the Demo Mode state",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Demo Mode State",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Demo Mode State: Boolean writable switch."
}
```

### 0x321f Steam Option State

```json
{
  "name": "Steam Option State",
  "id": "0x321f",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current state of the Steam Option State",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Steam Option State",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Steam Option State: Boolean writable switch."
}
```

### 0x3220 Bottle Blast Option State

```json
{
  "name": "Bottle Blast Option State",
  "id": "0x3220",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current state of the Bottle Blast Option State",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Bottle Blast Option State",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Bottle Blast Option State: Boolean writable switch."
}
```

### 0x3221 UltraFresh Option State

```json
{
  "name": "UltraFresh Option State",
  "id": "0x3221",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current state of the UltraFresh Option State",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "UltraFresh Option State",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "UltraFresh Option State: Boolean writable switch."
}
```

### 0x322b Silverware Wash Option State

```json
{
  "name": "Silverware Wash Option State",
  "id": "0x322b",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current state of the Silverware Wash Option State",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Silverware Wash Option State",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Silverware Wash Option State: Boolean writable switch."
}
```

### 0x3260 Rinse and Hold Request

```json
{
  "name": "Rinse and Hold Request",
  "id": "0x3260",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Requested state of the Rinse and Hold Option",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Rinse and Hold Option Requested State",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Rinse and Hold Request: Boolean writable switch."
}
```

### 0x3263 Auto Open Door Request

```json
{
  "name": "Auto Open Door Request",
  "id": "0x3263",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Requested state of the Auto Open Door Option",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Auto Open Door Option Requested State",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Auto Open Door Request: Boolean writable switch."
}
```

### 0x4008 Mixing valve home state request

```json
{
  "name": "Mixing valve home state request",
  "id": "0x4008",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request mixing valve to cycle to full cold",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Mixing valve home request byte",
      "type": "enum",
      "values": {
        "0": "Write to return to normal operation",
        "1": "Write to cycle to full cold"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Mixing valve home state request: Enum writable select."
}
```

### 0x4223 Requested Water Valve Position

```json
{
  "name": "Requested Water Valve Position",
  "id": "0x4223",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Command to move water valve to given state.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Water Valve Position Request",
      "type": "enum",
      "values": {
        "1": "Open",
        "2": "Closed"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Requested Water Valve Position: Binary enum writable switch."
}
```

### 0x502c Automatic Door Opener Local Public Enable

```json
{
  "name": "Automatic Door Opener Local Public Enable",
  "id": "0x502c",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Enables the automatic door opener (voice to open). There is an agreement in place with UL that this enable must set on the unit, so this ERD needs to remain local-only. This ERD is intended as a unit wide request in coordination with cavity statuses in 5118 and 5218.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Automatic Door Opener Enable",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Automatic Door Opener Local Public Enable: Boolean writable switch."
}
```

### 0x510f Request Upper Door Open

```json
{
  "name": "Request Upper Door Open",
  "id": "0x510f",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Writing true to this will attempt to open the upper cavity door. After door open is attempted, control will clear this to false.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Open Door",
      "type": "enum",
      "values": {
        "0": "Default",
        "1": "Open Door Request"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Request Upper Door Open: Enum writable select."
}
```

### 0x520f Request Lower Door Open

```json
{
  "name": "Request Lower Door Open",
  "id": "0x520f",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Writing true to this will attempt to open the lower cavity door. After door open is attempted, control will clear this to false.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Open Door",
      "type": "enum",
      "values": {
        "0": "Default",
        "1": "Open Door Request"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Request Lower Door Open: Enum writable select."
}
```

### 0x5901 Lock Gas Valve Request

```json
{
  "name": "Lock Gas Valve Request",
  "id": "0x5901",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request Gas Valve to be locked.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Gas Valve Lock Request",
      "type": "enum",
      "values": {
        "0": "Do Nothing",
        "1": "Request Gas Valve to be Locked"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Lock Gas Valve Request: Enum writable select."
}
```

### 0x5b12 Hood Request On/Off

```json
{
  "name": "Hood Request On/Off",
  "id": "0x5b12",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This request turns the hood on to product-specific default light/fan settings. When turning the hood off, the product might save the previously used fan/light settings.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Hood Request On Or Off",
      "type": "enum",
      "values": {
        "0": "Off",
        "1": "On"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Hood Request On/Off: Binary enum writable switch."
}
```

### 0x5b1b Hood Delay Off Request

```json
{
  "name": "Hood Delay Off Request",
  "id": "0x5b1b",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "A request to start or stop the Delay Off Mode",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Requested Delay Off Mode",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Hood Delay Off Request: Binary enum writable switch."
}
```

### 0x5c14 Microwave Remote Enable

```json
{
  "name": "Microwave Remote Enable",
  "id": "0x5c14",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Microwave Remote Enable.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Microwave Remote Enable",
      "type": "enum",
      "values": {
        "0": "Disabled",
        "1": "Enabled"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Microwave Remote Enable: Binary enum writable switch."
}
```

### 0x5c31 Turntable Setting

```json
{
  "name": "Turntable Setting",
  "id": "0x5c31",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current setting of the turntable.  If MWO supports turntable on/off is defined in 0x5C01.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Turntable",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Turntable Setting: Boolean writable switch."
}
```

### 0x7001 Zoneline On/Off Control

```json
{
  "name": "Zoneline On/Off Control",
  "id": "0x7001",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Control the Zoneline unit's state.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Control",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Zoneline On/Off Control: Boolean writable switch."
}
```

### 0x73ff UVC Kit Enable

```json
{
  "name": "UVC Kit Enable",
  "id": "0x73ff",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to enable UVC Kit support",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "UVC Kit support",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "UVC Kit Enable: Boolean writable switch."
}
```

### 0x7406 Constant Fan State

```json
{
  "name": "Constant Fan State",
  "id": "0x7406",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to control constant fan mode",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Constant fan mode",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Constant Fan State: Boolean writable switch."
}
```

### 0x740a Duct Mode

```json
{
  "name": "Duct Mode",
  "id": "0x740a",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to configure duct mode",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Duct mode",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Duct Mode: Boolean writable switch."
}
```

### 0x740b Electric Heat Only mode

```json
{
  "name": "Electric Heat Only mode",
  "id": "0x740b",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to control Electric Heat Only mode",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Electric heat only",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Electric Heat Only mode: Boolean writable switch."
}
```

### 0x740c Boost Heat Mode

```json
{
  "name": "Boost Heat Mode",
  "id": "0x740c",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to control Boost Heat mode",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Boost heat mode",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Boost Heat Mode: Boolean writable switch."
}
```

### 0x740e MUAM Occupancy Enabled

```json
{
  "name": "MUAM Occupancy Enabled",
  "id": "0x740e",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to configure MUAM Occupancy Enabled control",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Occupancy Enabled",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "MUAM Occupancy Enabled: Boolean writable switch."
}
```

### 0x7830 Dehumidifier Pump On/Off State Request

```json
{
  "name": "Dehumidifier Pump On/Off State Request",
  "id": "0x7830",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request to power on/off state for dehumidifier pump.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Power On/Off state",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Dehumidifier Pump On/Off State Request: Boolean writable switch."
}
```

### 0x7911 ODU Pan Heater status and control

```json
{
  "name": "ODU Pan Heater status and control",
  "id": "0x7911",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "ODU Pan Heater Status and control.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "ODU Pan Heater",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "ODU Pan Heater status and control: Boolean writable switch."
}
```

### 0x7912 Compressor Crankcase Heater status and control

```json
{
  "name": "Compressor Crankcase Heater status and control",
  "id": "0x7912",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Compressor Crankcase Heater Status and control.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Compressor Crankcase Heater",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Compressor Crankcase Heater status and control: Boolean writable switch."
}
```

### 0x7914 Defrost status and control

```json
{
  "name": "Defrost status and control",
  "id": "0x7914",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Defrost Status and control.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Defrost State",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Defrost status and control: Boolean writable switch."
}
```

### 0x796e Self Clean Mode Status and Control

```json
{
  "name": "Self Clean Mode Status and Control",
  "id": "0x796e",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Self Clean Mode ON/OFF Status and Control. Status must be reset to 0 when Self Clean Mode Terminates",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Self Clean Status",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Self Clean Mode Status and Control: Boolean writable switch."
}
```

### 0x7976 Vacation Mode (10C Heating Mode) Control

```json
{
  "name": "Vacation Mode (10C Heating Mode) Control",
  "id": "0x7976",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "A Request to put the Appliance into Vacation Mode. Writing to this ERD can change the mode of the Appliance.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Vacation Mode Status Request",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Vacation Mode (10C Heating Mode) Control: Boolean writable switch."
}
```

### 0x7977 Service Mode Electric Room Heater Request

```json
{
  "name": "Service Mode Electric Room Heater Request",
  "id": "0x7977",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Electric Room Heater ON/OFF Request. This ERD only controls the heater during service mode.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Electric Room Heater Requested Status",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Service Mode Electric Room Heater Request: Boolean writable switch."
}
```

### 0x7978 Self Clean Request

```json
{
  "name": "Self Clean Request",
  "id": "0x7978",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Client can request self clean actions to occur using this ERD. After client writes the ERD, the value will be immediately written back to `No Request.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Self Clean Request",
      "type": "enum",
      "values": {
        "0": "No Request",
        "1": "Request Self Clean Cycle To Occur"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Self Clean Request: Enum writable select."
}
```

### 0x79a2 Local Schedule Enable Request

```json
{
  "name": "Local Schedule Enable Request",
  "id": "0x79a2",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request to Enable Local Scheduling, a schedule stored entirely on the Appliance",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Appliance Local Schedule Enabled",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Local Schedule Enable Request: Boolean writable switch."
}
```

### 0x7a0f WAC Power On/Off State

```json
{
  "name": "WAC Power On/Off State",
  "id": "0x7a0f",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The power on/off state for WAC products",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Power On/Off state",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "WAC Power On/Off State: Boolean writable switch."
}
```

### 0x7b05 Sleep Mode

```json
{
  "name": "Sleep Mode",
  "id": "0x7b05",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Sleep mode for split AC",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Sleep Mode",
      "type": "enum",
      "values": {
        "0": "Sleep Mode Off",
        "1": "Sleep Mode On"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Sleep Mode: Binary enum writable switch."
}
```

### 0x7b0c Eco Mode

```json
{
  "name": "Eco Mode",
  "id": "0x7b0c",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Eco mode for Split AC",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Eco Mode",
      "type": "enum",
      "values": {
        "0": "Eco Mode Off",
        "1": "Eco Mode On"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Eco Mode: Binary enum writable switch."
}
```

### 0x7b0e Sleep Mode Request

```json
{
  "name": "Sleep Mode Request",
  "id": "0x7b0e",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Request to turn on/off sleep mode.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Sleep Mode Active",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Sleep Mode Request: Boolean writable switch."
}
```

### 0x9050 Disable Grinder Requested State

```json
{
  "name": "Disable Grinder Requested State",
  "id": "0x9050",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This ERD is used to disable the grinder in case the user is using\npre-ground coffee.\n\nSettings:\n0 = Enable Grinder\n1 = Disable Grinder",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Disable Grinder",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Disable Grinder Requested State: Boolean writable switch."
}
```

### 0x9102 Ice Maker Cloud Schedule Enabled

```json
{
  "name": "Ice Maker Cloud Schedule Enabled",
  "id": "0x9102",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Whether the cloud schedule is enabled or disabled.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Schedule enabled",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Ice Maker Cloud Schedule Enabled: Boolean writable switch."
}
```

### 0x9107 Ice Maker Power

```json
{
  "name": "Ice Maker Power",
  "id": "0x9107",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Power status and control.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Power on",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Ice Maker Power: Boolean writable switch."
}
```

### 0x9202 Toaster Oven Cavity Light Requested State

```json
{
  "name": "Toaster Oven Cavity Light Requested State",
  "id": "0x9202",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The requested state of the cavity light. 0 = off, 1 = on",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Cavity Light On",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Toaster Oven Cavity Light Requested State: Boolean writable switch."
}
```

### 0x922a Toaster Oven Requested Preheat Enabled Setting

```json
{
  "name": "Toaster Oven Requested Preheat Enabled Setting",
  "id": "0x922a",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The requested state of the preheat enabled setting. 0 = disabled, 1 = enabled",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Preheat Enabled",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Toaster Oven Requested Preheat Enabled Setting: Boolean writable switch."
}
```

### 0x922c Toaster Oven Requested Convection Fan State

```json
{
  "name": "Toaster Oven Requested Convection Fan State",
  "id": "0x922c",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The requested state of the convection fan. 0 = off, 1 = on\n\nNote that not all modes allow the operation of the convection fan.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Convection Fan On",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Toaster Oven Requested Convection Fan State: Boolean writable switch."
}
```

### 0x930f Scale Mode Enable

```json
{
  "name": "Scale Mode Enable",
  "id": "0x930f",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to enable scale feedback by displaying weight measured at the unit UI. Write a 1 (true) to enable the scale.  Mixer will enter scale mode.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Enable Scale Mode",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Scale Mode Enable: Boolean writable switch."
}
```

### 0x9422 Auto Warm Enable Requested Setting

```json
{
  "name": "Auto Warm Enable Requested Setting",
  "id": "0x9422",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Auto warm is a feature where if enabled, a warm cycle is initiated once cooking is complete.\nIf auto-warm is disabled the unit transitions to idle once cooking is complete.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Auto Warm Setting Request",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Auto Warm Enable Requested Setting: Boolean writable switch."
}
```

---

## Button (8 ERDs)

One-shot actions (stop, cancel, silence, pause, clear, tare).

### 0x2040 Remote Stop Cycle Request

```json
{
  "name": "Remote Stop Cycle Request",
  "id": "0x2040",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Write zero to this ERD to stop the currently running, paused, delay run or delay paused cycle.\n\nDepends on:\n- ERD 0x2000 must be Run, Pause, Delay Run or Delay Pause\n- ERD 0x2039 must be Enabled\n\nERD 0x2040 is a member of\n- API V1 Remote Start and Stop and\n- API V2 Remote Start and Stop V2.\n\nAPI V2 Remote Start and Stop V2 takes precedence.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Remote Cycle Stop Request",
      "type": "enum",
      "values": {
        "0": "Stop command",
        "255": "Request Processed"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Remote Stop Cycle Request: Enum writable select."
}
```

### 0x2208 Additional Cavity Remote Stop Cycle Request

```json
{
  "name": "Additional Cavity Remote Stop Cycle Request",
  "id": "0x2208",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Write zero to this ERD to stop the currently running, paused, delay run or delay paused additional cavity cycle.\n\nDepends on:\n- ERD 0x2200 must be run, pause, delay run or delay pause.\n- ERD 0x2207 must be enabled.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Remote Cycle Stop Request",
      "type": "enum",
      "values": {
        "0": "Stop command",
        "255": "Request Processed"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Additional Cavity Remote Stop Cycle Request: Enum writable select."
}
```

### 0x7858 Refrigerant Leak Sensor Error Clear Request

```json
{
  "name": "Refrigerant Leak Sensor Error Clear Request",
  "id": "0x7858",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to request the leak sensor clear errors.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Clear",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "device_class": "moisture",
  "confidence": "high",
  "comment": "Refrigerant Leak Sensor Error Clear Request: Leak/moisture detection binary sensor."
}
```

### 0x9224 Toaster Oven Door Alarm Silence

```json
{
  "name": "Toaster Oven Door Alarm Silence",
  "id": "0x9224",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Silence the door alarm. Write 1 to silence alarm.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Silence Door Alarm",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Toaster Oven Door Alarm Silence: Boolean writable switch."
}
```

### 0x9228 Toaster Oven Cancel Operation

```json
{
  "name": "Toaster Oven Cancel Operation",
  "id": "0x9228",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Cancel the oven operation.  This command is write-only.  Write a 1 to this ERD to cancel\nthe current oven operation.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Cancel Operation",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Toaster Oven Cancel Operation: Boolean writable switch."
}
```

### 0x9304 Mixer Pause Mixing Cycle

```json
{
  "name": "Mixer Pause Mixing Cycle",
  "id": "0x9304",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to pause the mixing cycle. Write a 1 (true) to pause.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Mixer Mixing Cycle Paused",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Mixer Pause Mixing Cycle: Boolean writable switch."
}
```

### 0x9310 Tare Scale

```json
{
  "name": "Tare Scale",
  "id": "0x9310",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to zero out the scale measurement by taring the scale. Write a 1 (true) to tare the scale.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Tare Scale",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Tare Scale: Boolean writable switch."
}
```

### 0x9406 Smoke Paused Request

```json
{
  "name": "Smoke Paused Request",
  "id": "0x9406",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The request to pause smoke",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Smoke Paused",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Smoke Paused Request: Boolean writable switch."
}
```

---

## Review: Likely Switch (12 ERDs)

These appear to be toggles but need confirmation.

### 0x201b Legacy - Dryer Extended Tumble Selection

```json
{
  "name": "Legacy - Dryer Extended Tumble Selection",
  "id": "0x201b",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Specifies Extended Tumble selection.\n\nNotes:\n- This is really a legacy ERD and in the past was not a member of any API.\n- It has recently been added to an API to be future compatible.\n- Maintained for Legacy App Versions\n- In legacy units\n  - writing to this ERD will set the ExtendedTumble Selection\n- Modern units maintain this ERD for compatibility with Legacy Apps\n  - writing to this ERD will send a request for this change to 0x2051 Extended Tumble Option Request\n  - if enable request is granted then a request is sent to disable EcoDry via 0x2044 EcoDry Option Request\n  - 0x201B Dryer Extended Tumble Selection is maintained to match 0x2053 Extended Tumble Option Selection\n- Prefer using the Extended Tumble API",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Extended Tumble",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Legacy - Dryer Extended Tumble Selection: Boolean writable switch."
}
```

### 0x5000 Twelve Hour Shutoff

```json
{
  "name": "Twelve Hour Shutoff",
  "id": "0x5000",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Specifies whether the range will automatically stop cooking if cooking for longer than twelve hours.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Twelve Hour Shutoff",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Twelve Hour Shutoff: Boolean writable switch."
}
```

### 0x5001 End Tone

```json
{
  "name": "End Tone",
  "id": "0x5001",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current tone type used to alert either an end of cook or an end of timer to the user.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "End Tone",
      "type": "enum",
      "values": {
        "0": "Beep",
        "1": "Continuous Tone"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "End Tone: Enum writable select."
}
```

### 0x5003 Convection Conversion

```json
{
  "name": "Convection Conversion",
  "id": "0x5003",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Specifies whether convection conversion is enabled.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Convection Conversion",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Convection Conversion: Boolean writable switch."
}
```

### 0x5b04 Hood Delay Off

```json
{
  "name": "Hood Delay Off",
  "id": "0x5b04",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "This activates the Delay Off if the unit is On. It can also be used to cancel a pending delay off.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Delay",
      "type": "enum",
      "values": {
        "0": "Cancel",
        "1": "Activate"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Hood Delay Off: Enum writable select."
}
```

### 0x7401 Smart Fan Cooling

```json
{
  "name": "Smart Fan Cooling",
  "id": "0x7401",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to control smart fan mode during cooling",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Fan mode",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Smart Fan Cooling: Boolean writable switch."
}
```

### 0x7402 Smart Fan Heating

```json
{
  "name": "Smart Fan Heating",
  "id": "0x7402",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to control smart fan mode during heating",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Fan mode",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Smart Fan Heating: Boolean writable switch."
}
```

### 0x7404 Freeze Sentinel

```json
{
  "name": "Freeze Sentinel",
  "id": "0x7404",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to allow Freeze Sentinel",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Freeze sentinel",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Freeze Sentinel: Boolean writable switch."
}
```

### 0x7405 Heat Sentinel

```json
{
  "name": "Heat Sentinel",
  "id": "0x7405",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "AUX setting to allow Heat Sentinel",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Heat sentinel",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Heat Sentinel: Boolean writable switch."
}
```

### 0x7a04 WAC Filter Notification

```json
{
  "name": "WAC Filter Notification",
  "id": "0x7a04",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Notification of whether the filter requires cleaning/replacement",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Filter Notification",
      "type": "enum",
      "values": {
        "0": "Clean filter light off",
        "1": "Clean filter light on"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "WAC Filter Notification: Binary enum writable switch."
}
```

### 0x7b07 Up-down Air Swing

```json
{
  "name": "Up-down Air Swing",
  "id": "0x7b07",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The vertical (up-down) swing",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Up-down Swing",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Up-down Air Swing: Boolean writable switch."
}
```

### 0x7b08 Left-right Air Swing

```json
{
  "name": "Left-right Air Swing",
  "id": "0x7b08",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The horizontal (left-right) swing",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Left-right Swing",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Left-right Air Swing: Boolean writable switch."
}
```

---

## Review: Likely Button (5 ERDs)

These appear to be one-shot start commands.

### 0x2041 Remote Start Extended Tumble

```json
{
  "name": "Remote Start Extended Tumble",
  "id": "0x2041",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Write zero to this ERD to start the Extended Tumble part of the current selected cycle.\n\nDepends on\n- ERD 0x2000 must be Idle, Standby, or End Of Cycle\n- ERD 0x2039 must be Enabled.\n\nAPI V2 Remote Start and Stop V2 takes precedence.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Remote Extended Tumble Start Command",
      "type": "enum",
      "values": {
        "0": "Start Extended Tumble command",
        "255": "Request Processed"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Remote Start Extended Tumble: Enum writable select."
}
```

### 0x209d Remote Care Start Command

```json
{
  "name": "Remote Care Start Command",
  "id": "0x209d",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Writing to this byte will start the current cycle.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Remote Start Command",
      "type": "enum",
      "values": {
        "0": "Start command",
        "255": "Normal State"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Remote Care Start Command: Enum writable select."
}
```

### 0x2133 Remote Sensored Dry Only Cycle Start Command

```json
{
  "name": "Remote Sensored Dry Only Cycle Start Command",
  "id": "0x2133",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Write zero to this ERD to start the Sensor Dry only cycle.\n\nDepends on\n- ERD 0x2000 must be End Of Cycle\n- ERD 0x2039 must be Enabled.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Remote Sensored Dry Only Cycle Start",
      "type": "enum",
      "values": {
        "0": "Start sensored dry only cycle command",
        "255": "Request Processed"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Remote Sensored Dry Only Cycle Start Command: Enum writable select."
}
```

### 0x2149 Remote Start Selected Cycle

```json
{
  "name": "Remote Start Selected Cycle",
  "id": "0x2149",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Client only can write into this ERD once the Remote Start Allowable Status (0x214A) is enabled.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Remote Start Selected Cycle",
      "type": "enum",
      "values": {
        "0": "Start Remote Cycle command",
        "255": "Request Processed"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Remote Start Selected Cycle: Enum writable select."
}
```

### 0x9435 Restore Factory Defaults

```json
{
  "name": "Restore Factory Defaults",
  "id": "0x9435",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Used to reset all user settings on the unit to factory defaults. Write a true to restore factory defaults.",
  "updateClass": {
    "type": "event"
  },
  "data": [
    {
      "name": "Restore Defaults",
      "type": "bool",
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Restore Factory Defaults: Boolean writable switch."
}
```

---

## Review: Unclear (2 ERDs)

These may not be toggles at all.

### 0x5b08 Hood Camera Light Assist Level

```json
{
  "name": "Hood Camera Light Assist Level",
  "id": "0x5b08",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "The current camera light assist setting. When writing, level must be listed as available in available light levels ERD 0x5B09. If 0x5B09 has \"Infinite\" set, then the Light Level is % with max 100.",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Light Level",
      "type": "enum",
      "values": {
        "1": "Dim",
        "2": "High"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Hood Camera Light Assist Level: Enum writable select."
}
```

### 0x8032 Water Softener Shutoff Valve Installed

```json
{
  "name": "Water Softener Shutoff Valve Installed",
  "id": "0x8032",
  "operations": [
    "read",
    "write",
    "publish",
    "subscribe"
  ],
  "description": "Flag indicating whether option is installed",
  "updateClass": {
    "type": "legacy"
  },
  "data": [
    {
      "name": "Water Softener Shutoff Valve Installed",
      "type": "enum",
      "values": {
        "0": "Not Installed",
        "1": "Installed"
      },
      "offset": 0,
      "size": 1
    }
  ],
  "ha_domain": "binary_sensor",
  "confidence": "medium",
  "comment": "Water Softener Shutoff Valve Installed: Enum writable select."
}
```

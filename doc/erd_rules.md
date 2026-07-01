# ERD-Specific Rules

These are exceptions and overrides that apply to specific ERDs only. Generic patterns belong in `AGENTS.md`.

## Filtered ERDs

These ERDs should have correct HA metadata in the JSON but be excluded from JSONL output via name-pattern filtering.

### Firmware & Version ERDs

| ERD | Name | Reason | Filter Pattern |
|---|---|---|---|
| `0x0030` | Ready to Enter Boot Loader | Firmware state indicator, not user-facing | `"ready to enter boot"` |
| `0x0032` | Reset Board | One-shot restart button, not useful in HA | `"reset board"` |
| `0x0035` | Personality (32-bit) | Internal appliance identifier for firmware routing | `"personality"` |
| `0x0038` | Supported Image Types | Firmware metadata (bit-field flags) | `"supported image types"` |
| `0x0039` | Boot Loader Version | Firmware version string | `"boot loader version"` |
| `0x003a` | Application Version | Firmware version string | `"application version"` |
| `0x003b` | Parametric Version | Firmware version string | `"parametric version"` |
| `0x003c` | Auxiliary Version | Firmware version string | `"auxiliary version"` |
| `0x0051` | Available Sound Levels | Appliance capability metadata | `"available sound levels"` |
| `0x0060` | Configuration Hash | SHA-256 hash, firmware metadata | `"configuration hash"` |
| `0x0505` | Image Upload Inference ID | Raw image data, not user-facing | `"image upload inference"` |
| `0x1105` | Engineering Snapshot | Raw engineering data | `"engineering snapshot"` |
| `0x4030` | Notifications | Raw notification data | `"notifications"` |
| `0x4107` | Water Heater Reset Information | Raw reset data | `"water heater reset information"` |
| `0x5300` | Recipe Status | Raw recipe data | `"recipe status"` |
| `0x5405` | Advantium Menu Tree Parametric Hash | Raw hash data | `"menu tree parametric hash"` |
| `0x0117` | Camera Configuration Personality | Camera-specific internal identifier | `"camera configuration personality"` |
| `0x1152` | Mainboard Application Version (v1.0.2) | Firmware version string | `"mainboard application version"` |
| `0x1153` | Temperature Board Application Version | Firmware version string | `"temperature board application version"` |
| `0x1154` | Dispenser Board Application Version | Firmware version string | `"dispenser board application version"` |
| `0x1155` | Door Board Application Version | Firmware version string | `"door board application version"` |
| `0x1156` | Deli-pan Board Application Version | Firmware version string | `"deli-pan board application version"` |
| `0x1157` | WiFi/Zigbee Board Application Version | Firmware version string | `"wifi zigbee board application version"` |
| `0x1158` | Auto-fill (Legacy) Board Application Version | Firmware version string | `"auto-fill board application version"` |
| `0x1159` | Feature Board Application Version | Firmware version string | `"feature board application version"` |
| `0x115a` | RFID Board Application Version | Firmware version string | `"rfid board application version"` |
| `0x115b` | Feature Pan Board Application Version | Firmware version string | `"feature pan board application version"` |
| `0x115c` | Autofill Pitcher Board Application Version | Firmware version string | `"autofill pitcher board application version"` |
| `0x115d` | Convertible Drawer UI Board Application Version | Firmware version string | `"convertible drawer ui board application version"` |

### Service Mode ERDs

| ERD | Name | Reason | Filter Pattern |
|---|---|---|---|
| `0x0036` | Service Mode State Request | Internal technician state (writable) | `"service mode"` |
| `0x0037` | Service Mode State | Internal technician state (read-only) | `"service mode"` |
| `0x7977` | Service Mode Electric Room Heater Request | Internal technician state | `"service mode electric room heater"` |

### Sabbath Mode ERDs (covered by 0x0009)

| ERD | Name | Reason | Filter Pattern |
|---|---|---|---|
| `0x004f` | Enhanced Sabbath Mode Status | Redundant with 0x0009 Sabbath Mode | `"enhanced sabbath mode"` |
| `0x502e` | Enhanced Sabbath State | Redundant with 0x0009 Sabbath Mode | `"enhanced sabbath state"` |
| `0x502f` | Enhanced Sabbath Cooking Accepted Request | Redundant with 0x0009 Sabbath Mode | `"enhanced sabbath cooking accepted"` |
| `0x5030` | Enhanced Sabbath Cooking Accepted Status | Redundant with 0x0009 Sabbath Mode | `"enhanced sabbath cooking accepted"` |
| `0x5031` | Enhanced Sabbath Warmness Setting Request | Redundant with 0x0009 Sabbath Mode | `"enhanced sabbath warmness"` |
| `0x5032` | Enhanced Sabbath Warmness Setting Status | Redundant with 0x0009 Sabbath Mode | `"enhanced sabbath warmness"` |
| `0x5302` | Manual Enhanced Sabbath Schedule Selected | Redundant with 0x0009 Sabbath Mode | `"manual enhanced sabbath schedule"` |

### UI/Settings Redundant with HA

| ERD | Name | Reason | Filter Pattern |
|---|---|---|---|
| `0x0004` | Control User Interface Locked | Internal appliance setting, not useful in HA | `"user interface locked"` |
| `0x0005` | Clock Time | Redundant with system time | `"clock time"` |
| `0x0006` | Clock Format | Redundant with HA system settings | `"clock format"` |
| `0x0007` | Temperature Display Units | Redundant with HA display settings | `"temperature display units"` |

### Still Frame & Sound Themes

| ERD | Name | Fix | Filter Pattern |
|---|---|---|---|
| `0x0502` | Still Frame | 2-val enum (Idle/Capture) → `select` | `"still frame"` |
| `0x0802` | Supported Sound Themes | `bool` read-only → `binary_sensor` | `"supported sound themes"` |


## Domain Overrides

These ERDs have domain assignments that deviate from the generic rules in `AGENTS.md`.

### 2-Value Enum → select (descriptive labels)

Per generic rules, 2-value enums map to `switch` (writable) or `binary_sensor` (read-only). These exceptions use `select` because the values are descriptive labels, not on/off states.

| ERD | Name | Values |
|---|---|---|
| `0x0007` | Temperature Display Units | Fahrenheit / Celsius |
| `0x746c` | Auxiliary 24V Input Status | Active / Inactive |

### Multi-Value Writable Enum → select

These are already correct per generic rules but listed for reference.

| ERD | Name | Value Count |
|---|---|---|
| `0x0009` | Sabbath Mode | 3 |
| `0x000a` | Sound Level | 4 |
| `0x0105` | Hosted Firmware Status | 7 |
| `0x20a7` | Remote Cycle Selection Request | multi |
| `0x20d1` | Downloaded Cycle Request | multi |
| `0x2209` | Additional Cavity Remote Cycle Selection Request | multi |
| `0x2338` | Commercial Remote Free Mode Request | multi |
| `0x6003` | Wireless Connection State | multi |
| `0x7052` | Energy Conservation Request | multi |
| `0x7451` | Fan Configuration in Cooling Request | multi |
| `0x7453` | Fan Configuration in Heating Request | multi |
| `0x745f` | Heat Selector Request | multi |
| `0x7467` | Make-up Air Filter Type Request | multi |
| `0x746b` | Dehumidification Mode Request | multi |
| `0x7473` | Heat Source Optimization Request | multi |
| `0x7703` | System Mode Request | multi |
| `0x7719` | Heat System Mode Fan Setting Request | multi |
| `0x771c` | Fan System Mode Fan Setting Request | multi |
| `0x771f` | Cool System Mode Fan Setting Request | multi |
| `0x795e` | Turbo/Quiet Mode Modifier Request | multi |
| `0x79be` | Fan Operating Mode Request | multi |

### Matter Device ERDs (filtered, 0x0410/0x0411 paired)

These are Matter protocol-level ERDs, not user-facing. 0x0410/0x0411 are paired as request/status.

| ERD | Name | Fix | Filter Pattern |
|---|---|---|---|
| `0x0410` | Matter Device On-Off Request | `bool` writable → `switch` | `"matter device on-off request"` |
| `0x0411` | Matter Device On-Off State | `bool` read-only → `binary_sensor` | `"matter device on-off state"` |
| `0x0412` | Matter Device Temperature Display Mode Request | 2-val enum (Celsius/Fahrenheit) → `select` | `"matter device temperature display mode request"` |
| `0x0413` | Matter Device Temperature Display Mode Actual | 2-val enum (Celsius/Fahrenheit) → `sensor` with `device_class: "enum"` | `"matter device temperature display mode actual"` |

## Request/Status Pairings (32 pairs)

These ERDs were identified as request/status pairs and linked with `paired_erd`/`pair_role`.

| Request ERD | Request Name | Status ERD | Status Name |
|---|---|---|---|
| `0x1308` | Displayed Grow Chamber Request | `0x1309` | Displayed Grow Chamber |
| `0x1322` | Clean Cycle Request | `0x1324` | Clean Cycle State |
| `0x2025` | Warm Rinse Option | `0x20bd` | Warm Rinse Option Request |
| `0x2055` | Time Saver Option | `0x2054` | Time Saver Option Request |
| `0x205b` | Prewash Option | `0x205a` | Prewash Option Request |
| `0x2064` | Wash And Dry Option | `0x2063` | Wash And Dry Option Request |
| `0x2098` | Power Care Option | `0x2097` | Power Care Option Request |
| `0x20a1` | Color Keeper Option | `0x20a0` | Color Keeper Option Request |
| `0x20a4` | No Tangle Wash Option | `0x20a3` | No Tangle Wash Option Request |
| `0x20aa` | True Rinse Option | `0x20a9` | True Rinse Option Request |
| `0x20ab` | Auto Soak Level Option | `0x20ac` | Auto Soak Level Option Request |
| `0x20ad` | Deep Fill Incremental Option | `0x20ae` | Deep Fill Incremental Option Request |
| `0x20af` | Deep Fill Fixed Level Option | `0x20b0` | Deep Fill Fixed Level Option Request |
| `0x20b1` | Delay Wash Option | `0x20b2` | Delay Wash Option Request |
| `0x20b3` | Extra Rinse Option | `0x20b4` | Extra Rinse Option Request |
| `0x20b5` | Fabric Softener Option | `0x20b6` | Fabric Softener Option Request |
| `0x20b7` | Spin Level Option | `0x20b8` | Spin Level Option Request |
| `0x20b9` | Water On Demand Soap Dispense Option | `0x20ba` | Water On Demand Soap Dispense Option Request |
| `0x20bb` | Water Temperature Option | `0x20bc` | Water Temperature Option Request |
| `0x20be` | Soil Level Option | `0x20bf` | Soil Level Option Request |
| `0x20cf` | Stain Removal Guide Option | `0x20d0` | Stain Removal Guide Option Request |
| `0x20d3` | Downloaded Cycle | `0x20d1` | Downloaded Cycle Request |
| `0x20f1` | Adaptive My Cycle Option | `0x20f2` | Adaptive My Cycle Option Request |
| `0x2124` | Eco Option | `0x2125` | Eco Option Request |
| `0x2139` | Remote Spin Time Level | `0x212a` | Remote Spin Time Level Request |
| `0x2134` | Timed Dry Option | `0x2137` | Timed Dry Option Request |
| `0x214b` | Soaking Rinse Option | `0x214c` | Soaking Rinse Option Request |
| `0x2230` | Pet Hair Removal Option | `0x2231` | Pet Hair Removal Option Request |
| `0x2f1a` | Short Cycle Option | `0x2f1b` | Short Cycle Option Request |
| `0x5028` | Articulating Display Mode | `0x5029` | Articulating Display Mode Request |
| `0x502a` | Articulating Display Position | `0x502b` | Articulating Display Position Request |
| `0x9008` | Coffee Brewer Brew Strength | `0x9016` | Coffee Brewer Brew Strength Request |

## Domain Fixes Applied (0x1000-0x5000)

### Writable 2-value enum → select

| ERD | Name |
|---|---|
| `0x1169` | Continuous Flow Alert |
| `0x1306` | Grow State Request |
| `0x1314` | Water Intake Configuration |
| `0x1315` | Paused Mode Request |
| `0x131f` | Reset Water Filter Timer Request |
| `0x1320` | Reset Air Filter Timer Request |
| `0x1321` | Reset Nutrient Cartridge Request |
| `0x2f06` | Mabe - Washer Options |

### Read-only 2-value enum → sensor with device_class: enum

| ERD | Name |
|---|---|
| `0x1162` | Daily Water Usage Update Alert |
| `0x1163` | Water Filter Expiration Alert |
| `0x116c` | System Fault Alert |
| `0x1307` | Grow State |
| `0x130c` | In Home Grower Door Status |
| `0x1323` | Clean Cycle Request Result |
| `0x1326` | Paused Request Result |
| `0x2002` | Remote End Of Cycle State |
| `0x2014` | Add Garment |
| `0x201d` | End Of Cycle Alarm Notification |
| `0x2047` | Damp Alert Status |
| `0x206f` | Blocked Vent Fault Active |
| `0x3038` | Rinse Aid Level |
| `0x304e` | Dishwasher Rinse Aid Sensor Exists |
| `0x3085` | Flood Detected |
| `0x4081` | Anode alarm active |
| `0x4082` | Accessory low battery alarm active |
| `0x40c3` | Missed flow off state |
| `0x40c6` | Service requested |
| `0x40cc` | Service requested (non-GEA) |

### Writable bool → switch

| ERD | Name |
|---|---|
| `0x224a` | Commercial Remote Spin Limit Option Request |
| `0x3086` | Enable Features |
| `0x3202` | Preference Options Request |
| `0x3222` | Enable Features Tub 1 |
| `0x322e` | Dish Favorite Settings Request |
| `0x3251` | Dishwasher Cycle Modifier Requested |
| `0x3253` | Dishwasher Cycle Modifier Requested Tub 1 |

### Read-only bool → binary_sensor

| ERD | Name |
|---|---|
| `0x105a` | Refrigeration Notifications |
| `0x105b` | Refrigeration Supported Notifications |
| `0x1172` | Package Zone Status |
| `0x1175` | Home Water Filter Notification |
| `0x1220` | Dimmable Lighting 0 Configuration |
| `0x122e` | V2 Refrigeration Notification |
| `0x1328` | In Home Grower Notifications |
| `0x20a8` | Remote Cycle Selection Allowables |
| `0x20d2` | Downloaded Cycle Allowables |
| `0x20d4` | Stain Removal Guide Available Options |
| `0x20db` | Water Tank Warnings |
| `0x211e` | Commercial Laundry Payment V1 Attribute Bitmap |
| `0x2154` | Washer and Dryer Combi Push Notifications |
| `0x2162` | Profile Clean Closet Push Notifications |
| `0x2170` | Laundry Center Push Notifications |
| `0x217a` | Dryer Notifications |
| `0x217b` | Dryer Supported Notifications |
| `0x222a` | Washer Push Notifications |
| `0x222b` | Laundry Appliance Fault Push Notifications |
| `0x2f17` | Mabe - Public Fault Code |
| `0x3003` | Reminder |
| `0x3203` | Tub1 1 Reminder |
| `0x3230` | Latched Key Status |
| `0x3250` | Dishwasher Cycle Modifier Actual |
| `0x3252` | Dishwasher Cycle Modifier Actual Tub 1 |
| `0x402b` | Water Heater Mixing Valve Available Tank Capacities |
| `0x4040` | Available Modes |
| `0x4058` | Heating Issues |

### Multi-value enum as binary_sensor → select (writable)

| ERD | Name |
|---|---|
| `0x1032` | Door Mute Status Upper Compartment |
| `0x1033` | Door Mute Status Lower Compartment |
| `0x1034` | Door Mute Status Middle Compartment |

### Multi-value enum as binary_sensor → sensor (read-only)

| ERD | Name |
|---|---|
| `0x1025` | Door In Door Status |
| `0x206c` | Washer Link Option Selection |

### 2-value enum as button → select

| ERD | Name |
|---|---|
| `0x1166` | Water Filter Reset Request |
| `0x2171` | Reset Current Coin Box Count Request |

## Domain Fixes Applied (0x5000-0x9FFF)

### Writable 2-value enum → select

| ERD | Name |
|---|---|
| `0x5001` | End Tone |
| `0x510f` | Request Upper Door Open |
| `0x5111` | Upper Oven Light Level |
| `0x520f` | Request Lower Door Open |
| `0x5211` | Lower Oven Light Level |
| `0x5901` | Lock Gas Valve Request |
| `0x5b04` | Hood Delay Off |
| `0x5b08` | Hood Camera Light Assist Level |
| `0x5b12` | Hood Request On/Off |
| `0x5b1b` | Hood Delay Off Request |
| `0x5b25` | Hood to Hob Request Auto Control |
| `0x5b4e` | Requested Color Scheme |
| `0x5c10` | Microwave Add 30 Second Command |
| `0x5c14` | Microwave Remote Enable |
| `0x5c1b` | Microwave Cook Timer Modification |
| `0x5c1e` | Microwave Kitchen Timer Modification |
| `0x7902` | 4 way valve position |
| `0x7978` | Self Clean Request |
| `0x7a04` | WAC Filter Notification |
| `0x7b05` | Sleep Mode |
| `0x7b0c` | Eco Mode |
| `0x8032` | Water Softener Shutoff Valve Installed |

### Read-only 2-value enum → sensor with device_class: enum

| ERD | Name |
|---|---|
| `0x500f` | Timer ERD Availability |
| `0x5018` | Cavity Layout |
| `0x5403` | Advantium Cook Time Remaining |
| `0x5b01` | Hood Fan Speed Availability |
| `0x5b05` | Hood Delay On |
| `0x5b0b` | Hood Display Protection Fan Speed Availability |
| `0x5b23` | Hood Available Light Colors |
| `0x5b24` | Hood to Hob Actual Auto Control |
| `0x5b4d` | Selected Color Scheme |
| `0x5c1a` | Microwave Cycle Setting Modification Availability |
| `0x7122` | Central desk control |
| `0x7460` | Heat Selector Strict Status |
| `0x7507` | External Thermostat fault state |
| `0x790d` | High and Low Pressure switch status |
| `0x7a10` | Compressor Error Status |
| `0x7a13` | WAC Save Energy Info Indicator |
| `0x7b00` | Available AC Modes |
| `0x7b0b` | Available AC Fan Speeds |
| `0x8007` | Water Softener Low Salt Alert |
| `0x9009` | Coffee Brewer Supported Brew Strengths |
| `0x9012` | Coffee Brewer Pot Present |
| `0x9013` | Coffee Brewer Out of Water |
| `0x905b` | Coffee Brewer Supported Features |
| `0x9237` | Toaster Oven Model |
| `0x930b` | Scale Mode Current Units |
| `0x9312` | Mixer Supported Equipment |

### Writable bool → switch

| ERD | Name |
|---|---|
| `0x7901` | ODU Dip Switch Settings |
| `0x9307` | Reset Mixer Notifications |

### Read-only bool → binary_sensor

| ERD | Name |
|---|---|
| `0x5007` | Oven Configuration |
| `0x5023` | Accent Lighting Request |
| `0x5080` | Cooktop v2 Notifications |
| `0x5081` | Cooktop v2 Supported Notifications |
| `0x511b` | Upper Oven Do Not Stop Cook Mode On Timer Expiration Status |
| `0x521b` | Lower Oven Do Not Stop Cook Mode On Timer Expiration Status |
| `0x5400` | Advantium Remote Cook Mode Configuration |
| `0x576f` | Closed Loop Cooking Supported Devices |
| `0x5b3e` | Hood Notifications V2 |
| `0x5b48` | Supported Hood Notifications V2 |
| `0x5b4c` | Available Color Schemes |
| `0x5c40` | Customer Feedback Request |
| `0x7051` | Air Purifier Request |
| `0x7704` | System Mode Allowed |
| `0x770c` | User Temperature Setpoint Limit Configurable Bitmap |
| `0x771a` | Heat System Mode Available Fan Settings |
| `0x771d` | Fan System Mode Available Fan Settings |
| `0x7720` | Cool System Mode Available Fan Settings |
| `0x7835` | Portable A/C Notifications |
| `0x7836` | Supported Portable A/C Notifications |
| `0x7850` | DFS Notifications |
| `0x7851` | Supported Notifications |
| `0x7900` | ODU DIP Switch Status |
| `0x7910` | Compressor Speed Limiting Factor |
| `0x795f` | Turbo/Quiet Mode Modifier Availability |
| `0x7960` | IDU DIP Switch Status |
| `0x796f` | Cassette IDU DIP Switch Status |
| `0x7970` | Mid-Static IDU DIP Switch Status |
| `0x7971` | Console IDU DIP Switch Status |
| `0x797b` | Alerts |
| `0x79a4` | Alert Status |
| `0x79a5` | Central Controller DIP Switch Status |
| `0x79bf` | Available Fan Operating Modes |
| `0x901c` | Espresso Maker Supported Brew Types |
| `0x9043` | Espresso Maker Supported Features |
| `0x905f` | Coffee Brewer Supported Features v1 |
| `0x910a` | Under Counter Ice Maker Bin Full |
| `0x9135` | Ice Maker Push Notifications |
| `0x9200` | Toaster Oven Supported Cook Modes |
| `0x9236` | Toaster Oven Cooking Push Notifications |
| `0x9303` | Mixer Control Settings Limits |
| `0x9306` | Mixer Notifications |
| `0x9309` | Cycle Setting Modification Availability |
| `0x9311` | Scale Action Availability |
| `0x9317` | Mixer Control v2 Modification Availability |
| `0x9402` | Supported States |
| `0x9403` | Smoke Status |
| `0x9405` | Pause Smoke Status |
| `0x9421` | Auto Warm Enable Current Setting |
| `0x9429` | Auto Warm Reminder Current Setting |
| `0x9437` | Smoker Push Notifications |
| `0x9505` | Sourdough Starter Push Notifications |
| `0xd008` | Available Demand Response Modes |

## Domain Fixes Applied (0xD000)

### Read-only 2-value enum → sensor with device_class: enum

| ERD | Name |
|---|---|
| `0xd015` | Appliance Energy Usage Estimated or Measured Flag |
| `0xd018` | Appliance Hot Water Usage Estimated or Measured Flag |
| `0xd01b` | Appliance Cold Water Usage Estimated or Measured Flag |
| `0xd01e` | Appliance Gas Usage Estimated or Measured Flag |
